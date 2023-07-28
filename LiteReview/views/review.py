from django.shortcuts import render, redirect

from LiteReview.models import User, Review
from LiteReview.utils.forms import ReviewModelForm
from LiteReview.views.ticket import CreateTicketModelForm


def critique(request):
    # make a review by first make a ticket
    if request.method == "POST":
        # get user's input to make a ticket and review
        form_review = ReviewModelForm(data=request.POST)
        form_ticket = CreateTicketModelForm(data=request.POST, files=request.FILES)

        if form_review.is_valid() and form_ticket.is_valid():
            # if the data is valid by django,make a ticket but not write to the database for the moment
            ticket = form_ticket.save(commit=False)
            # add user informations to associate to the ticket form and write to the database
            ticket.user = User.objects.get(username=request.session.get("info")["username"])
            ticket.save()

            # add user informations to associate to the review form and write to the database
            review = form_review.save(commit=False)
            review.user = User.objects.get(username=request.session.get("info")["username"])
            review.ticket = ticket
            review.save()

    # render html form by using django's modelform
    form_review = ReviewModelForm()
    form_ticket = CreateTicketModelForm()

    context = {
        "review": form_review,
        "ticket": form_ticket
    }
    return render(request, 'critique.html', context)


def edit_review(request, nid):
    # edit current review
    obj = Review.objects.get(id=nid)
    obj_modelform = ReviewModelForm(instance=obj)

    if request.method == "POST":
        # make a review instance to carry the nid's review database information
        review = ReviewModelForm(data=request.POST, files=request.FILES, instance=obj)
        if review.is_valid():
            review.user = User.objects.get(username=request.session.get("info")["username"])
            review.save()
            return redirect('/posts/')

    return render(request, "modifier_critique.html", {"form": obj, "review_model_form": obj_modelform})


def delete_review(request):
    nid = request.GET.get('nid')
    Review.objects.filter(id=nid).delete()
    return redirect('/posts/')
