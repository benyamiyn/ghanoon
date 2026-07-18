from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from blog.models import Category, Comment, Like, Maqale


class CategoryModelTest(TestCase):

    def test_create_category(self):
        category = Category.objects.create(title="Python")

        self.assertEqual(category.title, "Python")

    def test_str(self):
        category = Category.objects.create(title="Python")

        self.assertEqual(str(category), "Python")


class MaqaleModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="ali",
            password="1234"
        )

        self.category = Category.objects.create(
            title="Backend"
        )

    def test_create_maqale(self):

        maqale = Maqale.objects.create(
            title="Django Test",
            matn="Hello World",
            author=self.user,
            category=self.category
        )

        self.assertEqual(maqale.title, "Django Test")

    def test_slug_is_created(self):

        maqale = Maqale.objects.create(
            title="سلام دنیا",
            matn="text",
            author=self.user,
            category=self.category
        )

        self.assertTrue(maqale.slug)

    def test_slug_is_unique(self):

        one = Maqale.objects.create(
            title="Python",
            matn="1",
            author=self.user,
            category=self.category
        )

        two = Maqale.objects.create(
            title="Python",
            matn="2",
            author=self.user,
            category=self.category
        )

        self.assertNotEqual(one.slug, two.slug)

    def test_str(self):

        maqale = Maqale.objects.create(
            title="Article",
            matn="text",
            author=self.user,
            category=self.category
        )

        self.assertEqual(str(maqale), "Article")

    def test_get_absolute_url(self):

        maqale = Maqale.objects.create(
            title="Article",
            matn="text",
            author=self.user,
            category=self.category
        )

        self.assertEqual(
            maqale.get_absolute_url(),
            f"/{maqale.slug}/"
        )


class CommentModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="reza",
            password="1234"
        )

        self.category = Category.objects.create(
            title="Python"
        )

        self.maqale = Maqale.objects.create(
            title="Test",
            matn="text",
            author=self.user,
            category=self.category
        )

    def test_create_comment(self):

        comment = Comment.objects.create(
            maqale=self.maqale,
            author=self.user,
            text="Hello"
        )

        self.assertEqual(comment.text, "Hello")

    def test_parent_comment(self):

        parent = Comment.objects.create(
            maqale=self.maqale,
            author=self.user,
            text="Parent"
        )

        child = Comment.objects.create(
            maqale=self.maqale,
            author=self.user,
            text="Child",
            parent=parent
        )

        self.assertEqual(child.parent, parent)

    def test_is_parent_property(self):

        comment = Comment.objects.create(
            maqale=self.maqale,
            author=self.user,
            text="Hello"
        )

        self.assertTrue(comment.is_parent)

    def test_child_is_not_parent(self):

        parent = Comment.objects.create(
            maqale=self.maqale,
            author=self.user,
            text="Parent"
        )

        child = Comment.objects.create(
            maqale=self.maqale,
            author=self.user,
            text="Child",
            parent=parent
        )

        self.assertFalse(child.is_parent)

    def test_comment_str(self):

        comment = Comment.objects.create(
            maqale=self.maqale,
            author=self.user,
            text="Hello"
        )

        self.assertEqual(
            str(comment),
            "reza - Test"
        )


class LikeModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="ali",
            password="1234"
        )

        self.category = Category.objects.create(
            title="Python"
        )

        self.maqale = Maqale.objects.create(
            title="Article",
            matn="text",
            author=self.user,
            category=self.category
        )

    def test_create_like(self):

        like = Like.objects.create(
            maqale=self.maqale,
            user=self.user
        )

        self.assertEqual(
            like.user,
            self.user
        )

    def test_unique_like(self):

        Like.objects.create(
            maqale=self.maqale,
            user=self.user
        )

        with self.assertRaises(IntegrityError):

            Like.objects.create(
                maqale=self.maqale,
                user=self.user
            )

    def test_like_str(self):

        like = Like.objects.create(
            maqale=self.maqale,
            user=self.user
        )

        self.assertEqual(
            str(like),
            "ali likes Article"
        )