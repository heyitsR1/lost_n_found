# 👨‍💼 King's College Lost N Found - Admin Guide

## 🔐 **Admin Access**

### **Login to Admin Panel**
- **URL**: `/admin`
- **Username**: Your admin credentials
- **Permissions**: Full system access

### **Admin Dashboard Sections**
- **Items**: Manage all lost and found items
- **Users**: Manage student accounts
- **Categories**: Manage item categories
- **Locations**: Manage King's College locations
- **Ads Banners**: Manage advertisement system
- **Rewards**: Manage coin system and vouchers
- **Notifications**: Manage system notifications

---

## 📋 **Item Management**

### **Viewing All Items**
1. Go to **Items** section in admin
2. View items with filters:
   - **Status**: Active, Pending, Verified, Dropped Off, Claimed
   - **Type**: Lost or Found
   - **Date Range**: When items were created
   - **Location**: Filter by college areas

### **Item Status Workflow**

#### **1. Pending Verification**
- **New Items**: All new items start here
- **Action Required**: Review and verify item details
- **Next Step**: Mark as "Verified" or "Rejected"

#### **2. Verified**
- **Admin Verified**: Item details confirmed
- **Visible to Users**: Item appears in browse section
- **Next Step**: Wait for claims or drop-off

#### **3. Dropped Off**
- **At Admin Office**: Item physically received
- **Secure Storage**: Item stored safely
- **Next Step**: Ready for claim by owner

#### **4. Ready for Claim**
- **Owner Contacted**: Owner notified item is ready
- **Claim Process**: Owner can claim with ID verification
- **Next Step**: Item claimed or returned to storage

#### **5. Claimed**
- **Successfully Returned**: Item returned to owner
- **Rewards Distributed**: Coins awarded to finder
- **Case Closed**: Item archived

### **Admin Actions**

#### **Verify Item**
1. Click on item in admin panel
2. Review item details and images
3. Add admin notes if needed
4. Change status to "Verified"
5. Set "Admin Verified" fields:
   - **Verified By**: Your admin username
   - **Verified At**: Current timestamp
   - **Admin Notes**: Any additional notes

#### **Reject Item**
1. Review item details
2. Add rejection reason in admin notes
3. Change status to "Rejected"
4. Notify user via email

#### **Mark as Dropped Off**
1. When item is physically received
2. Update status to "Dropped Off"
3. Set drop-off date and time
4. Add storage location notes

#### **Process Claim**
1. Verify claimant's identity
2. Check item description matches
3. Update status to "Claimed"
4. Record claim details:
   - **Claimer Name**: Person claiming item
   - **Claimer ID Verified**: Yes/No
   - **Claim Date**: When item was claimed

---

## 🎯 **Ad Banner Management**

### **Creating New Banners**
1. Go to **Ads Banners** section
2. Click **"Add Advertisement Banner"**
3. Fill in banner details:

#### **Banner Information**
- **Title**: Clear, catchy title (e.g., "CMF Phone 2 Pro")
- **Description**: Brief description of the ad
- **Banner Type**: Sponsor, Event, Announcement, Club

#### **Display Settings**
- **Image**: Upload banner image (recommended size: 800x400px)
- **URL**: Link to more information (optional)

#### **Visibility Settings**
- **Is Active**: Enable/disable banner
- **Start Date**: When banner should appear
- **End Date**: When banner should disappear (leave blank for permanent)
- **Priority**: Higher numbers appear first (0-10)

### **Banner Types**

#### **Sponsor Banners**
- **Purpose**: Promote products and services
- **Examples**: Tech products, local businesses, services
- **Duration**: Usually 1-4 weeks
- **Priority**: 5-8
- **Note**: Sponsor information is kept internal and not displayed to users

#### **Event Banners**
- **Purpose**: Promote college events
- **Examples**: Career fairs, workshops, social events
- **Duration**: Event-specific (1-2 weeks)
- **Priority**: 7-9

#### **Announcement Banners**
- **Purpose**: Important college announcements
- **Examples**: Policy changes, system updates
- **Duration**: Until announcement is no longer relevant
- **Priority**: 8-10

#### **Club Banners**
- **Purpose**: Promote student clubs and activities
- **Examples**: Tech club, sports clubs, cultural groups
- **Duration**: Club-specific (1-3 weeks)
- **Priority**: 3-6

### **Managing Active Banners**
- **View All**: See all banners with status
- **Edit**: Modify banner details
- **Deactivate**: Turn off banners temporarily
- **Delete**: Remove banners permanently
- **Reorder**: Change priority to control display order

### **Banner Analytics**
- **View Count**: Track how many times banners are viewed
- **Click Rate**: Monitor banner effectiveness
- **Duration**: Track how long banners are active

---

## 🏆 **Reward System Management**

### **Coin System Overview**
- **Earning**: Users earn coins for helpful actions
- **Spending**: Coins can be redeemed for vouchers
- **Tracking**: All transactions are logged

### **Managing User Coins**
1. Go to **Reward Coins** section
2. View user coin balances
3. **Add Coins**: Award coins for special actions
4. **Deduct Coins**: Remove coins for violations
5. **View History**: See all coin transactions

### **Voucher Management**
1. Go to **Vouchers** section
2. **Create Vouchers**: Set up new voucher types
3. **Set Values**: Define coin cost for each voucher
4. **Manage Inventory**: Track available vouchers
5. **Process Redemptions**: Handle voucher requests

