from django import forms
from django.utils import timezone

from .models import BookingRequest, ContactMessage, Inquiry


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = [
            "name",
            "email",
            "phone",
            "tour_selection",
            "start_date",
            "group_size",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "John Doe",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "johndoe@example.com",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+256 ...",
                }
            ),
            "tour_selection": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "group_size": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "1",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": (
                        "Tell us about your preferred destinations, "
                        "accommodation level, activities, dietary "
                        "requirements, or any special requests..."
                    ),
                }
            ),
        }


class BookingRequestForm(forms.ModelForm):
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
                    "placeholder": (
                        "Any special accommodation, transport, "
                        "dietary, or activity requests?"
                    ),
                }
            ),
        }

    def clean_travel_date(self):
        travel_date = self.cleaned_data.get("travel_date")

        if travel_date and travel_date < timezone.now().date():
            raise forms.ValidationError(
                "Travel date cannot be in the past."
            )

        return travel_date

    def clean_travelers(self):
        travelers = self.cleaned_data.get("travelers")

        if travelers is not None and travelers < 1:
            raise forms.ValidationError(
                "You must register at least 1 traveler."
            )

        return travelers


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage

        fields = [
            "name",
            "email",
            "phone",
            "tour_selection",
            "start_date",
            "group_size",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "John Doe",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "johndoe@example.com",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+256 ...",
                }
            ),
            "tour_selection": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "group_size": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "1",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": (
                        "Tell us about your preferred destinations, "
                        "accommodation style, activities, dietary "
                        "requirements, or any special requests..."
                    ),
                }
            ),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")

        if start_date and start_date < timezone.now().date():
            raise forms.ValidationError(
                "Departure date cannot be in the past."
            )

        return start_date

    def clean_group_size(self):
        group_size = self.cleaned_data.get("group_size")

        if group_size is not None and group_size < 1:
            raise forms.ValidationError(
                "Group size must be at least 1 traveler."
            )

        return group_size