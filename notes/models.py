from django.db import models

# Create your models here.

class Note(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField()
  prompt = models.TextField()
  file_path = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
