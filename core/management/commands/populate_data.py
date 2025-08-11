from django.core.management.base import BaseCommand
from core.models import Category, Location


class Command(BaseCommand):
    help = 'Populate initial data for the lost and found platform'

    def handle(self, *args, **options):
        self.stdout.write('Creating categories...')
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'icon': 'laptop', 'color': '#007bff'},
            {'name': 'Clothing', 'icon': 'tshirt', 'color': '#28a745'},
            {'name': 'Books', 'icon': 'book', 'color': '#ffc107'},
            {'name': 'Jewelry', 'icon': 'gem', 'color': '#dc3545'},
            {'name': 'Keys', 'icon': 'key', 'color': '#6c757d'},
            {'name': 'Wallets', 'icon': 'wallet', 'color': '#fd7e14'},
            {'name': 'Phones', 'icon': 'mobile-alt', 'color': '#e83e8c'},
            {'name': 'Bags', 'icon': 'briefcase', 'color': '#20c997'},
            {'name': 'Sports Equipment', 'icon': 'futbol', 'color': '#17a2b8'},
            {'name': 'Other', 'icon': 'question-circle', 'color': '#6f42c1'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'color': cat_data['color']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')
        
        self.stdout.write('Creating locations...')
        
        # Create locations
        locations_data = [
            {'name': 'Main Library', 'building': 'Library', 'floor': '1st Floor'},
            {'name': 'Student Center', 'building': 'Student Center', 'floor': 'Ground Floor'},
            {'name': 'Science Building', 'building': 'Science Building', 'floor': '2nd Floor'},
            {'name': 'Cafeteria', 'building': 'Student Center', 'floor': '1st Floor'},
            {'name': 'Gymnasium', 'building': 'Sports Complex', 'floor': 'Ground Floor'},
            {'name': 'Computer Lab', 'building': 'Technology Building', 'floor': '3rd Floor'},
            {'name': 'Parking Lot A', 'building': 'Parking', 'floor': 'Ground Floor'},
            {'name': 'Administration Building', 'building': 'Admin Building', 'floor': '1st Floor'},
            {'name': 'Classroom 101', 'building': 'Academic Building', 'floor': '1st Floor', 'room': '101'},
            {'name': 'Classroom 202', 'building': 'Academic Building', 'floor': '2nd Floor', 'room': '202'},
            {'name': 'Study Room 1', 'building': 'Library', 'floor': '2nd Floor', 'room': 'Study Room 1'},
            {'name': 'Campus Grounds', 'building': 'Outdoor', 'floor': 'Ground Floor'},
        ]
        
        for loc_data in locations_data:
            location, created = Location.objects.get_or_create(
                name=loc_data['name'],
                defaults={
                    'building': loc_data.get('building', ''),
                    'floor': loc_data.get('floor', ''),
                    'room': loc_data.get('room', '')
                }
            )
            if created:
                self.stdout.write(f'Created location: {location.name}')
            else:
                self.stdout.write(f'Location already exists: {location.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated initial data!')
        ) 