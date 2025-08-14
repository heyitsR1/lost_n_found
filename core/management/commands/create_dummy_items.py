from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from core.models import Item, Category, Location
import random
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Create dummy lost and found items for testing'

    def handle(self, *args, **options):
        # Check if we have categories and locations
        if Category.objects.count() == 0 or Location.objects.count() == 0:
            self.stdout.write(self.style.ERROR('Please run python manage.py populate_data first to create categories and locations'))
            return

        # Check if we have at least one user
        if User.objects.count() == 0:
            self.stdout.write(self.style.WARNING('Creating a test user since no users exist'))
            user = User.objects.create_user(
                email='test@example.com',
                password='testpassword123',
                first_name='Test',
                last_name='User',
                student_id='K123456'
            )
        else:
            # Get the first user
            user = User.objects.first()

        # Get all categories and locations
        categories = list(Category.objects.all())
        locations = list(Location.objects.all())

        # Sample item descriptions
        lost_descriptions = [
            "I lost this item near the cafeteria. It has sentimental value to me.",
            "Left this in the library study room. Please contact me if found.",
            "Misplaced during the campus event. It's very important for my classes.",
            "Can't find it since yesterday. I really need it for my project.",
            "Lost somewhere between the dorms and the science building. Reward offered!"
        ]

        found_descriptions = [
            "Found this item near the student center. Contact me to claim it.",
            "Picked this up in classroom 101. Describe it to claim.",
            "Found on the bench outside the library. Looks valuable.",
            "Discovered this in the parking lot. Contact me with details to verify ownership.",
            "Found after the campus event. Please provide details to claim it."
        ]

        # Create lost items
        self.stdout.write('Creating lost items...')
        lost_items = [
            {
                'title': 'Lost MacBook Pro',
                'category': next(cat for cat in categories if cat.name == 'Electronics'),
                'location': random.choice(locations),
                'is_urgent': True,
                'reward': 50.00
            },
            {
                'title': 'Missing Blue Backpack',
                'category': next(cat for cat in categories if cat.name == 'Bags'),
                'location': random.choice(locations),
                'is_urgent': False,
                'reward': None
            },
            {
                'title': 'Lost Student ID Card',
                'category': next(cat for cat in categories if cat.name == 'Other'),
                'location': random.choice(locations),
                'is_urgent': True,
                'reward': 10.00
            },
            {
                'title': 'Missing Textbook - Data Structures',
                'category': next(cat for cat in categories if cat.name == 'Books'),
                'location': random.choice(locations),
                'is_urgent': False,
                'reward': None
            },
            {
                'title': 'Lost Car Keys with Red Keychain',
                'category': next(cat for cat in categories if cat.name == 'Keys'),
                'location': random.choice(locations),
                'is_urgent': True,
                'reward': 20.00
            },
        ]

        # Create found items
        self.stdout.write('Creating found items...')
        found_items = [
            {
                'title': 'Found iPhone 13',
                'category': next(cat for cat in categories if cat.name == 'Phones'),
                'location': random.choice(locations),
                'is_urgent': False,
                'contact_name': 'John Finder',
                'contact_email': 'john@example.com',
                'contact_phone': '555-123-4567'
            },
            {
                'title': 'Found Black Wallet',
                'category': next(cat for cat in categories if cat.name == 'Wallets'),
                'location': random.choice(locations),
                'is_urgent': False,
                'contact_name': 'Sarah Smith',
                'contact_email': 'sarah@example.com',
                'contact_phone': '555-987-6543'
            },
            {
                'title': 'Found Glasses in Case',
                'category': next(cat for cat in categories if cat.name == 'Other'),
                'location': random.choice(locations),
                'is_urgent': False,
                'contact_name': 'Mike Johnson',
                'contact_email': 'mike@example.com',
                'contact_phone': '555-456-7890'
            },
            {
                'title': 'Found Nike Jacket',
                'category': next(cat for cat in categories if cat.name == 'Clothing'),
                'location': random.choice(locations),
                'is_urgent': False,
                'contact_name': 'Emily Davis',
                'contact_email': 'emily@example.com',
                'contact_phone': '555-234-5678'
            },
            {
                'title': 'Found Calculator',
                'category': next(cat for cat in categories if cat.name == 'Electronics'),
                'location': random.choice(locations),
                'is_urgent': False,
                'contact_name': 'Alex Brown',
                'contact_email': 'alex@example.com',
                'contact_phone': '555-345-6789'
            },
        ]

        # Create the items in the database
        now = timezone.now()
        items_created = 0

        # Create lost items
        for item_data in lost_items:
            # Create with random date in the past 30 days
            random_days = random.randint(1, 30)
            created_date = now - timedelta(days=random_days)
            
            item = Item.objects.create(
                title=item_data['title'],
                description=random.choice(lost_descriptions),
                item_type='lost',
                status='active',
                category=item_data['category'],
                location=item_data['location'],
                user=user,
                is_urgent=item_data['is_urgent'],
                reward=item_data['reward'],
            )
            
            # Update the created_at field
            Item.objects.filter(pk=item.pk).update(created_at=created_date)
            
            self.stdout.write(f'Created lost item: {item.title}')
            items_created += 1

        # Create found items
        for item_data in found_items:
            # Create with random date in the past 30 days
            random_days = random.randint(1, 30)
            created_date = now - timedelta(days=random_days)
            
            item = Item.objects.create(
                title=item_data['title'],
                description=random.choice(found_descriptions),
                item_type='found',
                status='active',
                category=item_data['category'],
                location=item_data['location'],
                user=user,
                is_urgent=item_data['is_urgent'],
                contact_name=item_data['contact_name'],
                contact_email=item_data['contact_email'],
                contact_phone=item_data['contact_phone'],
            )
            
            # Update the created_at field
            Item.objects.filter(pk=item.pk).update(created_at=created_date)
            
            self.stdout.write(f'Created found item: {item.title}')
            items_created += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {items_created} dummy items!')
        )