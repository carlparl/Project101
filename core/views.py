from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.core.mail import send_mail 
from .models import Tour, Inquiry
from .forms import InquiryForm

# 1. Main Landing Deck
def home(request):
    tours = Tour.objects.all()[:3] # Shows top 3 feature safaris on home page
    return render(request, 'core/home.html', {'tours': tours})

# 2. Exploration Deck (All Safaris Directory) 👈 RESTORED THIS FUNCTION
def tours_list(request):
    tours = Tour.objects.all()
    return render(request, 'core/tours_list.html', {'tours': tours})

# 3. Tour Detail view (e.g., /safaris/1/)
def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, 'core/tour_detail.html', {'tour': tour})

# 4. About Workspace View
def about(request):
    return render(request, 'core/about.html')

# 5. Operational Reservation Desk / Contact Form
def contact(request):
    tours = Tour.objects.all()
    
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            
            # Formatted email log dump for console execution
            email_subject = f"🚨 NEW EXPEDITION MANIFEST: {inquiry.name} - {inquiry.tour_selection or 'Custom Route'}"
            email_body = f"""
==================================================
        SHAFNET TOURS - LOGISTICS DISPATCH
==================================================
• Lead Client: {inquiry.name}
• Email Address: {inquiry.email}
• Mobile Line: {inquiry.phone or 'Not Provided'}
• Target Target: {inquiry.tour_selection or 'Custom Tailored Profile'}
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