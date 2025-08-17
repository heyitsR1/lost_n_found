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
    name = models.CharField(max_length=200)
    building = models.CharField(max_length=100, blank=True)
    floor = models.CharField(max_length=20, blank=True)
    room = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        if self.building:
            return f"{self.name} - {self.building}"
        return self.name

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
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
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
