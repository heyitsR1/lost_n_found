from django.core.management.base import BaseCommand
from core.models import NotificationTemplate


class Command(BaseCommand):
    help = 'Set up default notification email templates'

    def handle(self, *args, **options):
        templates_data = [
            {
                'template_type': 'item_found',
                'subject': 'New Found Item: {item.title}',
                'html_template': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>New Found Item</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #007bff;">🔍 New Found Item Posted</h2>
                        <p>Hello {user.first_name or 'there'},</p>
                        <p>Your found item has been successfully posted to the Lost & Found system.</p>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="margin-top: 0;">Item Details:</h3>
                            <p><strong>Title:</strong> {item.title}</p>
                            <p><strong>Description:</strong> {item.description}</p>
                            <p><strong>Category:</strong> {item.category.name}</p>
                            <p><strong>Location:</strong> {item.location.get_full_location()}</p>
                            <p><strong>Posted:</strong> {item.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                        </div>
                        
                        <p>This item is now visible to all users. If someone claims it, you'll be notified immediately.</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{site_url}{item.get_absolute_url()}" 
                               style="background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                                View Item Details
                            </a>
                        </div>
                        
                        <p>Thank you for helping maintain our Lost & Found system!</p>
                        <p>Best regards,<br>Lost & Found Team</p>
                    </div>
                </body>
                </html>
                ''',
                'text_template': '''
                New Found Item Posted

                Hello {user.first_name or 'there'},

                Your found item has been successfully posted to the Lost & Found system.

                Item Details:
                - Title: {item.title}
                - Description: {item.description}
                - Category: {item.category.name}
                - Location: {item.location.get_full_location()}
                - Posted: {item.created_at.strftime('%B %d, %Y at %I:%M %p')}

                This item is now visible to all users. If someone claims it, you'll be notified immediately.

                View item details: {site_url}{item.get_absolute_url()}

                Thank you for helping maintain our Lost & Found system!

                Best regards,
                Lost & Found Team
                '''
            },
            {
                'template_type': 'item_claimed',
                'subject': 'Item Claimed: {item.title}',
                'html_template': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Item Claimed</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #28a745;">✅ Item Successfully Claimed</h2>
                        <p>Hello {user.first_name or 'there'},</p>
                        <p>Great news! Your found item has been claimed by someone.</p>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="margin-top: 0;">Item Details:</h3>
                            <p><strong>Title:</strong> {item.title}</p>
                            <p><strong>Description:</strong> {item.description}</p>
                            <p><strong>Category:</strong> {item.category.name}</p>
                            <p><strong>Claimed:</strong> {item.claimed_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                        </div>
                        
                        <p>The item has been marked as claimed and is no longer visible to other users.</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{site_url}{item.get_absolute_url()}" 
                               style="background: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                                View Item Details
                            </a>
                        </div>
                        
                        <p>Thank you for helping reunite someone with their lost item!</p>
                        <p>Best regards,<br>Lost & Found Team</p>
                    </div>
                </body>
                </html>
                ''',
                'text_template': '''
                Item Successfully Claimed

                Hello {user.first_name or 'there'},

                Great news! Your found item has been claimed by someone.

                Item Details:
                - Title: {item.title}
                - Description: {item.description}
                - Category: {item.category.name}
                - Claimed: {item.claimed_at.strftime('%B %d, %Y at %I:%M %p')}

                The item has been marked as claimed and is no longer visible to other users.

                View item details: {site_url}{item.get_absolute_url()}

                Thank you for helping reunite someone with their lost item!

                Best regards,
                Lost & Found Team
                '''
            },
            {
                'template_type': 'item_verified',
                'subject': 'Item Verified: {item.title}',
                'html_template': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Item Verified</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #17a2b8;">🔒 Item Admin Verified</h2>
                        <p>Hello {user.first_name or 'there'},</p>
                        <p>Your found item has been verified by our admin team and is now ready for the owner to claim.</p>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="margin-top: 0;">Item Details:</h3>
                            <p><strong>Title:</strong> {item.title}</p>
                            <p><strong>Description:</strong> {item.description}</p>
                            <p><strong>Category:</strong> {item.category.name}</p>
                            <p><strong>Verified by:</strong> {item.admin_verified_by.get_full_name()}</p>
                            <p><strong>Verified on:</strong> {item.admin_verified_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                        </div>
                        
                        <p>The item is now in our secure storage and will be held for the owner to claim.</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{site_url}{item.get_absolute_url()}" 
                               style="background: #17a2b8; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                                View Item Details
                            </a>
                        </div>
                        
                        <p>Thank you for your patience!</p>
                        <p>Best regards,<br>Lost & Found Team</p>
                    </div>
                </body>
                </html>
                ''',
                'text_template': '''
                Item Admin Verified

                Hello {user.first_name or 'there'},

                Your found item has been verified by our admin team and is now ready for the owner to claim.

                Item Details:
                - Title: {item.title}
                - Description: {item.description}
                - Category: {item.category.name}
                - Verified by: {item.admin_verified_by.get_full_name()}
                - Verified on: {item.admin_verified_at.strftime('%B %d, %Y at %I:%M %p')}

                The item is now in our secure storage and will be held for the owner to claim.

                View item details: {site_url}{item.get_absolute_url()}

                Thank you for your patience!

                Best regards,
                Lost & Found Team
                '''
            },
            {
                'template_type': 'item_dropped_off',
                'subject': 'Item Dropped Off: {item.title}',
                'html_template': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Item Dropped Off</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #ffc107;">📦 Item Dropped Off at Admin Section</h2>
                        <p>Hello Admin Team,</p>
                        <p>A new item has been physically dropped off at the admin section and requires verification.</p>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="margin-top: 0;">Item Details:</h3>
                            <p><strong>Title:</strong> {item.title}</p>
                            <p><strong>Description:</strong> {item.description}</p>
                            <p><strong>Category:</strong> {item.category.name}</p>
                            <p><strong>Posted by:</strong> {item.user.get_full_name()} ({item.user.email})</p>
                            <p><strong>Dropped off:</strong> {item.dropped_at_admin_date.strftime('%B %d, %Y at %I:%M %p')}</p>
                        </div>
                        
                        <p><strong>Action Required:</strong> Please verify this item in person and update its status.</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{site_url}{item.get_absolute_url()}" 
                               style="background: #ffc107; color: #333; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                                Review Item in Admin Panel
                            </a>
                        </div>
                        
                        <p>Thank you for your attention to this matter.</p>
                        <p>Best regards,<br>Lost & Found System</p>
                    </div>
                </body>
                </html>
                ''',
                'text_template': '''
                Item Dropped Off at Admin Section

                Hello Admin Team,

                A new item has been physically dropped off at the admin section and requires verification.

                Item Details:
                - Title: {item.title}
                - Description: {item.description}
                - Category: {item.category.name}
                - Posted by: {item.user.get_full_name()} ({item.user.email})
                - Dropped off: {item.dropped_at_admin_date.strftime('%B %d, %Y at %I:%M %p')}

                Action Required: Please verify this item in person and update its status.

                Review item in admin panel: {site_url}{item.get_absolute_url()}

                Thank you for your attention to this matter.

                Best regards,
                Lost & Found System
                '''
            },
            {
                'template_type': 'item_ready_claim',
                'subject': 'Item Ready for Claim: {item.title}',
                'html_template': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Item Ready for Claim</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #28a745;">🎉 Item Ready for Claim!</h2>
                        <p>Hello {user.first_name or 'there'},</p>
                        <p>Great news! Your found item has been verified and is now ready for the owner to claim.</p>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="margin-top: 0;">Item Details:</h3>
                            <p><strong>Title:</strong> {item.title}</p>
                            <p><strong>Description:</strong> {item.description}</p>
                            <p><strong>Category:</strong> {item.category.name}</p>
                            <p><strong>Status:</strong> Ready for Claim at Admin Section</p>
                        </div>
                        
                        <p><strong>Next Steps:</strong> The item owner can now visit the admin section to claim their item. You'll be notified once it's claimed.</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{site_url}{item.get_absolute_url()}" 
                               style="background: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                                View Item Details
                            </a>
                        </div>
                        
                        <p>Thank you for helping maintain our Lost & Found system!</p>
                        <p>Best regards,<br>Lost & Found Team</p>
                    </div>
                </body>
                </html>
                ''',
                'text_template': '''
                Item Ready for Claim!

                Hello {user.first_name or 'there'},

                Great news! Your found item has been verified and is now ready for the owner to claim.

                Item Details:
                - Title: {item.title}
                - Description: {item.description}
                - Category: {item.category.name}
                - Status: Ready for Claim at Admin Section

                Next Steps: The item owner can now visit the admin section to claim their item. You'll be notified once it's claimed.

                View item details: {site_url}{item.get_absolute_url()}

                Thank you for helping maintain our Lost & Found system!

                Best regards,
                Lost & Found Team
                '''
            },
            {
                'template_type': 'admin_action',
                'subject': 'Admin Action Required: {item.title}',
                'html_template': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Admin Action Required</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #dc3545;">⚠️ Admin Action Required</h2>
                        <p>Hello Admin Team,</p>
                        <p>An item requires your attention and action.</p>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="margin-top: 0;">Item Details:</h3>
                            <p><strong>Title:</strong> {item.title}</p>
                            <p><strong>Description:</strong> {item.description}</p>
                            <p><strong>Category:</strong> {item.category.name}</p>
                            <p><strong>Current Status:</strong> {item.get_status_display()}</p>
                            <p><strong>Action Required:</strong> {notification.message}</p>
                        </div>
                        
                        <p><strong>Please review this item and take appropriate action.</strong></p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{site_url}{item.get_absolute_url()}" 
                               style="background: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                                Review Item in Admin Panel
                            </a>
                        </div>
                        
                        <p>Thank you for your attention to this matter.</p>
                        <p>Best regards,<br>Lost & Found System</p>
                    </div>
                </body>
                </html>
                ''',
                'text_template': '''
                Admin Action Required

                Hello Admin Team,

                An item requires your attention and action.

                Item Details:
                - Title: {item.title}
                - Description: {item.description}
                - Category: {item.category.name}
                - Current Status: {item.get_status_display()}
                - Action Required: {notification.message}

                Please review this item and take appropriate action.

                Review item in admin panel: {site_url}{item.get_absolute_url()}

                Thank you for your attention to this matter.

                Best regards,
                Lost & Found System
                '''
            },
            {
                'template_type': 'reward_earned',
                'subject': 'Reward Earned: {amount} coins',
                'html_template': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Reward Earned</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #ffc107;">🪙 Reward Coins Earned!</h2>
                        <p>Hello {user.first_name or 'there'},</p>
                        <p>Congratulations! You have earned reward coins for your contribution.</p>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="margin-top: 0;">Reward Details:</h3>
                            <p><strong>Amount Earned:</strong> {amount} coins</p>
                            <p><strong>Reason:</strong> {reason}</p>
                            <p><strong>Current Balance:</strong> {user.reward_coins.coins} coins</p>
                        </div>
                        
                        <p>You can use these coins to redeem vouchers and rewards from our system.</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{site_url}/dashboard/" 
                               style="background: #ffc107; color: #333; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                                View Your Dashboard
                            </a>
                        </div>
                        
                        <p>Keep up the great work!</p>
                        <p>Best regards,<br>Lost & Found Team</p>
                    </div>
                </body>
                </html>
                ''',
                'text_template': '''
                Reward Coins Earned!

                Hello {user.first_name or 'there'},

                Congratulations! You have earned reward coins for your contribution.

                Reward Details:
                - Amount Earned: {amount} coins
                - Reason: {reason}
                - Current Balance: {user.reward_coins.coins} coins

                You can use these coins to redeem vouchers and rewards from our system.

                View your dashboard: {site_url}/dashboard/

                Keep up the great work!

                Best regards,
                Lost & Found Team
                '''
            },
            {
                'template_type': 'contact_received',
                'subject': 'New Contact Message for: {item.title}',
                'html_template': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>New Contact Message</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #17a2b8;">💬 New Contact Message Received</h2>
                        <p>Hello {user.first_name or 'there'},</p>
                        <p>You have received a new message regarding your item.</p>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="margin-top: 0;">Message Details:</h3>
                            <p><strong>From:</strong> {notification.item.contacts.first.name}</p>
                            <p><strong>Email:</strong> {notification.item.contacts.first.email}</p>
                            <p><strong>Phone:</strong> {notification.item.contacts.first.phone or 'Not provided'}</p>
                            <p><strong>Message:</strong> {notification.item.contacts.first.message}</p>
                        </div>
                        
                        <div style="background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="margin-top: 0;">Item Details:</h3>
                            <p><strong>Title:</strong> {item.title}</p>
                            <p><strong>Category:</strong> {item.category.name}</p>
                        </div>
                        
                        <p>Please respond to this message as soon as possible.</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{site_url}{item.get_absolute_url()}" 
                               style="background: #17a2b8; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                                View Item and Respond
                            </a>
                        </div>
                        
                        <p>Best regards,<br>Lost & Found Team</p>
                    </div>
                </body>
                </html>
                ''',
                'text_template': '''
                New Contact Message Received

                Hello {user.first_name or 'there'},

                You have received a new message regarding your item.

                Message Details:
                - From: {notification.item.contacts.first.name}
                - Email: {notification.item.contacts.first.email}
                - Phone: {notification.item.contacts.first.phone or 'Not provided'}
                - Message: {notification.item.contacts.first.message}

                Item Details:
                - Title: {item.title}
                - Category: {item.category.name}

                Please respond to this message as soon as possible.

                View item and respond: {site_url}{item.get_absolute_url()}

                Best regards,
                Lost & Found Team
                '''
            }
        ]

        created_count = 0
        updated_count = 0

        for template_data in templates_data:
            template, created = NotificationTemplate.objects.get_or_create(
                template_type=template_data['template_type'],
                defaults=template_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created template: {template.template_type}')
                )
            else:
                # Update existing template
                for key, value in template_data.items():
                    setattr(template, key, value)
                template.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated template: {template.template_type}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully set up notification templates. '
                f'Created: {created_count}, Updated: {updated_count}'
            )
        )


