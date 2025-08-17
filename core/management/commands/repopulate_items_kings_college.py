from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Item, Category, Location
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Repopulate items with King\'s College locations'

    def handle(self, *args, **options):
        self.stdout.write('Repopulating items with King\'s College locations...')
        
        # Get or create a test user
        user, created = User.objects.get_or_create(
            email='test@kings.edu',
            defaults={
                'username': 'testuser',
                'first_name': 'Test',
                'last_name': 'User',
                'student_id': 'KS2024001',
                'phone_number': '+1-555-0000',
                'department': 'Computer Science',
                'graduation_year': 2026,
                'is_staff': False,
                'is_superuser': False,
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f'Created test user: {user.email}')
        
        # Get categories
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write('No categories found. Please run populate_data command first.')
            return
        
        # Get locations
        locations = list(Location.objects.all())
        if not locations:
            self.stdout.write('No locations found. Please run populate_kings_college_locations command first.')
            return
        
        # Clear existing items
        Item.objects.all().delete()
        self.stdout.write('Cleared existing items.')
        
        # Sample items data with King's College locations
        items_data = [
            # Lost Items
            {
                'title': 'iPhone 15 Pro - Lost in Library',
                'description': 'Lost my iPhone 15 Pro while studying in the library. It has a black case with a cracked screen protector. Last seen on the study table near the IT Lab entrance.',
                'item_type': 'lost',
                'category': categories[0] if categories else None,
                'location': next((loc for loc in locations if loc.floor_area == 'library'), locations[0]),
                'is_urgent': True,
                'reward_coins': 50,
                'user': user,
                'created_at': timezone.now() - timedelta(hours=2)
            },
            {
                'title': 'MacBook Air - Left in Class 301',
                'description': 'Forgot my MacBook Air in Class 301 after the morning lecture. It\'s a silver 13-inch model with a sticker of King\'s College logo on the back.',
                'item_type': 'lost',
                'category': categories[0] if categories else None,
                'location': next((loc for loc in locations if loc.floor_area == 'class_301'), locations[0]),
                'is_urgent': True,
                'reward_coins': 100,
                'user': user,
                'created_at': timezone.now() - timedelta(hours=4)
            },
            {
                'title': 'Student ID Card - Lost in Canteen',
                'description': 'Lost my student ID card while having lunch in the canteen. Name: John Smith, ID: KS2024001. Please return to admin section.',
                'item_type': 'lost',
                'category': categories[0] if categories else None,
                'location': next((loc for loc in locations if loc.floor_area == 'canteen'), locations[0]),
                'is_urgent': False,
                'reward_coins': 25,
                'user': user,
                'created_at': timezone.now() - timedelta(hours=6)
            },
            {
                'title': 'AirPods Pro - Lost in Parking',
                'description': 'Lost my AirPods Pro in the main parking area. They were in a white charging case. Last used while walking to my car.',
                'item_type': 'lost',
                'category': categories[0] if categories else None,
                'location': next((loc for loc in locations if loc.location_type == 'parking'), locations[0]),
                'is_urgent': False,
                'reward_coins': 75,
                'user': user,
                'created_at': timezone.now() - timedelta(hours=8)
            },
            {
                'title': 'Calculus Textbook - Left in Class 201',
                'description': 'Left my calculus textbook in Class 201 after the afternoon session. It\'s a blue hardcover book with "Calculus: Early Transcendentals" on the cover.',
                'item_type': 'lost',
                'category': categories[0] if categories else None,
                'location': next((loc for loc in locations if loc.floor_area == 'class_201'), locations[0]),
                'is_urgent': False,
                'reward_coins': 30,
                'user': user,
                'created_at': timezone.now() - timedelta(hours=10)
            },
            
            # Found Items
            {
                'title': 'Found: Samsung Galaxy Phone',
                'description': 'Found this Samsung Galaxy phone in the IT Lab. It was left on the computer desk near the printer. Phone is locked but has a blue case.',
                'item_type': 'found',
                'category': categories[0] if categories else None,
                'location': next((loc for loc in locations if loc.floor_area == 'it_lab'), locations[0]),
                'is_urgent': False,
                'reward_coins': 0,
                'user': user,
                'contact_name': 'Sarah Johnson',
                'contact_email': 'sarah.j@kings.edu',
                'contact_phone': '+1-555-0123',
                'created_at': timezone.now() - timedelta(hours=1)
            },
            {
                'title': 'Found: Nike Jacket in Program Hall',
                'description': 'Found a black Nike jacket in the Program Hall after the evening event. Size L, has a small tear on the left sleeve. Currently at admin section.',
                'item_type': 'found',
                'category': categories[0] if categories else None,
                'location': next((loc for loc in locations if loc.floor_area == 'program_hall'), locations[0]),
                'is_urgent': False,
                'reward_coins': 0,
                'user': user,
                'contact_name': 'Mike Chen',
                'contact_email': 'mike.c@kings.edu',
                'contact_phone': '+1-555-0456',
                'status': 'dropped_off',
                'dropped_at_admin': True,
                'dropped_at_admin_date': timezone.now() - timedelta(hours=2),
                'created_at': timezone.now() - timedelta(hours=3)
            },
            {
                'title': 'Found: Calculator in Kafe Kodes',
                'description': 'Found a scientific calculator on the table in Kafe Kodes. It\'s a Casio fx-991EX model. Left it with the barista.',
                'item_type': 'found',
                'category': categories[0] if categories else None,
                'location': next((loc for loc in locations if loc.floor_area == 'kafe_kodes'), locations[0]),
                'is_urgent': False,
                'reward_coins': 0,
                'user': user,
                'contact_name': 'Emma Davis',
                'contact_email': 'emma.d@kings.edu',
                'contact_phone': '+1-555-0789',
                'created_at': timezone.now() - timedelta(hours=5)
            },
            {
                'title': 'Found: Keys in Tech Club Room',
                'description': 'Found a set of car keys in the Tech Club room. They have a King\'s College keychain and a small USB drive attached.',
                'item_type': 'found',
                'category': categories[0] if categories else None,
                'location': next((loc for loc in locations if loc.floor_area == 'tech_club'), locations[0]),
                'is_urgent': False,
                'reward_coins': 0,
                'user': user,
                'contact_name': 'Alex Rodriguez',
                'contact_email': 'alex.r@kings.edu',
                'contact_phone': '+1-555-0321',
                'created_at': timezone.now() - timedelta(hours=7)
            },
            {
                'title': 'Found: Water Bottle in Class 401',
                'description': 'Found a stainless steel water bottle in Class 401 after the morning lecture. It\'s a Hydro Flask with "King\'s College" sticker.',
                'item_type': 'found',
                'category': categories[0] if categories else None,
                'location': next((loc for loc in locations if loc.floor_area == 'class_401'), locations[0]),
                'is_urgent': False,
                'reward_coins': 0,
                'user': user,
                'contact_name': 'Lisa Wang',
                'contact_email': 'lisa.w@kings.edu',
                'contact_phone': '+1-555-0654',
                'created_at': timezone.now() - timedelta(hours=9)
            },
            {
                'title': 'Found: Student Card in DoLab',
                'description': 'Found a student ID card in the DoLab on the 6th floor. Name: David Kim, ID: KS2024123. Dropped off at admin section.',
                'item_type': 'found',
                'category': categories[0] if categories else None,
                'location': next((loc for loc in locations if loc.floor_area == 'dolab'), locations[0]),
                'is_urgent': False,
                'reward_coins': 0,
                'user': user,
                'contact_name': 'Tom Wilson',
                'contact_email': 'tom.w@kings.edu',
                'contact_phone': '+1-555-0987',
                'status': 'dropped_off',
                'dropped_at_admin': True,
                'dropped_at_admin_date': timezone.now() - timedelta(hours=4),
                'created_at': timezone.now() - timedelta(hours=5)
            },
            {
                'title': 'Found: Laptop Charger in Library',
                'description': 'Found a MacBook charger in the library study area. It\'s a 65W USB-C charger with a white cable. Left at the front desk.',
                'item_type': 'found',
                'category': categories[0] if categories else None,
                'location': next((loc for loc in locations if loc.floor_area == 'library'), locations[0]),
                'is_urgent': False,
                'reward_coins': 0,
                'user': user,
                'contact_name': 'Rachel Green',
                'contact_email': 'rachel.g@kings.edu',
                'contact_phone': '+1-555-0543',
                'created_at': timezone.now() - timedelta(hours=6)
            }
        ]
        
        created_items = []
        for item_data in items_data:
            item = Item.objects.create(**item_data)
            created_items.append(item)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created_items)} items with King\'s College locations!'
            )
        )
        
        # Display created items
        for item in created_items:
            self.stdout.write(f'  - {item.get_item_type_display()}: {item.title} at {item.location}')
        
        self.stdout.write('\nItems are now ready with the new location system!')
