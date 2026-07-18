from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Category, Comment, Like, Maqale


class BlogViewsTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="ali",
            password="1234"
        )

        self.category = Category.objects.create(
            title="Python"
        )

        self.maqale = Maqale.objects.create(
            title="Django",
            matn="Hello",
            author=self.user,
            category=self.category
        )

    def test_home_page_status(self):

        response = self.client.get(
            reverse("blog:home")
        )

        self.assertEqual(response.status_code, 200)

    def test_home_template(self):

        response = self.client.get(
            reverse("blog:home")
        )

        self.assertTemplateUsed(
            response,
            "blog/home.html"
        )

    def test_home_context(self):

        response = self.client.get(
            reverse("blog:home")
        )

        self.assertIn(
            self.maqale,
            response.context["maqaleha"]
        )

    def test_detail_status(self):

        response = self.client.get(
            reverse(
                "blog:detail",
                kwargs={"slug": self.maqale.slug}
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_detail_template(self):

        response = self.client.get(
            reverse(
                "blog:detail",
                kwargs={"slug": self.maqale.slug}
            )
        )

        self.assertTemplateUsed(
            response,
            "blog/post_detail.html"
        )

    def test_detail_context(self):

        response = self.client.get(
            reverse(
                "blog:detail",
                kwargs={"slug": self.maqale.slug}
            )
        )

        self.assertEqual(
            response.context["maqale"],
            self.maqale
        )

    def test_like_count_initially_zero(self):

        response = self.client.get(
            reverse(
                "blog:detail",
                kwargs={"slug": self.maqale.slug}
            )
        )

        self.assertEqual(
            response.context["like_count"],
            0
        )

    def test_like_count(self):

        Like.objects.create(
            maqale=self.maqale,
            user=self.user
        )

        response = self.client.get(
            reverse(
                "blog:detail",
                kwargs={"slug": self.maqale.slug}
            )
        )

        self.assertEqual(
            response.context["like_count"],
            1
        )

    def test_comments_in_context(self):

        comment = Comment.objects.create(
            maqale=self.maqale,
            author=self.user,
            text="hello"
        )

        response = self.client.get(
            reverse(
                "blog:detail",
                kwargs={"slug": self.maqale.slug}
            )
        )

        self.assertIn(
            comment,
            response.context["comments"]
        )

    def test_invalid_slug_returns_404(self):

        response = self.client.get(
            reverse(
                "blog:detail",
                kwargs={"slug": "invalid-slug"}
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )