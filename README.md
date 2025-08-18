# 🎓 King's College Lost N Found System

A comprehensive web application for managing lost and found items within King's College campus, featuring a reward system, advertisement management, and automated notification workflows.

## 🚀 Features

### Core Functionality
- **Lost & Found Management**: Post, search, and manage lost/found items
- **King's College Integration**: Location system matching actual campus layout
- **Reward System**: Coin-based rewards for helpful actions
- **Advertisement System**: Dynamic banner and listing ads
- **Admin Workflow**: Complete verification and claim process
- **Email Notifications**: Automated updates for all events

### Technical Features
- **Django 5.2.4**: Modern Python web framework
- **Custom User Model**: Extended student information
- **Real-time Notifications**: Signal-based event system
- **Responsive Design**: Bootstrap 5 frontend
- **Image Management**: Multiple images per item
- **Advanced Search**: Location, category, and status filtering

## 🏗️ System Architecture

```
lost_n_found/
├── accounts/                 # Custom user management
├── core/                     # Main application logic
├── lost_n_found_project/     # Django project settings
├── media/                    # User uploaded files
├── static/                   # CSS, JS, images
├── templates/                # HTML templates
└── manage.py                 # Django management
```

## 🔐 Authentication

- **Email-based login** with custom user model
- **Social authentication** (Google OAuth)
- **Student ID validation** with uniqueness checks
- **Extended user fields**: department, graduation year, phone

## 🗄️ Database Models

### Core Entities
- **Item**: Lost/found items with complete workflow tracking
- **Location**: King's College campus mapping system
- **Category**: Item classification system
- **User**: Extended student profiles
- **Notification**: System-wide notification system
- **AdsBanner**: Advertisement management
- **RewardCoin**: Virtual currency system

### Workflow States
1. **Pending Verification** → **Verified** → **Active**
2. **Dropped Off** → **Ready for Claim** → **Claimed**

## 📧 Notification System

### Automatic Triggers
- **Item Found**: Admin + user notifications
- **Item Verified**: User confirmation
- **Item Claimed**: User + admin updates
- **Admin Actions**: Required action notifications

### Email Templates
- HTML and text versions for all notification types
- Context-aware content with item details
- Professional styling and branding

## 🎯 Advertisement System

### Banner Types
- **Top Banners**: Pure image ads (100px height)
- **Listing Ads**: Integrated into item browse (every 3 items)

### Management Features
- **Priority-based ordering**
- **Date scheduling** (start/end dates)
- **Type categorization** (sponsor, event, announcement, club)
- **Admin-only sponsor tracking**

## 🏆 Reward System

### Coin Earning
- **Found Items**: 25 base coins
- **Admin Recognition**: Special rewards
- **Community Help**: Additional coins

### Redemption Options
- **Canteen Vouchers**: Food and beverages
- **Cafe Vouchers**: Coffee and snacks
- **Bookstore Vouchers**: Academic supplies
- **Event Vouchers**: Special activities

## 🔍 Search & Filtering

### Advanced Search
- **Multi-field search** across title, description, location
- **Location filtering** by floor and area
- **Status filtering** for workflow management
- **Category filtering** for organization
- **Pagination** for large result sets

### Location System
- **Ground Floor**: Library, IT Lab, Kafe Kodes, Tech Club
- **Second Floor**: Class 201
- **Third Floor**: Class 301
- **Fourth Floor**: Class 401
- **Sixth Floor**: Program Hall, DoLab
- **Seventh Floor**: Canteen
- **Parking**: Main Parking Area

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Django 5.2.4
- Virtual environment

### Installation
```bash
# Clone repository
git clone <repository-url>
cd lost_n_found

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate initial data
python manage.py populate_data
python manage.py populate_kings_college_locations
python manage.py repopulate_items_kings_college

# Run development server
python manage.py runserver
```

