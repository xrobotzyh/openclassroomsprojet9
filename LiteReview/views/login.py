from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin

from LiteReview import models
from LiteReview.utils.forms import LoginModelForm


# make a condition that only the authorized connecting user can visit divers page of the site
class auth_middleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info == '/index/' or request.path_info == '/inscription/':
            return
        status_login = request.session.get("info")
        # check the session info is none or not
        if status_login:
            return
        else:
            return redirect('/index/')


def index(request):
    form = LoginModelForm()
    if request.method == "POST":
        form = LoginModelForm(data=request.POST)
        if form.is_valid():
            # using the user's input data to find in the database if there is user info correspond this data
            user_object = models.User.objects.filter(**form.cleaned_data).first()
            if user_object:
                # if there is, make a session info to be used later
                request.session["info"] = {"id": user_object.id, "username": user_object.username}
                return redirect('/feed/')
            else:
                # if there is not have, error message
                form.add_error("password", "Le nom d'utilisateur ou le mot de passe n'est pas correct")

    return render(request, 'login.html', {"form": form})
