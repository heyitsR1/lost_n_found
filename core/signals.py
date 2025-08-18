from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Item, Contact, AdminOperation, Notification
from .services import NotificationService

User = get_user_model()


@receiver(post_save, sender=Item)
def notify_item_events(sender, instance, created, **kwargs):
    """Handle notifications for item events"""
    if created:
        # New item created
        if instance.item_type == 'found':
            NotificationService.notify_item_found(instance)
    else:
        # Item updated
        if instance.status == 'claimed' and not instance.claimed_from_admin:
            # Item claimed online
            claimer_name = getattr(instance, 'claimer_name', 'Unknown User')
            NotificationService.notify_item_claimed(instance, claimer_name)
        
        elif instance.status == 'verified' and instance.admin_verified:
            # Item verified by admin
            admin_user = instance.admin_verified_by
            if admin_user:
                NotificationService.notify_item_verified(instance, admin_user)
        
        elif instance.dropped_at_admin and not instance._state.adding:
            # Item dropped off at admin
            NotificationService.notify_item_dropped_off(instance)
        
        elif instance.status == 'ready_for_claim':
            # Item ready for claim
            NotificationService.notify_item_ready_claim(instance)


@receiver(post_save, sender=Contact)
def notify_contact_received(sender, instance, created, **kwargs):
    """Handle notifications for new contact messages"""
    if created:
        NotificationService.notify_contact_received(instance)


@receiver(post_save, sender=AdminOperation)
def notify_admin_operations(sender, instance, created, **kwargs):
    """Handle notifications for admin operations"""
    if created:
        # Notify when admin action is required
        if instance.operation_type in ['verify', 'drop_off', 'claim']:
            action_type = instance.get_operation_type_display()
            NotificationService.notify_admin_action_required(
                instance.item, 
                action_type
            )


@receiver(post_save, sender=User)
def create_reward_coins_for_new_user(sender, instance, created, **kwargs):
    """Create reward coins for new users"""
    if created:
        from .models import RewardCoin
        RewardCoin.objects.get_or_create(user=instance)


# Import signals in apps.py to ensure they are loaded
def ready():
    """Import signals when app is ready"""
    pass


