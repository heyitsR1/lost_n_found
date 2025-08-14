from .models import AdsBanner
from django.utils import timezone

def ads_banners_processor(request):
    """
    Context processor that adds active ads/banners to all templates
    """
    today = timezone.now().date()
    active_banners = AdsBanner.objects.filter(
        is_active=True,
        start_date__lte=today
    ).filter(
        end_date__isnull=True
    ).order_by('-priority', '-start_date')[:5]
    
    return {
        'ads_banners': active_banners
    }