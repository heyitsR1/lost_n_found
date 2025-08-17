# 🎓 University Lost & Found Management System

A comprehensive, scalable lost and found platform designed specifically for universities. Built with Django and modern web technologies, this system provides an intuitive interface for students and staff to report lost items, post found items, and manage the entire lost and found workflow.

## ✨ Features

### 🔐 Authentication & User Management
- **Custom User Model** with student ID validation
- **Google OAuth Integration** for seamless login
- **Student ID Verification** system
- **Department & Graduation Year** tracking
- **Role-based Access Control**

### 📱 Core Functionality
- **Lost Item Reports** - Students can post detailed descriptions with images
- **Found Item Posts** - Staff and students can report found items
- **Multi-image Support** with primary image selection
- **Category & Location Management** for organized item tracking
- **Contact System** for item owners and finders
- **Urgent Item Flagging** for time-sensitive cases
- **Reward System** for found items

### 🎨 Modern UI/UX
- **Responsive Design** - Works on all devices
- **Smooth Animations** - Hover effects, tilt animations, scroll-based reveals
- **Glitch-style Effects** - Modern, engaging visual elements
- **Bootstrap 5** framework for consistent styling
- **FontAwesome Icons** for intuitive navigation
- **Custom CSS Animations** for enhanced user experience

### 🔍 Search & Filtering
- **Advanced Search** by item type, category, location, and keywords
- **Filter System** for quick item discovery
- **Pagination** for large item collections
- **Status Tracking** (Active, Claimed, Expired, Closed)

### 📊 Dashboard & Analytics
- **User Dashboard** with personal item history
- **Admin Panel** for comprehensive system management
- **Statistics Overview** - Total items, success rates, etc.
- **Contact Management** for item inquiries

## 🚀 Technology Stack

### Backend
- **Django 5.2.4** - Robust web framework
- **SQLite/PostgreSQL** - Database support
- **Django Allauth** - Authentication system
- **Django Crispy Forms** - Form rendering
- **Django Filters** - Advanced filtering
- **Pillow** - Image processing

### Frontend
- **HTML5/CSS3** - Semantic markup and styling
- **Bootstrap 5** - Responsive UI framework
- **JavaScript** - Interactive features and animations
- **FontAwesome** - Icon library
- **Google Fonts** - Typography

### Authentication
- **Google OAuth 2.0** - Social login integration
- **Custom User Model** - Extended user fields
- **Student ID Validation** - University-specific verification

## 📋 Requirements

### Python Dependencies
```
Django>=5.2.4
django-allauth>=0.60.0
django-crispy-forms>=2.0
crispy-bootstrap5>=0.7
django-filter>=23.0
Pillow>=10.0.0
requests>=2.31.0
PyJWT>=2.8.0
cryptography>=41.0.0
```

### System Requirements
- Python 3.8+
- Virtual environment support
- Database (SQLite for development, PostgreSQL for production)
- Web server (Gunicorn, uWSGI, or similar)

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd lost_n_found
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Populate Initial Data
```bash
python manage.py populate_data
```

### 8. Run Development Server
```bash
python manage.py runserver
```

## 🔧 Configuration

### Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs: `http://localhost:8000/accounts/google/login/callback/`
6. Update settings with client ID and secret

### Customization for Different Universities
The system is designed to be easily customizable:

- **Branding**: Update colors, logos, and university names
- **Student ID Format**: Modify regex validation in `accounts/models.py`
- **Categories**: Customize item categories and locations
- **Email Templates**: Update notification emails
- **Domain Restrictions**: Configure allowed email domains

## 📱 Usage

### For Students
1. **Sign Up** with university email and student ID
2. **Report Lost Items** with descriptions and photos
3. **Browse Found Items** to claim lost belongings
4. **Contact Item Owners** through the built-in messaging system
5. **Track Item Status** in personal dashboard

### For Staff
1. **Post Found Items** with detailed descriptions
2. **Manage Item Status** (Active, Claimed, Expired)
3. **Process Claims** and verify ownership
4. **Generate Reports** on system usage

### For Administrators
1. **User Management** - Monitor and manage user accounts
2. **Category Management** - Add/edit item categories
3. **Location Management** - Configure campus locations
4. **System Analytics** - View usage statistics and reports

## 🏗️ Project Structure

```
lost_n_found/
├── accounts/                 # User authentication and management
│   ├── models.py            # Custom user model
│   ├── forms.py             # Signup and user forms
│   └── admin.py             # Admin interface configuration
├── core/                    # Main application logic
│   ├── models.py            # Item, Category, Location models
│   ├── views.py             # View functions and logic
│   ├── forms.py             # Item and search forms
│   └── urls.py              # URL routing
├── templates/               # HTML templates
│   ├── base.html            # Base template with navigation
│   └── core/                # Page-specific templates
├── static/                  # CSS, JavaScript, and images
├── media/                   # User-uploaded images
├── lost_n_found_project/    # Django project settings
│   ├── settings.py          # Project configuration
│   └── urls.py              # Main URL configuration
└── manage.py                # Django management script
```

## 🔒 Security Features

- **CSRF Protection** - Built-in Django security
- **SQL Injection Prevention** - ORM-based queries
- **XSS Protection** - Template auto-escaping
- **File Upload Security** - Image validation and sanitization
- **Authentication Middleware** - Secure user sessions
- **Permission-based Access** - Role-based system access

## 📊 Database Schema

### Core Models
- **User**: Extended user model with student information
- **Item**: Lost/found items with metadata
- **Category**: Item classification system
- **Location**: Campus location management
- **ItemImage**: Multiple image support for items
- **Contact**: Communication between users

### Key Relationships
- Users can post multiple items
- Items belong to categories and locations
- Items can have multiple images
- Users can contact item owners

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in settings
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up static file serving (nginx/Apache)
- [ ] Configure media file storage
- [ ] Set up SSL certificates
- [ ] Configure email backend
- [ ] Set up monitoring and logging
- [ ] Configure backup systems

### Recommended Production Stack
- **Web Server**: nginx
- **Application Server**: Gunicorn
- **Database**: PostgreSQL
- **File Storage**: AWS S3 or similar
- **Email**: SendGrid or AWS SES

## 🔄 API Endpoints

The system provides RESTful endpoints for:
- User authentication and management
- Item CRUD operations
- Search and filtering
- Image upload and management
- Contact and messaging

## 📈 Scalability Features

- **Modular Architecture** - Easy to extend and customize
- **Database Optimization** - Efficient queries and indexing
- **Caching Support** - Redis integration ready
- **CDN Ready** - Static file optimization
- **Multi-tenant Support** - Can serve multiple universities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- **Mobile App** - Native iOS/Android applications
- **AI Integration** - Image recognition for item matching
- **Blockchain** - Secure ownership verification
- **Multi-language Support** - International university support
- **Advanced Analytics** - Machine learning insights
- **Integration APIs** - Connect with university systems

---

**Built with ❤️ for universities worldwide**

*This system is designed to be easily deployable and customizable for any educational institution, making it an ideal solution for universities looking to modernize their lost and found operations.*

