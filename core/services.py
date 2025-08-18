import logging
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Notification, NotificationTemplate

User = get_user_model()
logger = logging.getLogger(__name__)


class NotificationService:
    """Service class for handling notifications and emails"""
    
    @staticmethod
    def create_notification(
        notification_type,
        title,
        message,
        recipient=None,
        is_admin_notification=False,
        item=None,
        admin_operation=None,
        priority='medium'
    ):
        """Create a notification and optionally send email"""
        try:
            notification = Notification.objects.create(
                notification_type=notification_type,
                title=title,
                message=message,
                recipient=recipient,
                is_admin_notification=is_admin_notification,
                item=item,
                admin_operation=admin_operation,
                priority=priority
            )
            
            # Send email notification
            if recipient or is_admin_notification:
                NotificationService.send_email_notification(notification)
            
            return notification
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            return None
    
    @staticmethod
    def send_email_notification(notification):
        """Send email for a notification"""
        try:
            # Get template
            template = NotificationTemplate.objects.filter(
                template_type=notification.notification_type,
                is_active=True
            ).first()
            
            if not template:
                logger.warning(f"No email template found for {notification.notification_type}")
                return False
            
            # Determine recipients
            recipients = []
            if notification.recipient:
                recipients.append(notification.recipient.email)
            elif notification.is_admin_notification:
                # Get all admin users
                admin_users = User.objects.filter(is_staff=True, is_active=True)
                recipients = [user.email for user in admin_users if user.email]
            
            if not recipients:
                logger.warning(f"No recipients found for notification {notification.id}")
                return False
            
            # Prepare context
            context = {
                'notification': notification,
                'item': notification.item,
                'user': notification.recipient or notification.item.user if notification.item else None,
                'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
            }
            
            # Get email content
            subject = template.get_subject(context)
            html_content = template.get_html_content(context)
            text_content = template.get_text_content(context)
            
            # Send email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipients
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            
            # Mark as sent
            notification.mark_as_sent()
            
            logger.info(f"Email sent successfully for notification {notification.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email for notification {notification.id}: {e}")
            return False
    
    @staticmethod
    def notify_item_found(item):
        """Notify when a new item is found"""
        title = f"New Found Item: {item.title}"
        message = f"A new item '{item.title}' has been found and posted to the Lost & Found system."
        
        # Notify all admins
        NotificationService.create_notification(
            notification_type='item_found',
            title=title,
            message=message,
            is_admin_notification=True,
            item=item,
            priority='high'
        )
        
        # Notify the user who posted
        if item.user:
            NotificationService.create_notification(
                notification_type='item_found',
                title=f"Your Found Item Posted: {item.title}",
                message=f"Your found item '{item.title}' has been successfully posted to the Lost & Found system.",
                recipient=item.user,
                item=item,
                priority='medium'
            )
    
    @staticmethod
    def notify_item_claimed(item, claimer_name):
        """Notify when an item is claimed"""
        title = f"Item Claimed: {item.title}"
        message = f"The item '{item.title}' has been claimed by {claimer_name}."
        
        # Notify the user who posted the item
        if item.user:
            NotificationService.create_notification(
                notification_type='item_claimed',
                title=title,
                message=message,
                recipient=item.user,
                item=item,
                priority='medium'
            )
        
        # Notify admins
        NotificationService.create_notification(
            notification_type='item_claimed',
            title=title,
            message=message,
            is_admin_notification=True,
            item=item,
            priority='medium'
        )
    
    @staticmethod
    def notify_item_verified(item, admin_user):
        """Notify when an item is verified by admin"""
        title = f"Item Verified: {item.title}"
        message = f"Your item '{item.title}' has been verified by admin {admin_user.get_full_name()}."
        
        # Notify the user who posted the item
        if item.user:
            NotificationService.create_notification(
                notification_type='item_verified',
                title=title,
                message=message,
                recipient=item.user,
                item=item,
                priority='medium'
            )
    
    @staticmethod
    def notify_item_dropped_off(item):
        """Notify when an item is dropped off at admin section"""
        title = f"Item Dropped Off: {item.title}"
        message = f"The item '{item.title}' has been dropped off at the admin section and is ready for verification."
        
        # Notify all admins
        NotificationService.create_notification(
            notification_type='item_dropped_off',
            title=title,
            message=message,
            is_admin_notification=True,
            item=item,
            priority='high'
        )
    
    @staticmethod
    def notify_item_ready_claim(item):
        """Notify when an item is ready for claim"""
        title = f"Item Ready for Claim: {item.title}"
        message = f"The item '{item.title}' has been verified and is ready for claim at the admin section."
        
        # Notify the user who posted the item
        if item.user:
            NotificationService.create_notification(
                notification_type='item_ready_claim',
                title=title,
                message=message,
                recipient=item.user,
                item=item,
                priority='medium'
            )
    
    @staticmethod
    def notify_admin_action_required(item, action_type):
        """Notify admins when action is required"""
        title = f"Admin Action Required: {item.title}"
        message = f"Action required for item '{item.title}': {action_type}"
        
        NotificationService.create_notification(
            notification_type='admin_action',
            title=title,
            message=message,
            is_admin_notification=True,
            item=item,
            priority='high'
        )
    
    @staticmethod
    def notify_reward_earned(user, amount, reason):
        """Notify when user earns reward coins"""
        title = f"Reward Earned: {amount} coins"
        message = f"You have earned {amount} reward coins for: {reason}"
        
        NotificationService.create_notification(
            notification_type='reward_earned',
            title=title,
            message=message,
            recipient=user,
            priority='medium'
        )
    
    @staticmethod
    def notify_contact_received(contact):
        """Notify when a new contact message is received"""
        title = f"New Contact Message for: {contact.item.title}"
        message = f"New message from {contact.name} regarding item '{contact.item.title}': {contact.message[:100]}..."
        
        # Notify the item owner
        if contact.item.user:
            NotificationService.create_notification(
                notification_type='contact_received',
                title=title,
                message=message,
                recipient=contact.item.user,
                item=contact.item,
                priority='medium'
            )
        
        # Notify admins
        NotificationService.create_notification(
            notification_type='contact_received',
            title=title,
            message=message,
            is_admin_notification=True,
            item=contact.item,
            priority='medium'
        )


class EmailService:
    """Service class for handling email operations"""
    
    @staticmethod
    def send_system_email(subject, message, recipients, html_message=None):
        """Send a system email"""
        try:
            if html_message:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=recipients
                )
                email.attach_alternative(html_message, "text/html")
                email.send()
            else:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipients,
                    fail_silently=False
                )
            return True
        except Exception as e:
            logger.error(f"Error sending system email: {e}")
            return False
    
    @staticmethod
    def send_admin_alert(subject, message, priority='medium'):
        """Send alert to all admin users"""
        try:
            admin_users = User.objects.filter(is_staff=True, is_active=True)
            admin_emails = [user.email for user in admin_users if user.email]
            
            if admin_emails:
                return EmailService.send_system_email(subject, message, admin_emails)
            return False
        except Exception as e:
            logger.error(f"Error sending admin alert: {e}")
            return False

