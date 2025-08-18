from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class AdsBanner(models.Model):
    BANNER_TYPES = [
        ('sponsor', 'Sponsor'),
        ('event', 'Event'),
        ('announcement', 'Announcement'),
        ('club', 'Club'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    banner_type = models.CharField(max_length=20, choices=BANNER_TYPES, default='sponsor')
    image = models.ImageField(upload_to='banners/', blank=True, null=True)
    url = models.URLField(blank=True)
    sponsor = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    priority = models.PositiveSmallIntegerField(default=0, help_text="Higher number means higher priority")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-priority', '-start_date']
        verbose_name = 'Advertisement Banner'
        verbose_name_plural = 'Advertisement Banners'
    
    def __str__(self):
        return self.title
    
    @property
    def is_current(self):
        today = timezone.now().date()
        if not self.is_active:
            return False
        if self.end_date and self.end_date < today:
            return False
        return True

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='tag')
    color = models.CharField(max_length=7, default='#007bff')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Location(models.Model):
    LOCATION_TYPES = [
        ('parking', 'Parking Space'),
        ('ground_floor', 'Ground Floor'),
        ('first_floor', 'First Floor'),
        ('second_floor', 'Second Floor'),
        ('third_floor', 'Third Floor'),
        ('fourth_floor', 'Fourth Floor'),
        ('fifth_floor', 'Fifth Floor'),
        ('sixth_floor', 'Sixth Floor'),
        ('seventh_floor', 'Seventh Floor'),
    ]
    
    FLOOR_AREAS = [
        # Ground Floor
        ('library', 'Library'),
        ('it_lab', 'IT Lab'),
        ('kafe_kodes', 'Kafe Kodes'),
        ('bathroom', 'Bathroom'),
        
        # First Floor (Admin Section)
        ('admin_section', 'Admin Section'),
        ('academic_support', 'Academic Support'),
        ('found_items_drop', 'Found Items Drop-off'),
        ('items_claim', 'Items Claim Center'),
        
        # Class Floors (2nd-5th)
        ('class_201', 'Class 201'),
        ('class_202', 'Class 202'),
        ('class_203', 'Class 203'),
        ('class_204', 'Class 204'),
        ('class_301', 'Class 301'),
        ('class_302', 'Class 302'),
        ('class_303', 'Class 303'),
        ('class_304', 'Class 304'),
        ('class_401', 'Class 401'),
        ('class_402', 'Class 402'),
        ('class_403', 'Class 403'),
        ('class_404', 'Class 404'),
        ('class_501', 'Class 501'),
        ('class_502', 'Class 502'),
        ('class_503', 'Class 503'),
        ('class_504', 'Class 504'),
        
        # Sixth Floor
        ('program_hall', 'Program Hall'),
        ('dolab', 'DoLab'),
        ('cipl', 'CIPL'),
        ('table_tennis', 'Table Tennis Board'),
        
        # Seventh Floor
        ('canteen', 'Canteen'),
        
        # Club Rooms
        ('tech_club', 'Tech Club'),
        ('finance_club', 'Finance Club'),
        ('social_club', 'Social Club'),
        ('athletics_club', 'Athletics Club'),
        ('literature_club', 'Literature Club'),
        ('skillbee_club', 'SkillBee Club'),
        
        # Other
        ('other', 'Other Location'),
    ]
    
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES, default='other')
    floor_area = models.CharField(max_length=20, choices=FLOOR_AREAS, default='other')
    specific_location = models.CharField(max_length=200, blank=True, help_text="Specific details like 'near entrance', 'back corner', etc.")
    
    def __str__(self):
        if self.specific_location:
            return f"{self.get_location_type_display()} - {self.get_floor_area_display()} - {self.specific_location}"
        return f"{self.get_location_type_display()} - {self.get_floor_area_display()}"
    
    def get_full_location(self):
        """Get the complete location string"""
        if self.specific_location:
            return f"{self.get_location_type_display()} - {self.get_floor_area_display()} - {self.specific_location}"
        return f"{self.get_location_type_display()} - {self.get_floor_area_display()}"
    
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

