from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from django import forms
from django.utils.deprecation import MiddlewareMixin

from LiteReview import models
from LiteReview.models import User, Ticket
from LiteReview.encrypt import md5


# def clean_
# Create your views here.
class auth_middleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info == '/login/' or request.path_info == '/inscription/':
            return
        status_login = request.session.get("info")
        if status_login:
            return
        else:
            return redirect('/login/')


class LoginModelForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "id": "floating-username", "placeholder": "1"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "floating-password", "placeholder": "5"}))

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        pwd = md5(pwd)
        return pwd


def login(request):
    form = LoginModelForm()
    if request.method == "POST":
        form = LoginModelForm(data=request.POST)
        if form.is_valid():
            user_object = models.User.objects.filter(**form.cleaned_data).first()
            if user_object:
                request.session["info"] = {"id": user_object.id, "username": user_object.username}
                return redirect('/dashboard/')
            else:
                form.add_error("password", "Le nom d'utilisateur ou le mot de passe n'est pas correct")

    return render(request, 'login.html', {"form": form})


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


def inscription(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "inscription.html", {"form": form})
    if request.method == "POST":
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        else:
            return render(request, "inscription.html", {"form": form})


def logout(request):
    request.session.clear()
    return redirect('/login/')


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


def create_ticket(request):
    form = CreateTicketModelForm()

    if request.method == "POST":
        form = CreateTicketModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            user = User.objects.get(username=request.session.get("info")["username"])
            ticket.user = user
            ticket.save()
            return redirect('/dashboard/')
    return render(request, 'create_ticket.html', {"form": form})


def dashboard(request):
    return render(request, 'dashboard.html')


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


def critique(request):
    if request.method == "POST":
        form_review = ReviewModelForm(data=request.POST)
        form_ticket = CreateTicketModelForm(data=request.POST, files=request.FILES)

        if form_review.is_valid() and form_ticket.is_valid():
            ticket = form_ticket.save(commit=False)
            ticket.user = User.objects.get(username=request.session.get("info")["username"])
            ticket.save()
            review = form_review.save(commit=False)
            review.user = User.objects.get(username=request.session.get("info")["username"])
            review.ticket = ticket
            review.save()

    form_review = ReviewModelForm()
    form_ticket = CreateTicketModelForm()

    context = {
        "review": form_review,
        "ticket": form_ticket
    }
    return render(request, 'critique.html', context)


def modifier_ticket(request, nid=10):
    obj = Ticket.objects.get(id=nid)
    data = CreateTicketModelForm(instance=obj)

    if request.method == "POST":
        ticket = CreateTicketModelForm(data=request.POST, files=request.FILES, instance=obj)
        if ticket.is_valid():
            ticket.user = User.objects.get(username=request.session.get("info")["username"])
            ticket.save()
            return redirect('/dashboard/')

    return render(request, "modifier_ticket.html", {"form": data})


def followers(request):
    # return render(request, "followers.html", {"followers": followers})
    return render(request, "followers.html")
