from django.shortcuts import render, HttpResponse, redirect
from django import forms

from LiteReview import models


# Create your views here.
def index(request):
    if request.method == "POST":
        pass
    return render(request, 'index.html')


class UserModelForm(forms.ModelForm):
    class Meta
        model = models.Userinfo
        fields = [""]
def inscription(request):
    return render(request, "inscription.html")
