# Image Guide for Lost N Found Items

## How to Add Images to Dummy Listings

### 1. Image Storage Location
Images for items should be stored in the `media/` folder at the root of your project. This is where Django automatically saves uploaded images.

**Folder Structure:**
```
lost_n_found/
├── media/           ← Images are stored here
│   ├── item_images/ ← Django creates this automatically
│   └── other_files/
├── static/          ← Static images (logos, icons)
└── ...
```

### 2. Adding Images to Existing Items

#### Option A: Through Django Admin
1. Go to `http://127.0.0.1:8001/admin/` (or your server port)
2. Login with your admin credentials
3. Navigate to **Core** → **Items**
4. Click on an item to edit it
5. In the **Item Images** section, click **Add another Item image**
6. Upload your image file
7. Click **Save**

#### Option B: Through the Website
1. Go to the item detail page
2. If you're the owner, you'll see an "Edit" button
3. Click "Edit" and add images in the form
4. Save the changes

### 3. Supported Image Formats
Django supports these image formats:
- **JPEG** (.jpg, .jpeg) - Best for photos
- **PNG** (.png) - Best for graphics with transparency
- **GIF** (.gif) - For simple animations
- **WebP** (.webp) - Modern, efficient format

### 4. Image Requirements
- **File Size**: Recommended under 5MB per image
- **Dimensions**: Recommended minimum 300x300 pixels
- **Aspect Ratio**: Any ratio is supported, but square or 4:3 works best for item cards

### 5. Checking Saved Image Format
To see what format your images are saved as:

#### Through Django Admin:
1. Go to **Core** → **Item Images**
2. View the list of uploaded images
3. The filename will show the extension (e.g., `item_photo.jpg`)

#### Through File System:
1. Navigate to `media/item_images/` folder
2. Check the file extensions of uploaded images
3. Common formats: `.jpg`, `.png`, `.gif`

#### Through Database:
```bash
# In Django shell
python manage.py shell

# Check image paths
from core.models import ItemImage
ItemImage.objects.all().values('image')
```

### 6. Image Naming Convention
Django automatically generates unique names for uploaded images to prevent conflicts:
- Format: `original_name_timestamp_randomstring.extension`
- Example: `phone_photo_20250816_123456_abc123.jpg`

### 7. Adding Images to New Items
When creating a new item:
1. Fill out the item form
2. In the **Images** section, click **Choose File**
3. Select your image(s)
4. You can add multiple images
5. Submit the form

### 8. Troubleshooting

#### Images Not Displaying:
- Check if `MEDIA_URL` and `MEDIA_ROOT` are configured in `settings.py`
- Ensure the media folder has proper permissions
- Check browser console for 404 errors

#### Upload Errors:
- Verify file format is supported
- Check file size limits
- Ensure form has `enctype="multipart/form-data"`

#### Image Quality Issues:
- Use higher resolution source images
- Avoid compressing images multiple times
- Consider using WebP format for better compression

### 9. Best Practices
1. **Use descriptive filenames** before uploading
2. **Optimize images** for web (compress without losing quality)
3. **Maintain consistent aspect ratios** for better display
4. **Include multiple angles** for better item identification
5. **Use good lighting** when taking photos

### 10. Example Image Setup
```
media/
├── item_images/
│   ├── phone_photo_20250816_123456_abc123.jpg
│   ├── laptop_photo_20250816_123457_def456.png
│   └── keys_photo_20250816_123458_ghi789.webp
└── other_files/
    └── video.mp4
```

### 11. Quick Test
To quickly test image functionality:
1. Add a test image to any item through admin
2. Check if it appears on the item detail page
3. Verify it shows correctly in the item list
4. Test the image in different browsers/devices

### 12. Need Help?
If you encounter issues:
- Check Django logs for error messages
- Verify file permissions on the media folder
- Ensure your web server is configured to serve media files
- Check if the image model relationships are correct
