from django.core.management.base import BaseCommand
from core.models import Item, ItemImage
import os

class Command(BaseCommand):
    help = 'Associate existing images with items'

    def handle(self, *args, **options):
        self.stdout.write('Associating existing images with items...')
        
        # Get all items
        items = Item.objects.all()
        if not items:
            self.stdout.write('No items found. Please run repopulate_items_kings_college first.')
            return
        
        # Get existing images from media folder
        media_path = 'media/item_images/'
        if not os.path.exists(media_path):
            self.stdout.write('Media folder not found.')
            return
        
        image_files = [f for f in os.listdir(media_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        if not image_files:
            self.stdout.write('No image files found in media folder.')
            return
        
        self.stdout.write(f'Found {len(image_files)} image files.')
        
        # Associate images with items
        for i, item in enumerate(items):
            if i < len(image_files):
                image_file = image_files[i]
                image_path = f'item_images/{image_file}'
                
                # Create ItemImage object
                item_image = ItemImage.objects.create(
                    item=item,
                    image=image_path,
                    caption=f'Image for {item.title}',
                    is_primary=(i == 0)  # First image is primary
                )
                
                self.stdout.write(f'  - Associated {image_file} with {item.title}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully associated images with {min(len(items), len(image_files))} items!'
            )
        )
