from django.contrib import admin
from .models import Tour, BookingRequest, Testimonial, ContactMessage, Inquiry

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'duration_days', 'price', 'is_featured')
    list_filter = ('is_featured', 'destination')
    search_fields = ('title', 'destination', 'short_description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'package', 'travel_date', 'travelers', 'created_at')
    list_filter = ('travel_date', 'created_at')
    search_fields = ('full_name', 'email', 'phone')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'tour', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'review')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'tour_selection', 'start_date', 'created_at')
    list_filter = ('start_date', 'created_at')
    search_fields = ('name', 'email', 'message')

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'tour_selection', 'start_date', 'created_at')
    list_filter = ('start_date', 'created_at')
    search_fields = ('name', 'email', 'message')