from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import List, ListItem


class TestList(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test",
            email="test@example.com",
        )

    def test_list_creation_with_defaults(self):
        l = List.objects.create(
            owner=self.user,
            title="A Test List",
        )
        self.assertEqual(l.owner, self.user)
        self.assertEqual(l.title, "A Test List")
        self.assertFalse(l.is_public)
        self.assertEqual(l.items.count(), 0)

    def test_list_creation_with_set_values(self):
        l = List.objects.create(
            owner=self.user, title="Another Test List", is_public=True
        )
        self.assertEqual(l.owner, self.user)
        self.assertEqual(l.title, "Another Test List")
        self.assertTrue(l.is_public)
        self.assertEqual(l.items.count(), 0)

    def test_list_with_list_items(self):
        l = List.objects.create(
            owner=self.user, title="Another Test List", is_public=True
        )
        ListItem.objects.create(text="A list item", list=l)
        self.assertEqual(l.owner, self.user)
        self.assertEqual(l.title, "Another Test List")
        self.assertTrue(l.is_public)
        self.assertEqual(l.items.count(), 1)
        self.assertEqual(l.items.first().text, "A list item")
