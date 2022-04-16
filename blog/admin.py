from django.contrib import admin

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'status', 'category', 'publish_date', 'author', 'slug', )
    list_display_links = ('title', )
    list_editable = ('status', 'category', )
    list_filter = ('publish_date', 'author', 'status', )
    search_fields = ('title', )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('name', 'post', 'publish_date', 'status')
    list_display_links = ('name', )
    list_editable = ('status', )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', )
    list_display_links = ('name', )


@admin.register(models.Tag)
class TagAdimn(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'slug')
    list_display_links = ('name', )
