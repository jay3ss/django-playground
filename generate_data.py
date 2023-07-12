import random
import requests

from django.contrib.auth import get_user_model

from lists.models import List, ListItem


User = get_user_model()

# Generate 15 different usernames
response = requests.get("https://randomuser.me/api/?results=15")
data = response.json()
usernames = [user["login"]["username"] for user in data["results"]]

# create the users
users = [
    User.objects.create_user(
        username=username,
        email=f"{username}@example.com",
        password="password",
    )
    for username in usernames
]

# Generate 10 titles for to-do lists
list_titles = [
    "Shopping List",
    "Home Improvement Tasks",
    "Work Projects",
    "Fitness Goals",
    "Recipe Ideas",
    "Travel Bucket List",
    "Books to Read",
    "Movies to Watch",
    "Gift Ideas",
    "Personal Goals",
]

# Generate 25 list items
response = requests.get("https://api.quotable.io/random?count=25")
data = response.json()

list_items = [quote["content"] for quote in data["results"]]

lists = [
    List.objects.create(
        title=random.choice(list_titles),
        owner=random.choice(users),
    )
]
lists.items = [
    ListItem.objects.create(
        text=random.choice(list_items),
        is_public=random.choice([True, False]),
    )
]
