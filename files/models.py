from django.db import models
from django.contrib.auth import get_user_model
import os

User = get_user_model()

def get_file_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.pdf']:
        return 'PDF'
    elif ext in ['.xls', '.xlsx']:
        return 'Excel'
    elif ext in ['.txt']:
        return 'TXT'
    elif ext in ['.doc', '.docx']:
        return 'Word'
    else:
        return 'Other'

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=20, default='Other')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')

    def save(self, *args, **kwargs):
        if self.file:
            self.file_type = get_file_type(self.file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file.name} by user ID {self.user.id}"
# User profile model to hold phone number
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

# Address model to hold multiple addresses per user
class Address(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='addresses')
    address_line = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"Address for {self.user_profile.user.username}"

