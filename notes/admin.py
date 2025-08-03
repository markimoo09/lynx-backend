from django.contrib import admin
from .models import Note

class NoteAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'description', 'prompt', 'file_path', 'created_at', 'updated_at')
  list_filter = ('name', 'created_at')

# Register your models here.
admin.site.register(Note, NoteAdmin)
