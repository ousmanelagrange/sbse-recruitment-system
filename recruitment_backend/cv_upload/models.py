from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class CVUpload(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    cv_file = CloudinaryField('cv', resource_type='raw', format='pdf')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    class Meta:
        ordering = ['-uploaded_at']
