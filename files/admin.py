from django.contrib import admin
from .models import UploadedFile

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_at', 'user')
    list_filter = ('uploaded_at', 'user')
    search_fields = ('file',)
