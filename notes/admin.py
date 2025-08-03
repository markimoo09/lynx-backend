from django.contrib import admin
from .models import Note

class NoteAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'description', 'prompt', 'file_path', 'created_at', 'updated_at')
  list_filter = ('name', 'created_at')
  search_fields = ('name',)
  ordering = ('-created_at',)
  readonly_fields = ('created_at', 'updated_at')
  fieldsets = (
    (None, {'fields': ('name', 'description', 'prompt', 'file_path')}),
    ('Dates', {'fields': ('created_at', 'updated_at')}),
  )

# Register your models here.
admin.site.register(Note, NoteAdmin)
