from django.forms import TextInput
from django.test import TestCase

from search.forms import SearchForm


class SearchFormTest(TestCase):

    def test_form_is_valid(self):

        form = SearchForm(
            data={
                "q": "django",
                "sort": "newest",
            }
        )

        self.assertTrue(form.is_valid())

    def test_empty_query_is_valid(self):

        form = SearchForm(
            data={
                "q": "",
                "sort": "newest",
            }
        )

        self.assertTrue(form.is_valid())

    def test_invalid_sort(self):

        form = SearchForm(
            data={
                "q": "django",
                "sort": "invalid",
            }
        )

        self.assertFalse(form.is_valid())

    def test_placeholder(self):

        form = SearchForm()

        self.assertEqual(
            form.fields["q"].widget.attrs["placeholder"],
            "جست و جو",
        )

    def test_q_widget(self):

        form = SearchForm()

        self.assertIsInstance(
            form.fields["q"].widget,
            TextInput,
        )

    def test_q_max_length(self):

        form = SearchForm()

        self.assertEqual(
            form.fields["q"].max_length,
            100,
        )

    def test_q_not_required(self):

        form = SearchForm()

        self.assertFalse(
            form.fields["q"].required,
        )

    def test_sort_not_required(self):

        form = SearchForm()

        self.assertFalse(
            form.fields["sort"].required,
        )

    def test_sort_choices(self):

        form = SearchForm()

        self.assertEqual(
            len(form.fields["sort"].choices),
            3,
        )

    def test_form_fields(self):

        form = SearchForm()

        self.assertEqual(
            list(form.fields.keys()),
            [
                "q",
                "sort",
            ],
        )