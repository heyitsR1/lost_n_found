from django.core.management.base import BaseCommand
from core.models import NotificationTemplate

class Command(BaseCommand):
    help = 'Fix all email template issues comprehensively'

    def handle(self, *args, **options):
        self.stdout.write('Fixing all email template issues...')
        
        # Define fixes for each template type
        fixes = {
            'item_found': {
                'subject': 'New Found Item: {item.title}',
                'html_template': '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>New Found Item</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #007bff;">🔍 New Found Item Posted</h2>
        <p>Hello {user.first_name},</p>
        <p>Your found item has been successfully posted to the Lost & Found system.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0;">Item Details:</h3>
            <p><strong>Title:</strong> {item.title}</p>
            <p><strong>Description:</strong> {item.description}</p>
            <p><strong>Category:</strong> {item.category.name}</p>
            <p><strong>Location:</strong> {item.location.get_full_location}</p>
            <p><strong>Posted:</strong> {item.created_at}</p>
        </div>
        
        <p>This item is now visible to all users. If someone claims it, you'll be notified immediately.</p>
        
        <p>Thank you for helping maintain our Lost & Found system!</p>
        <p>Best regards,<br>Lost & Found Team</p>
    </div>
</body>
</html>''',
                'text_template': '''New Found Item Posted

Hello {user.first_name},

Your found item has been successfully posted to the Lost & Found system.

Item Details:
- Title: {item.title}
- Description: {item.description}
- Category: {item.category.name}
- Location: {item.location.get_full_location}
- Posted: {item.created_at}

This item is now visible to all users. If someone claims it, you'll be notified immediately.

Thank you for helping maintain our Lost & Found system!

Best regards,
Lost & Found Team'''
            },
            'item_claimed': {
                'subject': 'Item Claimed: {item.title}',
                'html_template': '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Item Claimed</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #28a745;">✅ Item Claimed Successfully</h2>
        <p>Hello {user.first_name},</p>
        <p>Great news! Your item has been claimed.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0;">Item Details:</h3>
            <p><strong>Title:</strong> {item.title}</p>
            <p><strong>Description:</strong> {item.description}</p>
            <p><strong>Status:</strong> Claimed</p>
        </div>
        
        <p>Your item has been successfully returned to its owner. Thank you for your contribution!</p>
        
        <p>Best regards,<br>Lost & Found Team</p>
    </div>
</body>
</html>''',
                'text_template': '''Item Claimed Successfully

Hello {user.first_name},

Great news! Your item has been claimed.

Item Details:
- Title: {item.title}
- Description: {item.description}
- Status: Claimed

Your item has been successfully returned to its owner. Thank you for your contribution!

Best regards,
Lost & Found Team'''
            },
            'item_verified': {
                'subject': 'Item Verified: {item.title}',
                'html_template': '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Item Verified</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #28a745;">✅ Item Verified by Admin</h2>
        <p>Hello {user.first_name},</p>
        <p>Your item has been verified by our admin team and is now visible to all users.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0;">Item Details:</h3>
            <p><strong>Title:</strong> {item.title}</p>
            <p><strong>Description:</strong> {item.description}</p>
            <p><strong>Status:</strong> Verified</p>
        </div>
        
        <p>Your item is now searchable and can be found by users looking for it.</p>
        
        <p>Best regards,<br>Lost & Found Team</p>
    </div>
</body>
</html>''',
                'text_template': '''Item Verified by Admin

Hello {user.first_name},

Your item has been verified by our admin team and is now visible to all users.

Item Details:
- Title: {item.title}
- Description: {item.description}
- Status: Verified

Your item is now searchable and can be found by users looking for it.

Best regards,
Lost & Found Team'''
            }
        }
        
        fixed_count = 0
        for template_type, fix_data in fixes.items():
            try:
                template = NotificationTemplate.objects.get(template_type=template_type)
                template.subject = fix_data['subject']
                template.html_template = fix_data['html_template']
                template.text_template = fix_data['text_template']
                template.save()
                fixed_count += 1
                self.stdout.write(f'  - Fixed {template_type}')
            except NotificationTemplate.DoesNotExist:
                self.stdout.write(f'  - Template {template_type} not found')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully fixed {fixed_count} email templates!'
            )
        )

