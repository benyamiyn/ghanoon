from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Category, Comment, Maqale


class CommentViewTest(TestCase):

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
            "blog:add_comment",
            kwargs={"slug": self.maqale.slug}
        )

    def test_login_required(self):

        response = self.client.post(
            self.url,
            {"text": "Hello"}
        )

        self.assertEqual(response.status_code, 302)

    def test_add_comment(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        response = self.client.post(
            self.url,
            {
                "text": "First Comment"
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Comment.objects.count(),
            1
        )

    def test_comment_text(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        self.client.post(
            self.url,
            {
                "text": "Hello Django"
            }
        )

        comment = Comment.objects.first()

        self.assertEqual(
            comment.text,
            "Hello Django"
        )

    def test_empty_comment_not_created(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        self.client.post(
            self.url,
            {
                "text": ""
            }
        )

        self.assertEqual(
            Comment.objects.count(),
            0
        )

    def test_reply_comment(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        parent = Comment.objects.create(
            maqale=self.maqale,
            author=self.user,
            text="Parent"
        )

        self.client.post(
            self.url,
            {
                "text": "Child",
                "parent_id": parent.id
            }
        )

        child = Comment.objects.last()

        self.assertEqual(
            child.parent,
            parent
        )

    def test_reply_invalid_parent(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        self.client.post(
            self.url,
            {
                "text": "Reply",
                "parent_id": 999
            }
        )

        comment = Comment.objects.first()

        self.assertIsNone(
            comment.parent
        )

    def test_comment_author(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        self.client.post(
            self.url,
            {
                "text": "Author Test"
            }
        )

        comment = Comment.objects.first()

        self.assertEqual(
            comment.author,
            self.user
        )

    def test_comment_article(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        self.client.post(
            self.url,
            {
                "text": "Article Test"
            }
        )

        comment = Comment.objects.first()

        self.assertEqual(
            comment.maqale,
            self.maqale
        )

    def test_redirect_after_comment(self):

        self.client.login(
            username="ali",
            password="1234"
        )

        response = self.client.post(
            self.url,
            {
                "text": "Redirect"
            }
        )

        self.assertRedirects(
            response,
            self.maqale.get_absolute_url()
        )