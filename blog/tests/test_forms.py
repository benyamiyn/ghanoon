from django.test import TestCase
from django.forms import Textarea, HiddenInput

from blog.forms import CommentForm


class CommentFormTest(TestCase):

    def test_form_is_valid(self):

        form = CommentForm(
            data={
                "text": "سلام"
            }
        )

        self.assertTrue(form.is_valid())

    def test_empty_text_is_invalid(self):

        form = CommentForm(
            data={
                "text": ""
            }
        )

        self.assertFalse(form.is_valid())

    def test_parent_id_is_optional(self):

        form = CommentForm(
            data={
                "text": "Hello"
            }
        )

        self.assertTrue(form.is_valid())

    def test_parent_id_accepts_value(self):

        form = CommentForm(
            data={
                "text": "Reply",
                "parent_id": 5
            }
        )

        self.assertTrue(form.is_valid())

    def test_text_widget(self):

        form = CommentForm()

        self.assertIsInstance(
            form.fields["text"].widget,
            Textarea
        )

    def test_parent_widget(self):

        form = CommentForm()

        self.assertIsInstance(
            form.fields["parent_id"].widget,
            HiddenInput
        )

    def test_placeholder(self):

        form = CommentForm()

        self.assertEqual(
            form.fields["text"].widget.attrs["placeholder"],
            "نظر خود را بنویسید"
        )

    def test_rows(self):

        form = CommentForm()

        self.assertEqual(
            form.fields["text"].widget.attrs["rows"],
            4
        )

    def test_form_fields(self):

        form = CommentForm()

        self.assertEqual(
            list(form.fields.keys()),
            ["text", "parent_id"]
        )
        