from django.contrib import admin
from .models import CVUpload

@admin.register(CVUpload)
class CVUploadAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
