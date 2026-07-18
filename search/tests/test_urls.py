from django.test import SimpleTestCase
from django.urls import resolve, reverse

from search.views import (
    search,
    suggest,
    live_search,
)


class SearchUrlsTest(SimpleTestCase):

    def test_search_url(self):

        url = reverse("search:search")

        self.assertEqual(
            resolve(url).func,
            search,
        )

    def test_suggest_url(self):

        url = reverse("search:suggest")

        self.assertEqual(
            resolve(url).func,
            suggest,
        )

    def test_live_search_url(self):

        url = reverse("search:live")

        self.assertEqual(
            resolve(url).func,
            live_search,
        )

    def test_url_paths(self):

        self.assertEqual(
            reverse("search:search"),
            "/search/",
        )

        self.assertEqual(
            reverse("search:suggest"),
            "/search/suggest/",
        )

        self.assertEqual(
            reverse("search:live"),
            "/search/live/",
        )