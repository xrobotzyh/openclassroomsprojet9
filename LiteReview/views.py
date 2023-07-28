from itertools import chain

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.db.models import CharField, Value

from LiteReview import models
from LiteReview.models import User, Ticket, UserFollows, Review
from LiteReview.encrypt import md5


# def clean_
# Create your views here.
class auth_middleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info == '/index/' or request.path_info == '/inscription/':
            return
        status_login = request.session.get("info")
        if status_login:
            return
        else:
            return redirect('/index/')


class LoginModelForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "id": "floating-username", "placeholder": "1"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "floating-password", "placeholder": "5"}))

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        pwd = md5(pwd)
        return pwd


def index(request):
    form = LoginModelForm()
    if request.method == "POST":
        form = LoginModelForm(data=request.POST)
        if form.is_valid():
            user_object = models.User.objects.filter(**form.cleaned_data).first()
            if user_object:
                request.session["info"] = {"id": user_object.id, "username": user_object.username}
                return redirect('/feed/')
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
            return redirect('/index/')
        else:
            return render(request, "inscription.html", {"form": form})


def logout(request):
    request.session.clear()
    return redirect('/index/')


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


def modifier_ticket(request, nid):
    obj = Ticket.objects.get(id=nid)
    data = CreateTicketModelForm(instance=obj)

    if request.method == "POST":
        ticket = CreateTicketModelForm(data=request.POST, files=request.FILES, instance=obj)
        if ticket.is_valid():
            ticket.user = User.objects.get(username=request.session.get("info")["username"])
            ticket.save()
            return redirect('/dashboard/')

    return render(request, "modifier_ticket.html", {"form": data})


# todo 验证user_id和session id,如果是同一个人可以进行更改


def followers(request):
    if request.method == "GET":
        search_data = request.GET.get("query")
        user = User.objects.get(username=request.session.get("info")["username"])
        user_followers = user.following.all()
        users_followed_by = user.followed_by.all()
        if search_data:
            username_found = User.objects.filter(username__icontains=search_data)
            if username_found:
                if user_followers:
                    if users_followed_by:
                        return render(request, "followers.html",
                                      {"usernames_found": username_found, "show_table_username_found": True,
                                       "user_followers": user_followers, "show_table_user_followers": True,
                                       "users_followed_by": users_followed_by, "show_table_user_followed_by": True})
                    else:
                        return render(request, "followers.html",
                                      {"usernames_found": username_found, "show_table_username_found": True,
                                       "user_followers": user_followers, "show_table_user_followers": True,
                                       "show_table_user_followed_by": False})
                else:
                    return render(request, "followers.html",
                                  {"usernames_found": username_found, "show_table_username_found": True,
                                   "show_table_user_followers": False, "show_table_user_followed_by": False})
            else:
                messages.warning(request, 'Utilisateur non trouvé, Veuillez faire une nouvelle recherche')
                return redirect('/followers/')
        if user_followers:
            if users_followed_by:
                return render(request, "followers.html",
                              {"user_followers": user_followers, "show_table_user_followers": True,
                               "users_followed_by": users_followed_by, "show_table_user_followed_by": True})
            else:
                return render(request, "followers.html",
                              {"user_followers": user_followers, "show_table_user_followers": True,
                               "show_table_user_followed_by": False})

    return render(request, "followers.html", {"show_table_user_name_found": False, "show_table_user_followers": False})


def add_follower(request):
    nid = request.GET.get('nid')
    user_id = request.session.get('info')['id']
    UserFollows.objects.create(user_id=user_id, followed_user_id=nid)
    return redirect('/followers/')


def delete_follower(request):
    nid = request.GET.get('nid')
    UserFollows.objects.filter(id=nid).delete()
    return redirect('/followers/')


def get_users_viewable_tickets(user):
    ticket_objects = []
    user_followers = user.following.all()
    for user_follower in user_followers:
        tickets_object = Ticket.objects.filter(user_id=user_follower.followed_user_id).all()
        for ticket in tickets_object:
            ticket_objects.append(ticket)
    return ticket_objects


def get_users_viewable_reviews(user):
    review_object = []
    user_followers = user.following.all()
    ticket_objects = get_users_viewable_tickets(user)

    for ticket_object in ticket_objects:
        reviews_object = Review.objects.filter(ticket_id=ticket_object.id).all()
        for review in reviews_object:
            review_object.append(review)

    for user_follower in user_followers:
        review_objects = Review.objects.filter(user_id=user_follower.followed_user_id).all()
        for review in review_objects:
            review_object.append(review)
    return review_object


def feed(request):
    flux_reviews = []
    flux_tickets = []
    reviews = get_users_viewable_reviews(User.objects.get(username=request.session.get("info")["username"]))
    user = User.objects.get(username=request.session.get("info")["username"])
    reviews_user_connect = Review.objects.filter(user_id=user.id)
    # returns queryset of reviews
    for review in reviews:
        if review:
            review.content_type = 'REVIEW'
            flux_reviews.append(review)

    tickets = get_users_viewable_tickets(User.objects.get(username=request.session.get("info")["username"]))
    tickets_user_connect = Ticket.objects.filter(user_id=user.id)
    # returns queryset of tickets
    for ticket in tickets:
        if ticket:
            ticket.content_type = 'TICKET'
            flux_tickets.append(ticket)
    for ticket_user_connect in tickets_user_connect:
        if ticket_user_connect:
            ticket_user_connect.content_type = 'TICKET'
            flux_tickets.append(ticket_user_connect)
    # combine and sort the two types of posts
    posts = sorted(chain(flux_reviews, flux_tickets), key=lambda post: post.time_created, reverse=True)
    return render(request, 'feed.html', context={'posts': posts})


def user_posts(request):
    flux_reviews = []
    flux_tickets = []
    user = User.objects.get(username=request.session.get("info")["username"])
    tickets = Ticket.objects.filter(user_id=user.id)
    for ticket in tickets:
        if ticket:
            ticket.content_type = 'TICKET'
            flux_tickets.append(ticket)
    reviews = Review.objects.filter(user_id=user.id)
    for review in reviews:
        if review:
            review.content_type = "REVIEW"
            flux_reviews.append(review)
    posts = sorted(chain(flux_reviews, flux_tickets), key=lambda post: post.time_created, reverse=True)

    return render(request, 'posts.html', context={'posts': posts})


def delete_post(request):
    nid = request.GET.get('nid')
    Ticket.objects.filter(id=nid).delete()
    return redirect('/posts/')


def edit_review(request, nid):
    obj = Review.objects.get(id=nid)
    obj_modelform = ReviewModelForm(instance=obj)
    print(obj.user.username)

    if request.method == "POST":
        review = ReviewModelForm(data=request.POST, files=request.FILES, instance=obj)
        if review.is_valid():
            review.user = User.objects.get(username=request.session.get("info")["username"])
            review.save()
            return redirect('/dashboard/')

    return render(request, "modifier_critique.html", {"form": obj, "review_model_form": obj_modelform})


def delete_review(request):
    nid = request.GET.get('nid')
    Review.objects.filter(id=nid).delete()
    return redirect('/posts/')


def reply_ticket(request, nid):
    ticket_obj = Ticket.objects.filter(id=nid).first()
    review_model_form = ReviewModelForm()

    if request.method == "POST":
        review_form = ReviewModelForm(data=request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = User.objects.get(username=request.session.get("info")["username"])
            review.ticket = ticket_obj
            review.save()
        return redirect('/feed/')

    return render(request, 'reply_ticket.html', {"form": ticket_obj, "review_model_form": review_model_form})
