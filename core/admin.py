from django.contrib import admin
from .models import (
    Tour,  # Normalized name to eliminate the ImportError
    BookingRequest,
    ContactMessage,
    GalleryImage,
    Inquiry,
    Testimonial,
)

class GalleryImageInline(admin.TabularInline):
    """Allows multi-image uploading directly inside the Tour edit page."""
    model = GalleryImage
    extra = 3  # Generates 3 empty slots by default for fast uploads
    fields = ["title", "image"]


class TestimonialInline(admin.StackedInline):
    """Displays related client reviews at the bottom of the Tour page."""
    model = Testimonial
    extra = 0
    classes = ["collapse"]  # Keeps them neatly tucked away until clicked


from django.contrib import admin
from .models import Tour

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'duration_days', 'price', 'is_featured')
    list_filter = ('destination', 'is_featured')
    search_fields = ('title', 'destination')
    prepopulated_fields = {'slug': ('title',)}
    
@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone",
        "package",
        "travel_date",
        "travelers",
        "created_at",
    )
    search_fields = (
        "full_name",
        "email",
        "phone",
        "package__title",
    )
    list_filter = (
        "travel_date",
        "created_at",
    )
    ordering = (
        "-created_at",
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Displays the custom safari metrics collected by your 
    itinerary form, completely replacing the obsolete subject field.
    """
    list_display = (
        "name",
        "email",
        "phone",
        "tour_selection",
        "start_date",
        "group_size",
        "created_at",
    )
    search_fields = (
        "name",
        "email",
        "phone",
        "tour_selection",
    )
    list_filter = (
        "start_date",
        "created_at",
    )
    ordering = (
        "-created_at",
    )
    # Keep your existing TourAdmin configuration here...

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    # Change 'tour_package' to 'tour_selection' here 
    list_display = ('name', 'email', 'phone', 'tour_selection', 'created_at')
    list_filter = ('tour_selection', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)