from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Item, Category, Location, ItemImage, Contact
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
    
    if item_type:
        items = items.filter(item_type=item_type)
    if category_id:
        items = items.filter(category_id=category_id)
    if status:
        items = items.filter(status=status)
    if search:
        items = items.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(category__name__icontains=search) |
            Q(location__name__icontains=search)
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
            return redirect('item_detail', pk=pk)
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
            return redirect('item_detail', pk=item.pk)
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
            return redirect('item_detail', pk=item.pk)
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
        return redirect('item_list')
    
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


def about(request):
    """About page"""
    return render(request, 'core/about.html')


def contact_us(request):
    """Contact us page"""
    return render(request, 'core/contact.html')


def test_auth(request):
    """Test authentication view"""
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
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
