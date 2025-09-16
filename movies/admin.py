from django.contrib import admin
from .models import Movie, Review, CheckoutFeedback

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

@admin.register(CheckoutFeedback)
class CheckoutFeedbackAdmin(admin.ModelAdmin):
    list_display = ['get_name_display', 'feedback_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'feedback']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_name_display(self, obj):
        return obj.name if obj.name else "Anonymous"
    get_name_display.short_description = 'Customer Name'
    
    def feedback_preview(self, obj):
        return obj.feedback[:100] + "..." if len(obj.feedback) > 100 else obj.feedback
    feedback_preview.short_description = 'Feedback Preview'

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)