### Management Commands
```bash
# Data population
python manage.py populate_data
python manage.py populate_kings_college_locations
python manage.py repopulate_items_kings_college
python manage.py associate_images

# System maintenance
python manage.py fix_email_templates
python manage.py check
python manage.py collectstatic
```

## 📱 User Experience

### For Students
- **Easy item posting** with guided forms
- **Real-time updates** via email notifications
- **Reward earning** for helpful actions
- **Mobile-responsive** design

### For Admins
- **Complete workflow management**
- **Item verification system**
- **Advertisement control**
- **Analytics and reporting**

## 🔧 Configuration

### Environment Variables
```bash
DEBUG=True
SECRET_KEY=your-secret-key
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Email Setup
- **Gmail SMTP** configuration
- **App password** required for Gmail
- **Template system** for all notifications

## 🧪 Testing

### System Health
```bash
python manage.py check
```

### Email Testing
```bash
python manage.py shell -c "from django.core.mail import send_mail; send_mail('Test', 'Test email', 'from@example.com', ['to@example.com'])"
```

### Notification Testing
```bash
python manage.py shell -c "from core.services import NotificationService; from core.models import Item; item = Item.objects.first(); NotificationService.notify_item_found(item)"
```

## 📊 Performance

### Optimizations
- **Database indexing** for fast searches
- **Select related** queries to reduce database calls
- **Pagination** for large datasets
- **Image optimization** and responsive sizing

### Scalability
- **Modular architecture** for easy extension
- **Service layer** for business logic
- **Signal system** for loose coupling
- **Template inheritance** for reusable components

## 🔒 Security

### Features
- **CSRF protection** enabled
- **Input validation** on all forms
- **File upload security** for images
- **Admin access control**
- **Secure session management**

### Best Practices
- **Environment variables** for sensitive data
- **HTTPS ready** for production
- **Regular security updates**
- **User permission management**

## 🚀 Deployment

### Production Requirements
- **PostgreSQL** database
- **Cloud storage** for media files
- **CDN** for static assets
- **Production SMTP** service
- **HTTPS** configuration

### Deployment Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure production database
- [ ] Set up media file storage
- [ ] Configure email service
- [ ] Set `ALLOWED_HOSTS`
- [ ] Run `collectstatic`
- [ ] Test all functionality

## 📚 Documentation

### User Guides
- **USER_GUIDE.md**: Complete user documentation
- **ADMIN_GUIDE.md**: Administrative procedures
- **AD_BANNER_TESTING_GUIDE.md**: Advertisement system testing

### Technical Documentation
- **TECHNICAL_DOCUMENTATION.md**: Comprehensive technical overview
- **API Documentation**: REST API specifications
- **Database Schema**: Complete model documentation

## 🆘 Support

### Common Issues
1. **Signup Errors**: Check student ID uniqueness
2. **Email Issues**: Verify SMTP configuration
3. **Image Uploads**: Check media directory permissions
4. **Notification Problems**: Verify email templates

### Troubleshooting
- **Check system health**: `python manage.py check`
- **Verify email setup**: Test email sending
- **Check notifications**: Review notification logs
- **Database issues**: Run migrations

## 🎯 Future Enhancements

### Planned Features
- **Mobile Application**: React Native/Flutter
- **Real-time Updates**: WebSocket integration
- **Advanced Analytics**: User behavior tracking
- **Multi-language Support**: Internationalization
- **API Development**: Third-party integrations

### Technical Improvements
- **Microservices Architecture**: Service separation
- **Event Sourcing**: Advanced event tracking
- **Machine Learning**: Smart item matching
- **Blockchain**: Secure reward system

## 📞 Contact

- **Project Team**: Lost N Found Development Team
- **Support Email**: support@kings.edu
- **Documentation**: See technical documentation files
- **Issues**: Use project issue tracker

---

**🎉 The King's College Lost N Found system provides a comprehensive solution for managing lost and found items with modern web technologies, automated workflows, and a user-friendly interface designed specifically for educational environments.**

**Built with ❤️ for King's College students and staff.**

