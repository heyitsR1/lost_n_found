from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Contact, Category, Location


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'title', 'description', 'item_type', 'category', 'location',
            'contact_name', 'contact_email', 'contact_phone', 'reward', 'reward_coins', 'is_urgent'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter item title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the item in detail...'
            }),
            'item_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number'
            }),
            'reward': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'reward_coins': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
                'help_text': 'Offer reward coins to encourage people to help find your item'
            }),
            'is_urgent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make contact fields required for found items
        if self.instance.pk and self.instance.item_type == 'found':
            self.fields['contact_name'].required = True
            self.fields['contact_email'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        item_type = cleaned_data.get('item_type')
        contact_name = cleaned_data.get('contact_name')
        contact_email = cleaned_data.get('contact_email')
        
        # For found items, require contact information
        if item_type == 'found':
            if not contact_name:
                self.add_error('contact_name', 'Contact name is required for found items.')
            if not contact_email:
                self.add_error('contact_email', 'Contact email is required for found items.')
        
        return cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number (optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your message...'
            }),
        }
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long.')
        return message


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search items...'
        })
    )
    item_type = forms.ChoiceField(
        choices=[('', 'All Types'), ('lost', 'Lost'), ('found', 'Found')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    location_type = forms.ChoiceField(
        choices=[('', 'All Floors')] + [
            ('parking', 'Parking Space'),
            ('ground_floor', 'Ground Floor'),
            ('first_floor', 'First Floor'),
            ('second_floor', 'Second Floor'),
            ('third_floor', 'Third Floor'),
            ('fourth_floor', 'Fourth Floor'),
            ('fifth_floor', 'Fifth Floor'),
            ('sixth_floor', 'Sixth Floor'),
            ('seventh_floor', 'Seventh Floor'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    floor_area = forms.ChoiceField(
        choices=[('', 'All Areas')] + [
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
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status'), ('active', 'Active'), ('claimed', 'Claimed')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    ) 