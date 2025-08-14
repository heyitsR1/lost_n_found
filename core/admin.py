from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Location, Item, ItemImage, Contact, AdsBanner


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color_display', 'item_count']
    search_fields = ['name']
    list_filter = ['name']
    
    def color_display(self, obj):
        return format_html(
            '<span style="color: {};">■</span> {}',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Color'
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'building', 'floor', 'room', 'item_count']
    search_fields = ['name', 'building', 'room']
    list_filter = ['building']
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    fields = ['image', 'caption', 'is_primary']


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0
    readonly_fields = ['created_at']
    fields = ['name', 'email', 'phone', 'message', 'is_responded', 'created_at']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'item_type', 'status', 'category', 'location', 
        'user', 'created_at', 'is_urgent_display'
    ]
    list_filter = [
        'item_type', 'status', 'category', 'location', 
        'is_urgent', 'created_at'
    ]
    search_fields = ['title', 'description', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'claimed_at']
    date_hierarchy = 'created_at'
    inlines = [ItemImageInline, ContactInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'item_type', 'status')
        }),
        ('Categories & Location', {
            'fields': ('category', 'location')
        }),
        ('Contact Information', {
            'fields': ('contact_name', 'contact_email', 'contact_phone')
        }),
        ('Additional Details', {
            'fields': ('reward', 'is_urgent')
        }),
        ('User & Timestamps', {
            'fields': ('user', 'created_at', 'updated_at', 'claimed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_urgent_display(self, obj):
        if obj.is_urgent:
            return format_html('<span style="color: red;">⚠️ URGENT</span>')
        return ''
    is_urgent_display.short_description = 'Urgent'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'category', 'location', 'user'
        )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'item_title', 'created_at', 'is_responded']
    list_filter = ['is_responded', 'created_at']
    search_fields = ['name', 'email', 'message', 'item__title']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def item_title(self, obj):
        return obj.item.title
    item_title.short_description = 'Item'
    item_title.admin_order_field = 'item__title'


@admin.register(AdsBanner)
class AdsBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'banner_type', 'sponsor', 'is_active', 'start_date', 'end_date', 'priority', 'is_current_display']
    list_filter = ['banner_type', 'is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description', 'sponsor']
    readonly_fields = ['created_at']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Banner Information', {
            'fields': ('title', 'description', 'banner_type', 'sponsor')
        }),
        ('Display Settings', {
            'fields': ('image', 'url')
        }),
        ('Visibility Settings', {
            'fields': ('is_active', 'start_date', 'end_date', 'priority')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def is_current_display(self, obj):
        if obj.is_current:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: red;">✗ Inactive</span>')
    is_current_display.short_description = 'Current Status'
