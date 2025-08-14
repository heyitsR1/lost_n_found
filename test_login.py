from django.contrib.auth import authenticate

user = authenticate(email='testuser@example.com', password='testpassword123')
if user:
    print(f'Authentication successful: {user}')
else:
    print('Authentication failed')