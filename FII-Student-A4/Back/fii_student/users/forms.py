from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
# from django.contrib.auth.models import User
import django.forms.widgets

from .models import *
from .utils import validate_user_details
from personalise.constants import *


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=63, required=True, help_text="Prenume este obligatoriu")#, widget=forms.TextInput(attrs={'placeholder': 'Nume'}))
    last_name = forms.CharField(max_length=63, required=True, help_text="Numele este obligatoriu")#, widget=forms.TextInput(attrs={'placeholder': 'Prenume'}))
    email = forms.EmailField(max_length=254, help_text='Este necesara o adresa de email UAIC valida.')#, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    rol = forms.ChoiceField(choices=[(x, x) for x in ROLURI], required=True, help_text="")
    an_studiu = forms.ChoiceField(choices=[(x, x) for x in ANI_STUDIU])
    grupa = forms.ChoiceField(choices=[(x, x) for x in GRUPE])

    class Meta:
        model = FiiUser
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'email', 'rol', 'an_studiu', 'grupa')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        # self.fields['password1'].widget.attrs.update({'placeholder': 'Parola'})
        # self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmă parola'})
        # self.fields['rol'].widget.attrs.update({'': 'Selecteaza rolul'})

    def clean(self):
        validation_errs = validate_user_details(self.cleaned_data)
        if validation_errs is not None:
            self.add_error("grupa", validation_errs)
            raise forms.ValidationError(validation_errs)
        return self.cleaned_data


class SettingsForm(forms.Form):
    first_name = forms.CharField(max_length=63, required=False, help_text="Prenume")
    last_name = forms.CharField(max_length=63, required=False, help_text="Numele")
    email = forms.EmailField(max_length=254, required=False, help_text='Este necesara o adresa de email UAIC valida.')
    rol = forms.ChoiceField(choices=[(x, x) for x in ROLURI])
    an_studiu = forms.ChoiceField(choices=[(x, x) for x in ANI_STUDIU])
    grupa = forms.ChoiceField(choices=[(x, x) for x in GRUPE])
    navbar_color = forms.ChoiceField(choices=[(x, x) for x in FLAT_CHOICES])
    background_first = forms.ChoiceField(choices=[(x, x) for x in BACKGROUND_CHOICES['FIRST']])
    background_second = forms.ChoiceField(choices=[(x, x) for x in BACKGROUND_CHOICES['SECOND']])
    color1_first = forms.ChoiceField(choices=[(x, x) for x in ELEMENT_CHOICES['FIRST']])
    color1_second = forms.ChoiceField(choices=[(x, x) for x in ELEMENT_CHOICES['SECOND']])
    color2_first = forms.ChoiceField(choices=[(x, x) for x in ELEMENT_CHOICES['FIRST']])
    color2_second = forms.ChoiceField(choices=[(x, x) for x in ELEMENT_CHOICES['SECOND']])
    # accent_color = forms.CharField(max_length=255)
    font_color = forms.ChoiceField(choices=[(x, x) for x in FONT_COLOR_CHOICES])
    font_family = forms.ChoiceField(choices=[(x, x) for x in FONT_FAMILY_CHOICES])

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        # self.fields["navbar_color"].widget.attrs.update({'type': 'color'})
        # self.fields["background_color"].widget.attrs.update({'type': 'color'})
        # self.fields["accent_color"].widget.attrs.update({'type': 'color'})
        # self.fields["font_color"].widget.attrs.update({'type': 'color'})
#
# class LoginForm(AuthenticationForm):
#
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#
#     def __init__(self, *args, **kwargs):
#         super(LoginForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'class': 'form-control'})
#         self.fields['password'].widget.attrs.update({'class': 'form-control'})