### **Voucher Types**
- **Canteen Vouchers**: Food and beverages
- **Cafe Vouchers**: Coffee and snacks
- **Bookstore Vouchers**: Academic supplies
- **Event Vouchers**: Special events and activities

### **Reward Policies**
- **Found Items**: 25-100 coins based on item value
- **Helpful Actions**: 10-50 coins for community help
- **Admin Recognition**: Special rewards for outstanding behavior
- **Penalties**: Coin deduction for rule violations

---

## 📍 **Location Management**

### **King's College Layout**
The system uses the actual college layout:

#### **Ground Floor**
- **Library**: Main Library
- **IT Lab**: IT Lab
- **Kafe Kodes**: Kafe Kodes
- **Tech Club**: Tech Club Room

#### **Second Floor**
- **Class 201**: Classroom 201

#### **Third Floor**
- **Class 301**: Classroom 301

#### **Fourth Floor**
- **Class 401**: Classroom 401

#### **Sixth Floor**
- **Program Hall**: Program Hall
- **DoLab**: DoLab

#### **Seventh Floor**
- **Canteen**: Main Canteen

#### **Parking**
- **Main Parking**: Main Parking Area

### **Managing Locations**
1. Go to **Locations** section
2. **Add Locations**: Create new areas if needed
3. **Edit Locations**: Update location details
4. **Organize**: Maintain proper hierarchy

---

## 👥 **User Management**

### **Viewing Users**
1. Go to **Users** section
2. **Search Users**: Find specific students
3. **Filter**: By department, graduation year, etc.
4. **View Details**: See user profiles and activity

### **User Actions**
- **Verify Accounts**: Confirm student status
- **Suspend Users**: Temporarily disable accounts
- **Delete Users**: Remove accounts (use carefully)
- **Reset Passwords**: Help users with login issues

### **User Statistics**
- **Active Users**: Number of registered users
- **User Activity**: Login frequency and engagement
- **Item Contributions**: How many items each user has posted
- **Reward Status**: Coin balances and voucher redemptions

---

## 🔔 **Notification Management**

### **System Notifications**
- **Email Templates**: Manage notification emails
- **Auto Notifications**: System-generated alerts
- **Manual Notifications**: Send custom messages

### **Notification Types**
- **Item Found**: When lost items are found
- **Item Claimed**: When found items are claimed
- **Admin Actions**: Status changes and verifications
- **Rewards**: Coin earnings and voucher redemptions
- **System Alerts**: Important system updates

### **Managing Templates**
1. Go to **Notification Templates** section
2. **Edit Templates**: Modify email content
3. **Test Templates**: Send test emails
4. **Activate/Deactivate**: Control which templates are used

---

## 📊 **Analytics & Reports**

### **System Statistics**
- **Total Items**: Lost and found items count
- **Success Rate**: Percentage of items returned
- **User Engagement**: Active users and participation
- **Reward Distribution**: Coin and voucher statistics

### **Generate Reports**
- **Daily Reports**: Daily activity summaries
- **Weekly Reports**: Weekly statistics and trends
- **Monthly Reports**: Monthly performance analysis
- **Custom Reports**: Specific data queries

### **Key Metrics**
- **Items Posted**: New items per day/week/month
- **Items Returned**: Successfully claimed items
- **User Growth**: New user registrations
- **Reward Activity**: Coin transactions and redemptions

---

## 🛠️ **System Maintenance**

### **Regular Tasks**
- **Daily**: Check new items and verify them
- **Weekly**: Review banner performance and update
- **Monthly**: Generate reports and analyze trends
- **Quarterly**: Review and update location data

### **Data Management**
- **Backup**: Regular database backups
- **Cleanup**: Archive old items and notifications
- **Optimization**: Maintain system performance
- **Updates**: Keep system up to date

### **Security**
- **User Verification**: Verify new user accounts
- **Content Moderation**: Review and approve content
- **Access Control**: Manage admin permissions
- **Audit Logs**: Monitor system activity

---

## 🆘 **Troubleshooting**

### **Common Issues**

#### **Banners Not Showing**
- Check if banner is active
- Verify start/end dates
- Check priority settings
- Clear browser cache

#### **Items Not Appearing**
- Check item status (should be "Verified")
- Verify location settings
- Check user permissions
- Review admin verification

#### **Reward System Issues**
- Verify coin calculations
- Check voucher availability
- Review transaction logs
- Confirm user eligibility

### **Support Resources**
- **Documentation**: System documentation
- **Training**: Admin training materials
- **IT Support**: Technical assistance
- **Emergency Contacts**: Urgent issues

---

## 📞 **Quick Reference**

### **Admin URLs**
- **Admin Panel**: `/admin`
- **Items**: `/admin/core/item/`
- **Users**: `/admin/accounts/customuser/`
- **Banners**: `/admin/core/adsbanner/`
- **Rewards**: `/admin/core/rewardcoin/`

### **Important Commands**
```bash
# Check system status
python manage.py check

# Generate reports
python manage.py generate_reports

# Backup database
python manage.py dumpdata > backup.json

# Clear old data
python manage.py cleanup_old_data
```

### **Contact Information**
- **IT Support**: +1-555-8888
- **System Admin**: admin@kings.edu
- **Emergency**: +1-555-9999

---

**🎯 This admin guide covers all aspects of managing the King's College Lost N Found system. For additional support, contact the IT department.**
