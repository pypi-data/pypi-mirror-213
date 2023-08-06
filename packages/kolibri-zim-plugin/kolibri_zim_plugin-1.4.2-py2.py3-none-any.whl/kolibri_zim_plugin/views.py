from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import random
import textwrap
import time

from django.core.urlresolvers import get_resolver
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotFound
from django.http import HttpResponseNotModified
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.http import JsonResponse
from django.http import QueryDict
from django.utils.cache import patch_response_headers
from django.utils.http import http_date
from django.views import View
from kolibri.core.content.utils.paths import get_content_storage_file_path
from zimply_core.zim_core import to_bytes
from zimply_core.zim_core import ZIMClient

# This provides an API similar to the zipfile view in Kolibri core's zip_wsgi.
# In the future, we should replace this with a change adding Zim file support
# in the same place: <https://github.com/endlessm/kolibri/pull/3>.
#
# We are avoiding Django REST Framework here in case this code needs to be
# moved to the alternative zip_wsgi server.


YEAR_IN_SECONDS = 60 * 60 * 24 * 365
SNIPPET_MAX_CHARS = 280


class ZimFileNotFoundError(Exception):
    pass


class ZimFileReadError(Exception):
    pass


class _ZimFileViewMixin(View):
    zim_client_args = {"enable_search": False}

    def dispatch(self, request, *args, **kwargs):
        zim_filename = kwargs["zim_filename"]

        try:
            self.zim_client = self.__get_zim_client(zim_filename)
        except ZimFileNotFoundError:
            return HttpResponseNotFound("Zim file does not exist")
        except ZimFileReadError:
            return HttpResponseServerError("Error reading Zim file")

        return super(_ZimFileViewMixin, self).dispatch(request, *args, **kwargs)

    def __get_zim_client(self, zim_filename):
        zim_file_path = get_content_storage_file_path(zim_filename)

        if not os.path.exists(zim_file_path):
            raise ZimFileNotFoundError()

        # Raises RuntimeError
        try:
            # A ZIMClient requires an encoding (usually UTF-8). The
            # auto_delete property only applies to an FTS index and will
            # automagically recreate an index if any issues are detected.
            zim_client = ZIMClient(
                zim_file_path,
                encoding="utf-8",
                auto_delete=True,
                **self.zim_client_args
            )
        except RuntimeError as error:
            raise ZimFileReadError(str(error))

        return zim_client


class _ImmutableViewMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method != "GET":
            return super(_ImmutableViewMixin, self).dispatch(request, *args, **kwargs)
        elif request.META.get("HTTP_IF_MODIFIED_SINCE"):
            return HttpResponseNotModified()
        else:
            response = super(_ImmutableViewMixin, self).dispatch(
                request, *args, **kwargs
            )
        if response.status_code == 200:
            patch_response_headers(response, cache_timeout=YEAR_IN_SECONDS)
        return response


class ZimIndexView(_ImmutableViewMixin, _ZimFileViewMixin, View):
    http_method_names = (
        "get",
        "options",
    )

    def get(self, request, zim_filename):
        main_page = self.zim_client.main_page

        if main_page is None:
            return HttpResponseNotFound("Article does not exist")

        article_url = _zim_article_url(
            zim_filename, main_page.full_url, redirect_from=""
        )

        return HttpResponseRedirect(article_url)


class ZimArticleView(_ImmutableViewMixin, _ZimFileViewMixin, View):
    http_method_names = (
        "get",
        "options",
    )

    def get(self, request, zim_filename, zim_article_path):
        redirect_from = request.GET.get("redirect_from")

        try:
            zim_article = self.zim_client.get_article(
                zim_article_path, follow_redirect=False
            )
        except KeyError:
            return HttpResponseNotFound("Article does not exist")

        if zim_article.redirect_to_url:
            article_url = _zim_article_url(
                zim_filename,
                zim_article.redirect_to_url,
                redirect_from=zim_article.full_url,
            )
            return HttpResponseRedirect(article_url)

        if self._article_is_main_page(zim_article) and redirect_from != "":
            # Make the main page article work like it does via ZimIndexView
            article_url = _zim_article_url(
                zim_filename,
                zim_article.full_url,
                redirect_from="",
            )
            return HttpResponseRedirect(article_url)

        return self._get_response_for_article(zim_article)

    def _article_is_main_page(self, article):
        if not self.zim_client.main_page:
            return False

        return self.zim_client.main_page.full_url == article.full_url

    def _get_response_for_article(self, article):
        if article is None:
            return HttpResponseNotFound("Article does not exist")

        response = HttpResponse()
        article_bytes = to_bytes(article.data, "utf-8")
        response["Content-Length"] = len(article_bytes)
        # Ensure the browser knows not to try byte-range requests, as we don't support them here
        response["Accept-Ranges"] = "none"
        response["Last-Modified"] = http_date(time.time())
        if article.mimetype.startswith("text/"):
            response["Content-Type"] = "{mimetype}; charset={charset}".format(
                mimetype=article.mimetype, charset="utf-8"
            )
        else:
            response["Content-Type"] = article.mimetype
        response.write(article_bytes)
        return response


