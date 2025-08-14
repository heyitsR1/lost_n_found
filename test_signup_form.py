from accounts.forms import CustomSignupForm
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
import uuid

# Create a test request
factory = RequestFactory()
request = factory.get('/accounts/signup/')

# Add session to request
middleware = SessionMiddleware(lambda req: None)
middleware.process_request(request)
request.session.save()

# Generate a unique email
unique_id = uuid.uuid4().hex[:8]
email = f"testuser_{unique_id}@example.com"
student_id = f"K{unique_id[:6]}"

# Create form data
form_data = {
    'email': email,
    'student_id': student_id,
    'first_name': 'Test',
    'last_name': 'User',
    'password1': 'testpassword123',
    'password2': 'testpassword123',
    'phone_number': '1234567890',
    'department': 'Computer Science'
}

print(f"Testing with email: {email} and student_id: {student_id}")

# Create and validate the form
form = CustomSignupForm(form_data)
print(f"Form is valid: {form.is_valid()}")
if not form.is_valid():
    print(f"Form errors: {form.errors}")
else:
    # Save the user
    user = form.save(request)
    print(f"User created: {user}")
    
    # Verify the user was saved to the database
    User = get_user_model()
    try:
        saved_user = User.objects.get(email=email)
        print(f"User found in database: {saved_user}")
        print(f"User ID: {saved_user.id}")
        print(f"Student ID: {saved_user.student_id}")
        print(f"First Name: {saved_user.first_name}")
        print(f"Last Name: {saved_user.last_name}")
    except User.DoesNotExist:
        print("User not found in database!")