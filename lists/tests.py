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
        self.assertEqual(self.user.lists.first(), l)
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

    def test_that_user_cant_see_other_users_private_lists(self):
        user2 = get_user_model().objects.create_user(
            username="test2",
            email="test2@example.com",
        )


class TestListItem(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test",
            email="test@example.com",
        )
        cls.list = List.objects.create(
            owner=cls.user,
            title="A Test List",
        )

    def test_list_item_creation_with_defaults(self):
        li = ListItem.objects.create(
            text="A list item",
            list=self.list,
        )
        self.assertEqual(li.list.owner, self.user)
        self.assertEqual(li.list, self.list)
        self.assertEqual(li.text, "A list item")
        self.assertFalse(li.is_complete)

    def test_list_item_creation_with_set_values(self):
        li = ListItem.objects.create(
            text="A list item", list=self.list, is_complete=True
        )
        self.assertEqual(li.list.owner, self.user)
        self.assertEqual(li.text, "A list item")
        self.assertTrue(li.is_complete)
