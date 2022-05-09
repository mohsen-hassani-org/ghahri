from django.contrib import admin
from .models import Career, CareerGroup

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'career_group')
    search_fields = ('name', 'career_group__name')
    list_filter = ('career_group', )

@admin.register(CareerGroup)
class CareerGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
