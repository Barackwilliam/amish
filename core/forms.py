from django import forms

from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    # Shamba la kuwatega bots. Mtu halisi haliwezi kuliona.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Enquiry
        fields = ["name", "phone", "email", "subject", "message", "division", "product"]
        labels = {
            "name": "Your name",
            "phone": "Phone number",
            "email": "Email address",
            "subject": "Subject",
            "message": "Your message",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"placeholder": "0700 000 000", "autocomplete": "tel"}),
            "email": forms.EmailInput(attrs={"placeholder": "Optional", "autocomplete": "email"}),
            "subject": forms.TextInput(attrs={"placeholder": "What do you need?"}),
            "message": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Tell us what you are looking for, "
                                                 "how much you need and when."},
            ),
            "division": forms.HiddenInput,
            "product": forms.HiddenInput,
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Your message could not be sent.")
        if not cleaned.get("phone") and not cleaned.get("email"):
            raise forms.ValidationError(
                "Please leave a phone number or an email address so that we can reply."
            )
        return cleaned
