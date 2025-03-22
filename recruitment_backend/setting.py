# filepath: /home/aureltoukam/Bureau/Master 2/SBSE/projet SBSE/sbse-recruitment-system/recruitment_backend/settings.py
INSTALLED_APPS = [
    # ...existing apps...
    'cloudinary',
    'cloudinary_storage',
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'ddcnxl9ro',
    'API_KEY': '676362383327282',
    'API_SECRET': 'mP_RHbOv79EXP0tlPUmKToNR2BY',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'