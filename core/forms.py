from django import forms
from django.utils import timezone
from .models import BookingRequest, ContactMessage, Inquiry



class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'tour_selection', 'start_date', 'group_size', 'message']
class BookingRequestForm(forms.ModelForm):
    """Handles package-specific reservation request validation and styling."""
    class Meta:
        model = BookingRequest
        fields = [
            "full_name",
            "email",
            "phone",
            "travel_date",
            "travelers",
            "special_requests",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Full Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number",
                }
            ),
            "travel_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "travelers": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "Number of Travelers",
                }
            ),
            "special_requests": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Any specific requests or requirements? (Optional)",
                }
            ),
        }

    def clean_travel_date(self):
        """Validates that the selected travel date is not set in the past."""
        travel_date = self.cleaned_data.get("travel_date")
        if travel_date and travel_date < timezone.now().date():
            raise forms.ValidationError("Travel date cannot be in the past.")
        return travel_date

    def clean_travelers(self):
        """Validates that the headcount configuration is at least 1 person."""
        travelers = self.cleaned_data.get("travelers")
        if travelers is not None and travelers < 1:
            raise forms.ValidationError("You must register at least 1 traveler.")
        return travelers


class ContactForm(forms.ModelForm):
    """Handles the custom itinerary generation inquiry form validation and styling."""
    class Meta:
        model = ContactMessage
        fields = [
            "name", 
            "email", 
            "phone", 
            "tour_selection", 
            "start_date", 
            "group_size", 
            "message"
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control-premium", "placeholder": "John Doe"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control-premium", "placeholder": "johndoe@example.com"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control-premium", "placeholder": "+256 ..."}
            ),
            "tour_selection": forms.Select(
                attrs={"class": "form-select form-control-premium"}
            ),
            "start_date": forms.DateInput(
                attrs={"class": "form-control-premium", "type": "date"}
            ),
            "group_size": forms.NumberInput(
                attrs={"class": "form-control-premium", "min": 1, "placeholder": "1"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control-premium", 
                    "rows": 5, 
                    "placeholder": "Specify packing needs, vehicle preferences, camera gear space, or physical limitations..."
                }
            ),
        }

    def clean_start_date(self):
        """Validates that the requested safari startup timeline does not point to a past date."""
        start_date = self.cleaned_data.get("start_date")
        if start_date and start_date < timezone.now().date():
            raise forms.ValidationError("Your expedition departure date cannot be in the past.")
        return start_date

    def clean_group_size(self):
        """Validates that the safari track group contains at least one traveler."""
        group_size = self.cleaned_data.get("group_size")
        if group_size is not None and group_size < 1:
            raise forms.ValidationError("Group size must be at least 1 client.")
        return group_size