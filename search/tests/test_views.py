from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Category, Maqale


class SearchViewsTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="ali",
            password="1234"
        )

        self.category = Category.objects.create(
            title="Backend"
        )

        self.article1 = Maqale.objects.create(
            title="Django Tutorial",
            matn="Learning Django Framework",
            author=self.user,
            category=self.category,
        )

        self.article2 = Maqale.objects.create(
            title="Python Basics",
            matn="Python Programming",
            author=self.user,
            category=self.category,
        )

    # ---------------- SEARCH ---------------- #

    def test_search_page_status(self):

        response = self.client.get(
            reverse("search:search")
        )

        self.assertEqual(response.status_code, 200)

    def test_search_template(self):

        response = self.client.get(
            reverse("search:search")
        )

        self.assertTemplateUsed(
            response,
            "search/search_results.html"
        )

    def test_search_by_title(self):

        response = self.client.get(
            reverse("search:search"),
            {"q": "Django"}
        )

        self.assertContains(
            response,
            "Django Tutorial"
        )

    def test_search_by_body(self):

        response = self.client.get(
            reverse("search:search"),
            {"q": "Programming"}
        )

        self.assertContains(
            response,
            "Python Basics"
        )

    def test_search_by_author(self):

        response = self.client.get(
            reverse("search:search"),
            {"q": "ali"}
        )

        self.assertEqual(
            len(response.context["articles"]),
            2
        )

    def test_search_by_category(self):

        response = self.client.get(
            reverse("search:search"),
            {"q": "Backend"}
        )

        self.assertEqual(
            len(response.context["articles"]),
            2
        )

    def test_empty_query(self):

        response = self.client.get(
            reverse("search:search"),
            {"q": ""}
        )

        self.assertEqual(
            len(response.context["articles"]),
            0
        )

    def test_invalid_query(self):

        response = self.client.get(
            reverse("search:search"),
            {"q": "Java"}
        )

        self.assertEqual(
            len(response.context["articles"]),
            0
        )

    def test_sort_newest(self):

        response = self.client.get(
            reverse("search:search"),
            {
                "q": "Python",
                "sort": "newest"
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_sort_oldest(self):

        response = self.client.get(
            reverse("search:search"),
            {
                "q": "Python",
                "sort": "oldest"
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_sort_title(self):

        response = self.client.get(
            reverse("search:search"),
            {
                "q": "Python",
                "sort": "title"
            }
        )

        self.assertEqual(response.status_code, 200)

    # ---------------- SUGGEST ---------------- #

    def test_suggest_status(self):

        response = self.client.get(
            reverse("search:suggest"),
            {"q": "Dja"}
        )

        self.assertEqual(response.status_code, 200)

    def test_suggest_returns_json(self):

        response = self.client.get(
            reverse("search:suggest"),
            {"q": "Dja"}
        )

        self.assertContains(
            response,
            "Django Tutorial"
        )

    def test_suggest_empty(self):

        response = self.client.get(
            reverse("search:suggest")
        )

        self.assertJSONEqual(
            response.content,
            []
        )

    # ---------------- LIVE ---------------- #

    def test_live_status(self):

        response = self.client.get(
            reverse("search:live"),
            {"q": "Python"}
        )

        self.assertEqual(response.status_code, 200)

    def test_live_template(self):

        response = self.client.get(
            reverse("search:live"),
            {"q": "Python"}
        )

        self.assertTemplateUsed(
            response,
            "search/live_results.html"
        )

    def test_live_context(self):

        response = self.client.get(
            reverse("search:live"),
            {"q": "Python"}
        )

        self.assertGreater(
            len(response.context["articles"]),
            0
        )

    def test_live_empty(self):

        response = self.client.get(
            reverse("search:live")
        )

        self.assertEqual(
            len(response.context["articles"]),
            0
        )