from django.contrib.auth.models import User
from core.models import Profile

# Users data
users = [
    {'id': 2, 'username': 'user2', 'email': 'user2@example.com', 'password': 'password2'},
    {'id': 3, 'username': 'user3', 'email': 'user3@example.com', 'password': 'password3'},
    {'id': 4, 'username': 'user4', 'email': 'user4@example.com', 'password': 'password4'},
    {'id': 5, 'username': 'user5', 'email': 'user5@example.com', 'password': 'password5'},
]

for user_data in users:
    user, created = User.objects.get_or_create(id=user_data['id'], username=user_data['username'], defaults=user_data)
    if created:
        user.set_password(user_data['password'])
        user.save()
    # Ensure profile exists
    Profile.objects.get_or_create(user=user)
