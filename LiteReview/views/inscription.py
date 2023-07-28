from django.shortcuts import render, redirect

from LiteReview.utils.forms import UserModelForm


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
