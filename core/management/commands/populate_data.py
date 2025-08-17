from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Category, Location, Voucher, RewardCoin
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate initial data for the Lost N Found system'

    def handle(self, *args, **options):
        self.stdout.write('Populating initial data...')
        
        # Create categories if they don't exist
        categories_data = [
            {'name': 'Electronics', 'icon': 'laptop', 'color': '#007bff'},
            {'name': 'Books', 'icon': 'book', 'color': '#28a745'},
            {'name': 'Clothing', 'icon': 'tshirt', 'color': '#dc3545'},
            {'name': 'Jewelry', 'icon': 'gem', 'color': '#ffc107'},
            {'name': 'Keys', 'icon': 'key', 'color': '#6c757d'},
            {'name': 'Wallets', 'icon': 'credit-card', 'color': '#17a2b8'},
            {'name': 'Bags', 'icon': 'briefcase', 'color': '#6f42c1'},
            {'name': 'Sports Equipment', 'icon': 'futbol', 'color': '#fd7e14'},
            {'name': 'Musical Instruments', 'icon': 'music', 'color': '#e83e8c'},
            {'name': 'Other', 'icon': 'tag', 'color': '#6c757d'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create locations if they don't exist
        locations_data = [
            {'name': 'Main Library', 'building': 'Library Building', 'floor': '1st Floor'},
            {'name': 'Student Center', 'building': 'Student Center', 'floor': 'Ground Floor'},
            {'name': 'Science Building', 'building': 'Science Building', 'floor': '2nd Floor'},
            {'name': 'Cafeteria', 'building': 'Student Center', 'floor': '1st Floor'},
            {'name': 'Computer Lab', 'building': 'Technology Building', 'floor': '3rd Floor'},
            {'name': 'Gymnasium', 'building': 'Sports Complex', 'floor': 'Ground Floor'},
            {'name': 'Parking Lot A', 'building': 'Parking Area', 'floor': 'Ground Floor'},
            {'name': 'Lecture Hall 101', 'building': 'Academic Building', 'floor': '1st Floor'},
            {'name': 'Study Room 205', 'building': 'Library Building', 'floor': '2nd Floor'},
            {'name': 'Campus Grounds', 'building': 'Outdoor Area', 'floor': 'Ground Floor'},
            {'name': 'Bookstore', 'building': 'Student Center', 'floor': 'Ground Floor'},
            {'name': 'Administration Office', 'building': 'Admin Building', 'floor': '1st Floor'},
        ]
        
        for loc_data in locations_data:
            location, created = Location.objects.get_or_create(
                name=loc_data['name'],
                defaults=loc_data
            )
            if created:
                self.stdout.write(f'Created location: {location.name}')
        
        # Create vouchers if they don't exist
        vouchers_data = [
            {
                'name': 'Canteen Voucher - $5',
                'description': 'Get $5 off your next meal at the campus canteen',
                'voucher_type': 'canteen',
                'coin_cost': 50,
                'value': Decimal('5.00')
            },
            {
                'name': 'Cafe Voucher - $3',
                'description': 'Enjoy a $3 discount at the campus cafe',
                'voucher_type': 'cafe',
                'coin_cost': 30,
                'value': Decimal('3.00')
            },
            {
                'name': 'Bookstore Voucher - $10',
                'description': 'Save $10 on your next purchase at the campus bookstore',
                'voucher_type': 'bookstore',
                'coin_cost': 100,
                'value': Decimal('10.00')
            },
            {
                'name': 'Canteen Voucher - $10',
                'description': 'Get $10 off your next meal at the campus canteen',
                'voucher_type': 'canteen',
                'coin_cost': 100,
                'value': Decimal('10.00')
            },
            {
                'name': 'Cafe Voucher - $5',
                'description': 'Enjoy a $5 discount at the campus cafe',
                'voucher_type': 'cafe',
                'coin_cost': 50,
                'value': Decimal('5.00')
            },
        ]
        
        for voucher_data in vouchers_data:
            voucher, created = Voucher.objects.get_or_create(
                name=voucher_data['name'],
                defaults=voucher_data
            )
            if created:
                self.stdout.write(f'Created voucher: {voucher.name}')
        
        # Create reward coins for existing users
        users = User.objects.all()
        for user in users:
            reward_coins, created = RewardCoin.objects.get_or_create(user=user)
            if created:
                # Give some initial coins to new users
                reward_coins.add_coins(100, "Welcome bonus")
                self.stdout.write(f'Created reward coins for user: {user.email}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated initial data!')) 