from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from .models import Item, Category, Location, ItemImage, Contact, Notification, AdsBanner
from .forms import ItemForm, ContactForm
import json


def home(request):
    """Landing page with statistics and recent items"""
    context = {
        'total_items': Item.objects.count(),
        'lost_items': Item.objects.filter(item_type='lost', status='active').count(),
        'found_items': Item.objects.filter(item_type='found', status='active').count(),
        'recent_lost': Item.objects.filter(item_type='lost', status='active').order_by('-created_at')[:3],
        'recent_found': Item.objects.filter(item_type='found', status='active').order_by('-created_at')[:3],
        'categories': Category.objects.all(),
    }
    return render(request, 'core/home.html', context)


def item_list(request):
    """List all items with filtering and search"""
    items = Item.objects.select_related('category', 'location', 'user').prefetch_related('images')
    
    # Filtering
    item_type = request.GET.get('type')
    category_id = request.GET.get('category')
    status = request.GET.get('status')
    search = request.GET.get('search')
    location_type = request.GET.get('location_type')
    floor_area = request.GET.get('floor_area')
    
    if item_type:
        items = items.filter(item_type=item_type)
    if category_id:
        items = items.filter(category_id=category_id)
    if status:
        items = items.filter(status=status)
    if location_type:
        items = items.filter(location__location_type=location_type)
    if floor_area:
        items = items.filter(location__floor_area=floor_area)
    if search:
        items = items.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(category__name__icontains=search) |
            Q(location__location_type__icontains=search) |
            Q(location__floor_area__icontains=search) |
            Q(location__specific_location__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'locations': Location.objects.all(),
        'filters': {
            'type': item_type,
            'category': category_id,
            'status': status,
            'search': search,
            'location_type': location_type,
            'floor_area': floor_area,
        }
    }
    return render(request, 'core/item_list.html', context)


def item_detail(request, pk):
    """Detail view for a specific item"""
    item = get_object_or_404(Item.objects.select_related('category', 'location', 'user').prefetch_related('images'), pk=pk)
    
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.item = item
            contact.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('core:item_detail', pk=pk)
    else:
        contact_form = ContactForm()
    
    # Get related items
    related_items = Item.objects.filter(
        category=item.category,
        item_type=item.item_type
    ).exclude(pk=item.pk)[:3]
    
    context = {
        'item': item,
        'contact_form': contact_form,
        'related_items': related_items,
    }
    return render(request, 'core/item_detail.html', context)


@login_required
def item_create(request):
    """Create a new item"""
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            
            # Handle multiple images
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                ItemImage.objects.create(
                    item=item,
                    image=image,
                    is_primary=(i == 0)  # First image is primary
                )
            
            messages.success(request, f'Your {item.get_item_type_display()} item has been posted successfully!')
            return redirect('core:item_detail', pk=item.pk)
    else:
        form = ItemForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
        'locations': Location.objects.all(),
    }
    return render(request, 'core/item_form.html', context)


@login_required
def item_update(request, pk):
    """Update an existing item"""
    item = get_object_or_404(Item, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            
            # Handle new images
            images = request.FILES.getlist('images')
            for image in images:
                ItemImage.objects.create(item=item, image=image)
            
            messages.success(request, 'Item updated successfully!')
            return redirect('core:item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    
    context = {
        'form': form,
        'item': item,
        'categories': Category.objects.all(),
        'locations': Location.objects.all(),
    }
    return render(request, 'core/item_form.html', context)


@login_required
def item_delete(request, pk):
    """Delete an item"""
    item = get_object_or_404(Item, pk=pk, user=request.user)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('core:item_list')
    
    return render(request, 'core/item_confirm_delete.html', {'item': item})


@login_required
def dashboard(request):
    """User dashboard showing their items"""
    user_items = Item.objects.filter(user=request.user).select_related('category', 'location')
    
    context = {
        'user_items': user_items,
        'active_items': user_items.filter(status='active'),
        'claimed_items': user_items.filter(status='claimed'),
        'expired_items': user_items.filter(status='expired'),
    }
    return render(request, 'core/dashboard.html', context)


def search_items(request):
    """AJAX search for items"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'items': []})
    
    items = Item.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    ).select_related('category', 'location')[:10]
    
    results = []
    for item in items:
        results.append({
            'id': item.pk,
            'title': item.title,
            'type': item.get_item_type_display(),
            'category': item.category.name,
            'location': str(item.location),
            'url': item.get_absolute_url(),
        })
    
    return JsonResponse({'items': results})


def debug_urls(request):
    """Debug view to test URL resolution"""
    from django.urls import reverse
    try:
        item_detail_url = reverse('core:item_detail', kwargs={'pk': 1})
        item_list_url = reverse('core:item_list')
        return JsonResponse({
            'success': True,
            'item_detail_url': item_detail_url,
            'item_list_url': item_list_url,
            'available_urls': [
                'core:item_detail',
                'core:item_list',
                'core:item_create',
                'core:item_update',
                'core:item_delete'
            ]
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        })


def about(request):
    """About page"""
    return render(request, 'core/about.html')


def contact_us(request):
    """Contact us page"""
    return render(request, 'core/contact.html')


def test_auth(request):
    """Test authentication view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': f'Logged in as {user.email}'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        else:
            return JsonResponse({'success': False, 'message': 'Missing email or password'})
    
    return render(request, 'core/test_auth.html')


@login_required
def notifications_view(request):
    """View for user notifications"""
    notifications = request.user.notifications.all().order_by('-created_at')
    
    # Mark notifications as read when viewed
    unread_notifications = notifications.filter(is_read=False)
    if unread_notifications.exists():
        unread_notifications.update(is_read=True)
    
    context = {
        'notifications': notifications,
        'unread_count': request.user.notifications.filter(is_read=False).count(),
    }
    return render(request, 'core/notifications.html', context)


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Mark a notification as read via AJAX"""
    try:
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.mark_as_read()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def mark_all_notifications_read(request):
    """Mark all user notifications as read"""
    if request.method == 'POST':
        request.user.notifications.filter(is_read=False).update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
        return redirect('core:notifications')
    
    return redirect('core:notifications')
