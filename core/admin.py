from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Category, Location, Item, ItemImage, Contact, AdsBanner, RewardCoin, CoinTransaction, Voucher, VoucherRedemption, AdminOperation


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
    list_display = ['location_type', 'floor_area', 'specific_location', 'item_count']
    search_fields = ['location_type', 'floor_area', 'specific_location']
    list_filter = ['location_type', 'floor_area']
    
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
        'user', 'created_at', 'is_urgent_display', 'reward_coins_display', 'admin_verified_display'
    ]
    list_filter = [
        'item_type', 'status', 'category', 'location', 
        'is_urgent', 'created_at', 'admin_verified', 'dropped_at_admin'
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
            'fields': ('reward', 'reward_coins', 'is_urgent')
        }),
        ('Admin Verification', {
            'fields': ('admin_verified', 'admin_verified_by', 'admin_verified_at', 'admin_notes'),
            'classes': ('collapse',)
        }),
        ('Drop-off & Claim', {
            'fields': ('dropped_at_admin', 'dropped_at_admin_date', 'claimed_from_admin', 'claimed_from_admin_date', 'claimer_name', 'claimer_id_verified'),
            'classes': ('collapse',)
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
    
    def reward_coins_display(self, obj):
        if obj.reward_coins > 0:
            return format_html('<span style="color: gold;">🪙 {} coins</span>', obj.reward_coins)
        return ''
    reward_coins_display.short_description = 'Reward Coins'
    
    def admin_verified_display(self, obj):
        if obj.admin_verified:
            return format_html('<span style="color: green;">✓ Verified</span>')
        elif obj.dropped_at_admin:
            return format_html('<span style="color: orange;">📦 Dropped</span>')
        elif obj.status == 'pending_verification':
            return format_html('<span style="color: yellow;">⏳ Pending</span>')
        return format_html('<span style="color: red;">✗ Not Verified</span>')
    admin_verified_display.short_description = 'Admin Status'
    
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


@admin.register(RewardCoin)
class RewardCoinAdmin(admin.ModelAdmin):
    list_display = ['user', 'coins', 'total_earned', 'total_spent', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(CoinTransaction)
class CoinTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'transaction_type', 'reason', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['user__email', 'reason']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['name', 'voucher_type', 'coin_cost', 'value', 'is_active', 'created_at']
    list_filter = ['voucher_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(VoucherRedemption)
class VoucherRedemptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'voucher', 'redeemed_at', 'is_used', 'used_at']
    list_filter = ['is_used', 'redeemed_at', 'voucher__voucher_type']
    search_fields = ['user__email', 'voucher__name']
    readonly_fields = ['redeemed_at']
    date_hierarchy = 'redeemed_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'voucher')


@admin.register(AdminOperation)
class AdminOperationAdmin(admin.ModelAdmin):
    list_display = ['item', 'operation_type', 'admin_user', 'operation_date', 'status_change']
    list_filter = ['operation_type', 'operation_date', 'admin_user']
    search_fields = ['item__title', 'admin_user__email', 'notes']
    readonly_fields = ['operation_date']
    date_hierarchy = 'operation_date'
    
    def status_change(self, obj):
        if obj.previous_status and obj.new_status:
            return f"{obj.previous_status} → {obj.new_status}"
        return "-"
    status_change.short_description = 'Status Change'
