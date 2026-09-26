from django.contrib import admin
from .models import ReviewModel
# Register your models here.

@admin.register(ReviewModel)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "rate", "created_date", "status"]
    list_filter = ["status"]
    
