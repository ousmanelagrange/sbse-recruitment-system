from django.db import models
import cloudinary
import cloudinary.uploader
from cloudinary.models import CloudinaryField

class CVUpload(models.Model):
    """Model for storing CV uploads in Cloudinary"""
    name = models.CharField(max_length=255, blank=True)
    file = CloudinaryField('cv', resource_type='auto', folder='cv_uploads/')
    file_type = models.CharField(max_length=100, blank=True)
    file_size = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"CV: {self.name} (uploaded at {self.uploaded_at})"
    
    class Meta:
        ordering = ['-uploaded_at']
