from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Category, Like, Maqale


class LikeViewTest(TestCase):

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

        self.url = reverse(
            "blog:toggle_like",
            kwargs={"slug": self.maqale.slug}
        )

    def test_login_required(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_create_like(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        self.client.get(self.url)

        self.assertEqual(
            Like.objects.count(),
            1
        )

    def test_like_belongs_to_user(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        self.client.get(self.url)

        like = Like.objects.first()

        self.assertEqual(
            like.user,
            self.user
        )

    def test_like_belongs_to_article(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        self.client.get(self.url)

        like = Like.objects.first()

        self.assertEqual(
            like.maqale,
            self.maqale
        )

    def test_toggle_like_removes_like(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        self.client.get(self.url)

        self.assertEqual(
            Like.objects.count(),
            1
        )

        self.client.get(self.url)

        self.assertEqual(
            Like.objects.count(),
            0
        )

    def test_redirect_after_like(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            self.maqale.get_absolute_url()
        )

    def test_only_one_like_exists(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        self.client.get(self.url)
        self.client.get(self.url)
        self.client.get(self.url)

        self.assertEqual(
            Like.objects.count(),
            1
        )

    def test_like_deleted_after_second_click(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        self.client.get(self.url)
        self.client.get(self.url)

        self.assertFalse(
            Like.objects.filter(
                user=self.user,
                maqale=self.maqale
            ).exists()
        )