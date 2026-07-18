from django.test import SimpleTestCase
from django.urls import resolve, reverse

from blog.views import (
    home,
    maqale_detail,
    add_comment,
    toggle_like,
)


class BlogUrlsTest(SimpleTestCase):

    def test_home_url(self):
        self.assertEqual(
            resolve(reverse("blog:home")).func,
            home
        )

    def test_detail_url(self):
        url = reverse(
            "blog:detail",
            kwargs={"slug": "test"}
        )

        self.assertEqual(
            resolve(url).func,
            maqale_detail
        )

    def test_comment_url(self):
        url = reverse(
            "blog:add_comment",
            kwargs={"slug": "test"}
        )

        self.assertEqual(
            resolve(url).func,
            add_comment
        )

    def test_like_url(self):
        url = reverse(
            "blog:toggle_like",
            kwargs={"slug": "test"}
        )

        self.assertEqual(
            resolve(url).func,
            toggle_like
        )