class RewardCoin(models.Model):
    """Reward coin system for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reward_coins')
    coins = models.PositiveIntegerField(default=0, help_text="Number of reward coins")
    total_earned = models.PositiveIntegerField(default=0, help_text="Total coins earned")
    total_spent = models.PositiveIntegerField(default=0, help_text="Total coins spent")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.coins} coins"
    
    def add_coins(self, amount, reason="Earned"):
        """Add coins to user's balance"""
        self.coins += amount
        self.total_earned += amount
        self.save()
        CoinTransaction.objects.create(
            user=self.user,
            amount=amount,
            transaction_type='earned',
            reason=reason
        )
    
    def spend_coins(self, amount, reason="Spent"):
        """Spend coins from user's balance"""
        if self.coins >= amount:
            self.coins -= amount
            self.total_spent += amount
            self.save()
            CoinTransaction.objects.create(
                user=self.user,
                amount=amount,
                transaction_type='spent',
                reason=reason
            )
            return True
        return False

class CoinTransaction(models.Model):
    """Track coin transactions"""
    TRANSACTION_TYPES = [
        ('earned', 'Earned'),
        ('spent', 'Spent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coin_transactions')
    amount = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.transaction_type} {self.amount} coins"

class Voucher(models.Model):
    """Vouchers that can be redeemed with coins"""
    VOUCHER_TYPES = [
        ('canteen', 'Canteen'),
        ('cafe', 'Cafe'),
        ('bookstore', 'Bookstore'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    voucher_type = models.CharField(max_length=20, choices=VOUCHER_TYPES)
    coin_cost = models.PositiveIntegerField(help_text="Number of coins required")
    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monetary value of voucher")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.coin_cost} coins"
    
    class Meta:
        ordering = ['coin_cost']

class VoucherRedemption(models.Model):
    """Track voucher redemptions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voucher_redemptions')
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.voucher.name}"
    
    class Meta:
        ordering = ['-redeemed_at']

class Item(models.Model):
    ITEM_TYPES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('claimed', 'Claimed'),
        ('expired', 'Expired'),
        ('closed', 'Closed'),
        ('pending_verification', 'Pending Admin Verification'),
        ('verified', 'Admin Verified'),
        ('dropped_off', 'Dropped at Admin Section'),
        ('ready_for_claim', 'Ready for Claim at Admin Section'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='active')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    # Contact information (for found items)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # User who posted the item
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    claimed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional fields
    reward = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reward_coins = models.PositiveIntegerField(default=0, help_text="Reward in coins")
    is_urgent = models.BooleanField(default=False)
    
    # Admin verification fields
    admin_verified = models.BooleanField(default=False, help_text="Item verified by admin in person")
    admin_verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_items')
    admin_verified_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, help_text="Admin notes about the item")
    
    # Drop-off and claim fields
    dropped_at_admin = models.BooleanField(default=False, help_text="Item physically dropped at admin section")
    dropped_at_admin_date = models.DateTimeField(null=True, blank=True)
    claimed_from_admin = models.BooleanField(default=False, help_text="Item claimed from admin section")
    claimed_from_admin_date = models.DateTimeField(null=True, blank=True)
    claimer_name = models.CharField(max_length=100, blank=True, help_text="Name of person claiming the item")
    claimer_id_verified = models.BooleanField(default=False, help_text="Claimer's ID verified by admin")
    
    def __str__(self):
        return f"{self.get_item_type_display()}: {self.title}"
    
    def get_absolute_url(self):
        return reverse('core:item_detail', kwargs={'pk': self.pk})
    
    @property
    def is_expired(self):
        # Items expire after 30 days
        return self.created_at < timezone.now() - timedelta(days=30)
    
    def save(self, *args, **kwargs):
        # If this is a new item and has a reward, give coins to the user
        if not self.pk and self.reward_coins > 0:
            super().save(*args, **kwargs)
            # Give coins to the user who posted the found item
            if self.item_type == 'found':
                reward_coins, created = RewardCoin.objects.get_or_create(user=self.user)
                reward_coins.add_coins(self.reward_coins, f"Reward for posting found item: {self.title}")
        else:
            super().save(*args, **kwargs)

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='item_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Ensure only one primary image per item
        if self.is_primary:
            ItemImage.objects.filter(item=self.item, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Image for {self.item.title}"

class AdminOperation(models.Model):
    """Track admin operations on items"""
    OPERATION_TYPES = [
        ('verify', 'Verify Item'),
        ('drop_off', 'Mark as Dropped Off'),
        ('claim', 'Process Claim'),
        ('update_status', 'Update Status'),
        ('add_note', 'Add Note'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='admin_operations')
    operation_type = models.CharField(max_length=20, choices=OPERATION_TYPES)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_operations')
    operation_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    previous_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.get_operation_type_display()} on {self.item.title} by {self.admin_user.get_full_name()}"
    
    class Meta:
        ordering = ['-operation_date']
        verbose_name = 'Admin Operation'
        verbose_name_plural = 'Admin Operations'

class Contact(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Contact from {self.name} for {self.item.title}"


class Notification(models.Model):
    """System notifications for users and admins"""
    NOTIFICATION_TYPES = [
        ('item_found', 'Item Found'),
        ('item_claimed', 'Item Claimed'),
        ('item_verified', 'Item Admin Verified'),
        ('item_dropped_off', 'Item Dropped at Admin'),
        ('item_ready_claim', 'Item Ready for Claim'),
        ('admin_action', 'Admin Action Required'),
        ('system_alert', 'System Alert'),
        ('reward_earned', 'Reward Earned'),
        ('contact_received', 'New Contact Message'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    notification_type = models.CharField(max_length=25, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    
    # Recipients
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    is_admin_notification = models.BooleanField(default=False, help_text="If True, all admins will receive this notification")
    
    # Related objects
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    admin_operation = models.ForeignKey(AdminOperation, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    
    # Status tracking
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False, help_text="Email sent successfully")
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.get_notification_type_display()}: {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.save(update_fields=['is_read', 'updated_at'])
    
    def mark_as_sent(self):
        """Mark notification as sent via email"""
        self.is_sent = True
        self.sent_at = timezone.now()
        self.save(update_fields=['is_sent', 'sent_at', 'updated_at'])
    
    @property
    def is_urgent(self):
        """Check if notification is urgent based on priority and type"""
        return (self.priority == 'urgent' or 
                self.notification_type in ['item_found', 'admin_action'] or
                (self.item and self.item.is_urgent))


class NotificationTemplate(models.Model):
    """Email templates for different notification types"""
    TEMPLATE_TYPES = [
        ('item_found', 'Item Found'),
        ('item_claimed', 'Item Claimed'),
        ('item_verified', 'Item Admin Verified'),
        ('item_dropped_off', 'Item Dropped at Admin'),
        ('item_ready_claim', 'Item Ready for Claim'),
        ('admin_action', 'Admin Action Required'),
        ('system_alert', 'System Alert'),
        ('reward_earned', 'Reward Earned'),
        ('contact_received', 'New Contact Message'),
    ]
    
    template_type = models.CharField(max_length=25, choices=TEMPLATE_TYPES, unique=True)
    subject = models.CharField(max_length=200)
    html_template = models.TextField(help_text="HTML email template with placeholders")
    text_template = models.TextField(help_text="Plain text email template with placeholders")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['template_type']
        verbose_name = 'Notification Template'
        verbose_name_plural = 'Notification Templates'
    
    def __str__(self):
        return f"{self.get_template_type_display()} Template"
    
    def get_subject(self, context=None):
        """Get subject with context variables replaced"""
        if not context:
            return self.subject
        return self.subject.format(**context)
    
    def get_html_content(self, context=None):
        """Get HTML content with context variables replaced"""
        if not context:
            return self.html_template
        return self.html_template.format(**context)
    
    def get_text_content(self, context=None):
        """Get text content with context variables replaced"""
        if not context:
            return self.text_template
        return self.text_template.format(**context)
