from django import forms
from .models import Category, Listing


class CreateNewListingForm(forms.ModelForm):
    title = forms.CharField(label="New Listing", max_length=100)
    description = forms.CharField(
        label="Description",
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                "class": "content_field",
                "type": "text"
            }
        )
    )
    min_starting_bid = forms.DecimalField()
    pic_url = forms.CharField(label="Photo URL", max_length=1000, required=False)
    category = forms.ModelChoiceField(
        label="Category", queryset=Category.objects.all(), required=False
    )
    class Meta:
        model = Listing
        exclude = ["user", "pic"]
