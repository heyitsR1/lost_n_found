from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

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
    is_urgent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.get_item_type_display()}: {self.title}"
    
    def get_absolute_url(self):
        return reverse('core:item_detail', kwargs={'pk': self.pk})
    
    @property
    def is_expired(self):
        # Items expire after 30 days
        return self.created_at < timezone.now() - timedelta(days=30)

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
