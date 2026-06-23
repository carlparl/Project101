from django import forms
from django.utils import timezone
from .models import Inquiry

class InquiryForm(forms.ModelForm):
    """Handles package reservation request validation, clean data processing, and premium styling."""
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'tour_selection', 'start_date', 'group_size', 'message']
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "premium-input", "placeholder": "John Doe"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "premium-input", "placeholder": "johndoe@example.com"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "premium-input", "placeholder": "+256 ..."}
            ),
            "tour_selection": forms.TextInput(
                attrs={"class": "premium-input", "readonly": "readonly"}
            ),
            "start_date": forms.DateInput(
                attrs={"class": "premium-input", "type": "date"}
            ),
            "group_size": forms.NumberInput(
                attrs={"class": "premium-input", "min": 1, "placeholder": "1"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "premium-input", 
                    "rows": 4, 
                    "placeholder": "Specify camera gear space requirements, dietary constraints, or tracking modifications..."
                }
            ),
        }

    def clean_start_date(self):
        """Validates that the requested safari departure timeline does not point to a past date."""
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