from django.contrib import admin
from .models import Blog, Comment, Category, Post

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Post)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name', 'slug')
    list_filter = ('slug',)
    prepopulated_fields = {'slug': ('name',)}
