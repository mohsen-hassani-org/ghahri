from django.contrib import admin
from .models import BigSlider, Feature

@admin.register(BigSlider)
class BigSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_publish', 'page', 'created_at', 'updated_at')
    list_filter = ('is_publish', 'page', 'created_at', 'updated_at')
    search_fields = ('title', 'page')
    readonly_fields = ('created_at', 'updated_at', 'image_tag')

    
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_publish', 'page', 'created_at', 'updated_at')
    list_filter = ('is_publish', 'page', 'created_at', 'updated_at')
    search_fields = ('title', 'page')
    readonly_fields = ('created_at', 'updated_at', 'thumbnail_tag')

