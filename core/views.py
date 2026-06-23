from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail 
from .models import Tour
from .forms import InquiryForm

def home(request):
    """Main Landing Deck - Pulls the top 3 featured safaris efficiently."""
    tours = Tour.objects.all().only('id', 'title', 'image', 'price', 'location', 'duration')[:3]
    return render(request, 'core/home.html', {'tours': tours})

def tours_list(request):
    """Exploration Deck - Displays the entire safari package directory."""
    tours = Tour.objects.all()
    return render(request, 'core/tours_list.html', {'tours': tours})

def tour_detail(request, tour_id):
    """Tour Detail View - Displays a deep-dive route manifest for a specific package."""
    tour = get_object_or_404(Tour, id=tour_id)
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
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email='operations@shafnettours.com',
                recipient_list=['info@shafnettours.com'],
                fail_silently=False,
            )

            messages.success(request, "Your expedition manifest has been successfully captured!")
            return redirect('contact')
    else:
        form = InquiryForm()

    context = {
        'form': form,
        'tours': tours,
    }
    return render(request, 'core/contact.html', context)