from LiteReview import models
from django import forms
from LiteReview.encrypt import md5
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class CreateTicketModelForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control"},
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control"},
            ),
            "image": forms.FileInput(
                attrs={"class": "form-control form-control-Sm"}
            ),
        }


class LoginModelForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "id": "floating-username", "placeholder": "1"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "floating-password", "placeholder": "5"}))

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        pwd = md5(pwd)
        return pwd


class UserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "floating-password-confirm",
                                          "placeholder": "confirm mot de passe"}),
        validators=[RegexValidator(r'^[A-Za-z\d@$!%*#?&]{8,}$', 'Mot de pass '
                                                                'n\'est pas '
                                                                'valide')], )

    # model form
    class Meta:
        model = models.User
        fields = ["username", "password", "confirm_password"]

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "id": "floating-username", "placeholder": "Nom d'utilisateur"},
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control", "id": "floating-password", "placeholder": "mot de passe"},
            ),
        }

    # hook method for encrypt password with md5
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        pwd_md5 = md5(pwd)
        return pwd_md5

    # hook method to validate if the input password is some as input confirm password
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm_pwd = self.cleaned_data.get("confirm_password")
        confirm_pwd = md5(confirm_pwd)
        if pwd != confirm_pwd:
            raise ValidationError("Le mot de passe n'est pas conforme")


class ReviewModelForm(forms.ModelForm):
    choices = [(0, '-0'), (1, '-1'), (2, '-2'), (3, '-3'), (4, '-4'), (5, '-5')]
    rating = forms.ChoiceField(choices=choices,
                               widget=forms.RadioSelect(attrs={"class": "form-check form-check-inline"}))

    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]
        widgets = {
            "headline": forms.TextInput(
                attrs={"class": "form-control"},
            ),
            "body": forms.Textarea(
                attrs={"class": "form-control"},
            ),
        }
