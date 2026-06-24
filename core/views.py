import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail 
from .models import Tour
from .forms import InquiryForm

# Initialize a logger for backend monitoring
logger = logging.getLogger(__name__)

def home(request):
    """Main Landing Deck - Pulls the top 3 featured safaris efficiently."""
    
    # ADVANCEMENT: The original code didn't actually filter by "featured". 
    # This now targets the `is_featured` boolean you set up in your models, 
    # and sorts by newest first.
    tours = Tour.objects.filter(is_featured=True).only(
        'id', 'title', 'image', 'price', 'destination', 'duration_days'
    ).order_by('-created_at')[:3]
    
    # Fallback: If no tours are explicitly marked as featured, just grab the latest 3
    if not tours.exists():
        tours = Tour.objects.all().only(
            'id', 'title', 'image', 'price', 'destination', 'duration_days'
        ).order_by('-created_at')[:3]

    return render(request, 'core/home.html', {'tours': tours})

def tours_list(request):
    """Exploration Deck - Displays the entire safari package directory."""
    
    # ADVANCEMENT: Added .only() to prevent loading massive `detailed_itinerary` 
    # text blocks into RAM for every single tour when rendering the list view.
    tours = Tour.objects.all().only(
        'id', 'title', 'image', 'price', 'destination', 'duration_days', 'short_description'
    ).order_by('-created_at')
    
    return render(request, 'core/tours_list.html', {'tours': tours})

def gallery_view(request):
    return render(request, 'core/gallery.html')

def tour_detail(request, tour_id):
    """Tour Detail View - Displays a deep-dive route manifest for a specific package."""
    
    # ADVANCEMENT: Used prefetch_related('testimonials'). 
    # If your template loops through testimonials for this tour, this prevents 
    # the dreaded N+1 Query problem (hammering your database with a new query for every review).
    tour = get_object_or_404(
        Tour.objects.prefetch_related('testimonials'), 
        id=tour_id
    )
    
    return render(request, 'core/tour_detail.html', {'tour': tour})

def about(request):
    """About Workspace View."""
    return render(request, 'core/about.html')

def contact(request):
    """Operational Reservation Desk - Handles dynamic custom safari bookings and inquiries."""
    tours = Tour.objects.all().only('title')
    
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            # Data is saved to the database (Inquiry model)
            inquiry = form.save()
            
            # Formatted email log template for operational dispatch
            email_subject = f"🚨 NEW EXPEDITION MANIFEST: {inquiry.name} - {inquiry.tour_selection or 'Custom Route'}"
            email_body = f"""
==================================================
        SHAFNET TOURS - LOGISTICS DISPATCH
==================================================
• Lead Client: {inquiry.name}
• Email Address: {inquiry.email}
• Mobile Line: {inquiry.phone or 'Not Provided'}
• Target Safari: {inquiry.tour_selection or 'Custom Tailored Profile'}
• Transit Start: {inquiry.start_date or 'Flexible Schedule'}
• Group Count: {inquiry.group_size} Traveler(s)

[Special Constraints / Provisions]
{inquiry.message}
==================================================
"""
            # ADVANCEMENT: Added Fault Tolerance (Try/Except). 
            # If your email server goes down, the form will still save to the database, 
            # and the user won't get a scary '500 Server Error' page.
            try:
                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email='operations@shafnettours.com',
                    recipient_list=['info@shafnettours.com'],
                    fail_silently=False,
                )
                messages.success(request, "Your expedition manifest has been successfully captured! Our dispatch team will contact you shortly.")
            except Exception as e:
                # Log the error for the dev team, but still tell the user it was successful 
                # (because we successfully saved it to the DB panel).
                logger.error(f"SMTP Email Failure for Inquiry ID {inquiry.id}: {str(e)}")
                messages.success(request, "Your expedition manifest has been secured! We will review your constraints and reach out soon.")
            
            return redirect('contact')
            
        else:
            # ADVANCEMENT: Catch invalid form submissions and alert the user.
            messages.error(request, "There was an issue with your manifest. Please review the highlighted fields below.")
    else:
        form = InquiryForm()

    context = {
        'form': form,
        'tours': tours
    }
    return render(request, 'core/contact.html', context)