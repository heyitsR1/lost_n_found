from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password

try:
    user = CustomUser.objects.create(
        email='testuser@example.com',
        student_id='K123456',
        first_name='Test',
        last_name='User',
        password=make_password('testpassword123')
    )
    print(f'User created: {user}')
except Exception as e:
    print(f'Error creating user: {e}')