class ZimRandomArticleView(_ZimFileViewMixin, View):
    http_method_names = (
        "get",
        "options",
    )

    def get(self, request, zim_filename):
        random_article_path = self.__get_random_article_path()
        return JsonResponse({"zimFile": zim_filename, "zimPath": random_article_path})

    def __get_random_article_path(self):
        if self.zim_client._zim_file.version <= (6, 0):
            return self.zim_client.random_article_url
        else:
            # We are unable to get a random article with new Zim files
            # <https://github.com/kimbauters/ZIMply/issues/26>
            # But we can do an expensive workaround. We'll try a random sample
            # of articles, and return the first one that has the correct
            # mimetype. If we exhaust our list of random samples, we will have
            # to return None.

            articles_range = self.zim_client._zim_file.get_articles_range()
            random_articles_list = random.sample(
                range(articles_range.start, articles_range.end), 100
            )

            for article_id in random_articles_list:
                article = self.zim_client._zim_file.get_article_by_id(article_id)
                if article.mimetype == "text/html":
                    return article.full_url

            return None


class ZimSearchView(_ZimFileViewMixin, View):
    zim_client_args = {"enable_search": True}

    MAX_RESULTS_MAXIMUM = 100

    def get(self, request, zim_filename):
        query = request.GET.get("query")
        suggest = "suggest" in request.GET
        start = request.GET.get("start", 0)
        max_results = request.GET.get("max_results", 30)
        if suggest:
            snippet_length = None
        else:
            snippet_length = request.GET.get("snippet_length", SNIPPET_MAX_CHARS)

        if not query:
            return HttpResponseBadRequest('Missing "query"')

        try:
            start = int(start)
        except ValueError:
            return HttpResponseBadRequest('Invalid "start"')

        try:
            max_results = int(max_results)
        except ValueError:
            return HttpResponseBadRequest('Invalid "max_results"')

        if max_results < 0 or max_results > self.MAX_RESULTS_MAXIMUM:
            return HttpResponseBadRequest('Invalid "max_results"')

        # This results in a list of SearchResult objects ordered by their
        # score (lower is better is earlier in the list)...

        if suggest:
            count = self.zim_client.get_suggestions_results_count(query)
            search = self.zim_client.suggest(
                query, start=start, end=start + max_results
            )
        else:
            count = self.zim_client.get_search_results_count(query)
            search = self.zim_client.search(query, start=start, end=start + max_results)

        articles = list(
            self.__article_metadata(result, snippet_length) for result in search
        )

        return JsonResponse({"articles": articles, "count": count})

    def __article_metadata(self, search_result, snippet_length):
        full_url = search_result.namespace + "/" + search_result.url
        zim_article = self.zim_client.get_article(full_url, follow_redirect=False)

        result = {}

        if zim_article.redirect_to_url:
            result["redirect_from"] = zim_article.title
            zim_article = self.zim_client.get_article(full_url, follow_redirect=True)

        result["path"] = zim_article.full_url
        result["title"] = zim_article.title

        if snippet_length:
            result["snippet"] = _zim_article_snippet(zim_article, snippet_length)

        return result


def _zim_article_url(zim_filename, zim_article_path, redirect_from=None):
    # I don't know why I need to torment the resolver like this instead of
    # using django.urls.reverse, but something is trying to add a language
    # prefix incorrectly and causing an error.
    resolver = get_resolver(None)
    url = "/" + resolver.reverse(
        "zim_article", zim_filename=zim_filename, zim_article_path=zim_article_path
    )
    if redirect_from is not None:
        query = QueryDict(mutable=True)
        query["redirect_from"] = redirect_from
        return "{url}?{query}".format(url=url, query=query.urlencode())
    else:
        return url


def _zim_article_snippet(zim_article, max_chars):
    soup = _zim_article_soup(zim_article)

    if soup is None:
        return None

    return _html_snippet(soup, max_chars)


def _zim_article_soup(zim_article):
    try:
        import bs4
    except ImportError:
        return None

    html_str = to_bytes(zim_article.data, "utf-8")

    try:
        # Use lxml if it is available in this environment
        soup = bs4.BeautifulSoup(html_str, "lxml")
    except bs4.FeatureNotFound:
        # Otherwise, fall back to Python's built in html parser
        soup = bs4.BeautifulSoup(html_str, "html.parser")

    return soup


def _html_snippet(soup, max_chars):
    snippet_text = _html_snippet_text(soup)
    return textwrap.shorten(snippet_text, width=max_chars, placeholder="")


def _html_snippet_text(soup):
    meta_description = soup.find("meta", attrs={"name": "description"})

    if meta_description:
        description_text = meta_description.get("content").strip()
    else:
        description_text = None

    if description_text:
        return description_text

    article_elems = filter(
        _filter_article_elem,
        soup.find("body").find_all(["h2", "h3", "h4", "h5", "h6", "p"]),
    )
    article_elems_text = "\n".join(elem.get_text() for elem in article_elems)

    if len(article_elems_text) > 0:
        return article_elems_text

    return soup.find("body").get_text().strip()


def _filter_article_elem(elem):
    exclude_parent_roles = [
        "banner",
        "complementary",
        "contentinfo",
        "form",
        "navigation",
        "search",
    ]

    # In addition to excluding elements by role, we can filter some well-known
    # class names in supported zim files.

    exclude_parent_classes = [
        "article_byline",  # WikiHow
    ]

    while elem:
        if elem.has_attr("hidden"):
            return False
        elif elem.get("role") in exclude_parent_roles:
            return False
        elif any(
            elem_class in exclude_parent_classes
            for elem_class in elem.get_attribute_list("class")
        ):
            return False
        elem = elem.parent

    return True
