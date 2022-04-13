from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'status', 'publish_date', 'author', 'slug', )
    list_display_links = ('title', )
    list_editable = ('status',)
    list_filter = ('publish_date', 'author', 'status', )
    search_fields = ('title', )

