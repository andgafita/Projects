from django import forms
from .models import Resources


class ResourcesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ResourcesForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Resources



