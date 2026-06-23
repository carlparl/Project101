from django.db import models
from django.utils.text import slugify

class Tour(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    destination = models.CharField(max_length=150, default="Uganda")
    duration_days = models.PositiveIntegerField(default=1, help_text="Duration of the safari in days")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Cost in USD or UGX")
    short_description = models.TextField(max_length=300, default="")
    detailed_itinerary = models.TextField(default="")
    image = models.ImageField(upload_to='tours/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def location(self):
        """Fallback property mapping to destination for templates using tour.location."""
        return self.destination

    @property
    def duration(self):
        """Fallback property mapping to duration_days for templates using tour.duration."""
        return f"{self.duration_days} Days"


class BookingRequest(models.Model):
    package = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    travel_date = models.DateField()
    travelers = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Booking by {self.full_name} for {self.package.title}"


class Testimonial(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="testimonials")
    name = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.rating}/5)"


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    tour_selection = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    group_size = models.PositiveIntegerField(default=1, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - Itinerary Inquiry"


class Inquiry(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    tour_selection = models.CharField(max_length=250, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    group_size = models.PositiveIntegerField(default=1)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - Web Inquiry"