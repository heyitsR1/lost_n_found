from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.services import EmailService, NotificationService
from core.models import NotificationTemplate

User = get_user_model()


class Command(BaseCommand):
    help = 'Test the email notification system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test email to'
        )
        parser.add_argument(
            '--admin-alert',
            action='store_true',
            help='Send test admin alert'
        )
        parser.add_argument(
            '--notification',
            action='store_true',
            help='Create test notification'
        )

    def handle(self, *args, **options):
        if options['email']:
            self.test_single_email(options['email'])
        
        if options['admin_alert']:
            self.test_admin_alert()
        
        if options['notification']:
            self.test_notification()
        
        if not any([options['email'], options['admin_alert'], options['notification']]):
            self.stdout.write(
                self.style.WARNING(
                    'No test type specified. Use --email, --admin-alert, or --notification'
                )
            )

    def test_single_email(self, email):
        """Test sending a single email"""
        self.stdout.write(f'Testing single email to: {email}')
        
        subject = 'Test Email - Lost & Found System'
        message = '''
        This is a test email from the Lost & Found notification system.
        
        If you receive this email, the email configuration is working correctly.
        
        Best regards,
        Lost & Found Team
        '''
        
        html_message = '''
        <html>
        <body>
            <h2>Test Email - Lost & Found System</h2>
            <p>This is a test email from the Lost & Found notification system.</p>
            <p>If you receive this email, the email configuration is working correctly.</p>
            <hr>
            <p><strong>Best regards,</strong><br>Lost & Found Team</p>
        </body>
        </html>
        '''
        
        try:
            success = EmailService.send_system_email(
                subject=subject,
                message=message,
                recipients=[email],
                html_message=html_message
            )
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f'Test email sent successfully to {email}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Failed to send test email to {email}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending test email: {e}')
            )

    def test_admin_alert(self):
        """Test sending admin alert"""
        self.stdout.write('Testing admin alert...')
        
        subject = 'Test Admin Alert - Lost & Found System'
        message = '''
        This is a test admin alert from the Lost & Found notification system.
        
        All admin users should receive this email.
        
        Best regards,
        Lost & Found System
        '''
        
        try:
            success = EmailService.send_admin_alert(subject, message)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS('Test admin alert sent successfully')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('Failed to send test admin alert')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending test admin alert: {e}')
            )

    def test_notification(self):
        """Test creating a test notification"""
        self.stdout.write('Testing notification creation...')
        
        try:
            # Get first user for testing
            user = User.objects.first()
            if not user:
                self.stdout.write(
                    self.style.ERROR('No users found in database. Please create a user first.')
                )
                return
            
            # Create test notification
            notification = NotificationService.create_notification(
                notification_type='system_alert',
                title='Test Notification',
                message='This is a test notification to verify the system is working.',
                recipient=user,
                priority='medium'
            )
            
            if notification:
                self.stdout.write(
                    self.style.SUCCESS(f'Test notification created successfully: {notification.id}')
                )
                
                # Check if email was sent
                if notification.is_sent:
                    self.stdout.write(
                        self.style.SUCCESS('Test notification email sent successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('Test notification created but email not sent')
                    )
            else:
                self.stdout.write(
                    self.style.ERROR('Failed to create test notification')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating test notification: {e}')
            )

    def check_email_templates(self):
        """Check if email templates are set up"""
        self.stdout.write('Checking email templates...')
        
        templates = NotificationTemplate.objects.filter(is_active=True)
        
        if templates.exists():
            self.stdout.write(
                self.style.SUCCESS(f'Found {templates.count()} active email templates')
            )
            for template in templates:
                self.stdout.write(f'  - {template.template_type}')
        else:
            self.stdout.write(
                self.style.WARNING('No active email templates found. Run setup_notification_templates first.')
            )


