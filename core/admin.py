from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Category, Location, Item, ItemImage, Contact, AdsBanner, RewardCoin, CoinTransaction, Voucher, VoucherRedemption, AdminOperation, Notification, NotificationTemplate


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
        return obj.item.title if obj.item else 'N/A'
    item_title.short_description = 'Item'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'notification_type', 'title', 'recipient_display', 'priority', 
        'is_read', 'is_sent', 'created_at'
    ]
    list_filter = [
        'notification_type', 'priority', 'is_read', 'is_sent', 
        'is_admin_notification', 'created_at'
    ]
    search_fields = ['title', 'message', 'recipient__email', 'item__title']
    readonly_fields = ['created_at', 'updated_at', 'sent_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('notification_type', 'title', 'message', 'priority')
        }),
        ('Recipients', {
            'fields': ('recipient', 'is_admin_notification')
        }),
        ('Related Objects', {
            'fields': ('item', 'admin_operation'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'is_sent', 'sent_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def recipient_display(self, obj):
        if obj.recipient:
            return obj.recipient.email
        elif obj.is_admin_notification:
            return "All Admins"
        return "None"
    recipient_display.short_description = 'Recipient'
    
    actions = ['mark_as_read', 'mark_as_unread', 'resend_email']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = "Mark selected notifications as unread"
    
    def resend_email(self, request, queryset):
        from .services import NotificationService
        sent_count = 0
        for notification in queryset:
            if NotificationService.send_email_notification(notification):
                sent_count += 1
        self.message_user(request, f'{sent_count} emails sent successfully.')
    resend_email.short_description = "Resend email for selected notifications"


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ['template_type', 'subject', 'is_active', 'created_at']
    list_filter = ['template_type', 'is_active', 'created_at']
    search_fields = ['template_type', 'subject']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('template_type', 'subject', 'is_active')
        }),
        ('Email Content', {
            'fields': ('html_template', 'text_template'),
            'description': 'Use placeholders like {user}, {item}, {site_url} in your templates.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_templates', 'deactivate_templates']
    
    def activate_templates(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} templates activated.')
    activate_templates.short_description = "Activate selected templates"
    
    def deactivate_templates(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} templates deactivated.')
    deactivate_templates.short_description = "Deactivate selected templates"


@admin.register(AdsBanner)
class AdsBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'banner_type', 'is_active', 'start_date', 'end_date', 'priority', 'is_current_display']
    list_filter = ['banner_type', 'is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description', 'sponsor']
    readonly_fields = ['created_at']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Banner Information', {
            'fields': ('title', 'description', 'banner_type')
        }),
        ('Display Settings', {
            'fields': ('image', 'url')
        }),
        ('Visibility Settings', {
            'fields': ('is_active', 'start_date', 'end_date', 'priority')
        }),
        ('Internal Information', {
            'fields': ('sponsor',),
            'classes': ('collapse',),
            'description': 'Sponsor information is for internal use only and will not be displayed to users.'
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
