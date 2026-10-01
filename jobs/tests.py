from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Applications, Jobs, Sectors


class JobPortalTests(TestCase):
    def setUp(self):
        self.sector = Sectors.objects.create(name="Engineering")
        self.owner = User.objects.create_user("owner@example.com", password="safe-password-123")
        self.candidate = User.objects.create_user("candidate@example.com", password="safe-password-123")
        self.job = Jobs.objects.create(title="Backend Engineer", sector=self.sector, location="Remote", description="Build reliable APIs for customers.", salary="12-18 LPA", author=self.owner)

    def test_search_finds_relevant_jobs(self):
        response = self.client.get(reverse("all_jobs"), {"q": "backend"})
        self.assertContains(response, "Backend Engineer")

    def test_candidate_can_apply_once(self):
        self.client.login(username="candidate@example.com", password="safe-password-123")
        self.client.post(reverse("apply_job", args=[self.job.id]))
        self.client.post(reverse("apply_job", args=[self.job.id]))
        self.assertEqual(Applications.objects.filter(job=self.job, user=self.candidate).count(), 1)

    def test_other_user_cannot_edit_job(self):
        self.client.login(username="candidate@example.com", password="safe-password-123")
        response = self.client.get(reverse("update_job", args=[self.job.id]))
        self.assertRedirects(response, reverse("login") + "?next=" + reverse("update_job", args=[self.job.id]))

    def test_only_staff_can_create_or_delete_jobs(self):
        self.client.login(username="candidate@example.com", password="safe-password-123")
        self.assertEqual(self.client.get(reverse("add_job")).status_code, 302)
        self.assertEqual(self.client.post(reverse("delete_job", args=[self.job.id])).status_code, 302)
        self.assertTrue(Jobs.objects.filter(id=self.job.id).exists())
