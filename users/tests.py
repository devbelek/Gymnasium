from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from datetime import datetime
from .models import UserProfile, Donation, ConfirmedDonation
from main.models import Graduates, SuccessfulGraduates, Teachers

class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(user=self.user, about='Test profile')
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.about, 'Test profile')

    def test_user_profile_str(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(str(profile), 'testuser')

    def test_unique_user_profile(self):
        UserProfile.objects.create(user=self.user)
        with self.assertRaises(Exception):
            UserProfile.objects.create(user=self.user)

class DonationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.file_mock = SimpleUploadedFile("file.txt", b"file_content")

    def test_donation_creation(self):
        donation = Donation.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            confirmation_file=self.file_mock
        )
        self.assertEqual(donation.user.username, 'testuser')
        self.assertEqual(donation.amount, Decimal('100.00'))

    def test_donation_str(self):
        donation = Donation.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            confirmation_file=self.file_mock
        )
        expected_str = f"{self.user.username} - 100.00 - {donation.date}"
        self.assertEqual(str(donation), expected_str)

class ConfirmedDonationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.file_mock = SimpleUploadedFile("file.txt", b"file_content")
        self.donation = Donation.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            confirmation_file=self.file_mock
        )

    def test_confirmed_donation_creation(self):
        confirmed_donation = ConfirmedDonation.objects.create(
            donation=self.donation,
            user=self.user
        )
        self.assertEqual(confirmed_donation.user.username, 'testuser')
        self.assertEqual(confirmed_donation.amount, Decimal('100.00'))

    def test_confirmed_donation_str(self):
        confirmed_donation = ConfirmedDonation.objects.create(
            donation=self.donation,
            user=self.user
        )
        expected_str = f"{self.user.username} - 100.00 - {confirmed_donation.date}"
        self.assertEqual(str(confirmed_donation), expected_str)

class GraduatesTest(TestCase):
    def setUp(self):
        self.teacher = Teachers.objects.create(name='Test Teacher')

    def test_graduates_creation(self):
        graduate = Graduates.objects.create(
            name='John',
            surname='Doe',
            year=2024,
            ort=200,
            kl_rukovoditel=self.teacher
        )
        self.assertEqual(graduate.name, 'John')
        self.assertEqual(graduate.surname, 'Doe')
        self.assertEqual(graduate.year, 2024)
        self.assertEqual(graduate.ort, 200)

    def test_graduates_str(self):
        graduate = Graduates.objects.create(
            name='John',
            surname='Doe',
            year=2024,
            ort=200,
            kl_rukovoditel=self.teacher
        )
        self.assertEqual(str(graduate), 'Выпускники 2024 года: John Doe')

    def test_graduates_year_validator(self):
        current_year = datetime.now().year
        with self.assertRaises(Exception):
            Graduates.objects.create(
                name='John',
                surname='Doe',
                year=current_year + 1,
                ort=200,
                kl_rukovoditel=self.teacher
            )

class SuccessfulGraduatesTest(TestCase):
    def setUp(self):
        self.teacher = Teachers.objects.create(name='Test Teacher')
        self.graduate = Graduates.objects.create(
            name='John',
            surname='Doe',
            year=2024,
            ort=200,
            kl_rukovoditel=self.teacher
        )

    def test_successful_graduates_creation(self):
        successful_graduate = SuccessfulGraduates.objects.create(
            graduate=self.graduate,
            year=2024,
            title='Success Story',
            content='Test content'
        )
        self.assertEqual(successful_graduate.graduate, self.graduate)
        self.assertEqual(successful_graduate.year, 2024)
        self.assertEqual(successful_graduate.title, 'Success Story')