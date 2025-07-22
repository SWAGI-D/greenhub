from django.contrib import admin
from .models import Post, Comment, Like, Question

class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'caption', 'timestamp']
    search_fields = ['caption', 'user__username']
    list_filter = ['timestamp']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Question)
