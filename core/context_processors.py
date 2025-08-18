from .models import AdsBanner
from django.utils import timezone
from django.db import models

def ads_banners_processor(request):
    """
    Context processor that adds active ads/banners to all templates
    """
    today = timezone.now().date()
    active_banners = AdsBanner.objects.filter(
        is_active=True,
        start_date__lte=today
    ).filter(
        models.Q(end_date__isnull=True) | models.Q(end_date__gte=today)
    ).order_by('-priority', '-start_date')[:5]
    
    return {
        'ads_banners': active_banners
    }


def notification_processor(request):
    """
    Context processor that adds notification count to all templates
    """
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
        return {
            'notification_count': unread_count
        }
    return {
        'notification_count': 0
    }