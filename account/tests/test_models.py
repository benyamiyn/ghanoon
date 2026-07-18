from django.contrib.auth.models import User
from django.test import TestCase

from account.models import Profile


class ProfileModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="ali",
            password="1234",
            first_name="Ali",
            last_name="Ahmadi",
            email="ali@test.com",
        )

    def test_create_profile(self):

        profile = Profile.objects.create(
            user=self.user
        )

        self.assertEqual(
            profile.user,
            self.user
        )

    def test_str(self):

        profile = Profile.objects.create(
            user=self.user
        )

        self.assertEqual(
            str(profile),
            "ali"
        )

    def test_bio_default(self):

        profile = Profile.objects.create(
            user=self.user
        )

        self.assertEqual(
            profile.bio,
            ""
        )

    def test_birth_date_default(self):

        profile = Profile.objects.create(
            user=self.user
        )

        self.assertIsNone(
            profile.birth_date
        )

    def test_profile_has_user(self):

        profile = Profile.objects.create(
            user=self.user
        )

        self.assertEqual(
            profile.user.username,
            "ali"
        )

    def test_one_profile_per_user(self):

        Profile.objects.create(
            user=self.user
        )

        with self.assertRaises(Exception):

            Profile.objects.create(
                user=self.user
            )