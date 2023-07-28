from django.shortcuts import render, redirect
from django.contrib import messages


from LiteReview.models import User, Ticket, Review
from LiteReview.utils.forms import CreateTicketModelForm, ReviewModelForm


def create_ticket(request):
    form = CreateTicketModelForm()

    if request.method == "POST":
        form = CreateTicketModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            user = User.objects.get(username=request.session.get("info")["username"])
            ticket.user = user
            ticket.save()
            return redirect('/posts/')
    return render(request, 'create_ticket.html', {"form": form})


def modifier_ticket(request, nid):
    obj = Ticket.objects.get(id=nid)
    data = CreateTicketModelForm(instance=obj)

    if request.method == "POST":
        ticket = CreateTicketModelForm(data=request.POST, files=request.FILES, instance=obj)
        if ticket.is_valid():
            ticket.user = User.objects.get(username=request.session.get("info")["username"])
            ticket.save()
            return redirect('/posts/')

    return render(request, "modifier_ticket.html", {"form": data})


def reply_ticket(request, nid):
    # reply a ticket
    current_ticket_id = []
    ticket_obj = Ticket.objects.filter(id=nid).first()
    review_model_form = ReviewModelForm()

    if request.method == "POST":
        review_form = ReviewModelForm(data=request.POST)

        if review_form.is_valid():
            # get the ticket database information to see if the current user's id has already reply the current ticket
            # if so, give a error message otherwise reply ticket to the database
            current_ticket_reviews = Review.objects.filter(ticket_id=nid).all()
            for current_ticket_review in current_ticket_reviews:
                current_ticket_id.append(current_ticket_review.user_id)
            if request.session.get('info')['id'] not in current_ticket_id:
                review = review_form.save(commit=False)
                review.user = User.objects.get(username=request.session.get("info")["username"])
                review.ticket = ticket_obj
                review.save()
                return redirect('/feed/')
            messages.warning(request, 'Vous ne pouvez plus laisser une commentaire sur cet livre')
            # return to the current page
            return redirect(request.get_full_path())
        return redirect('/feed/')

    return render(request, 'reply_ticket.html', {"form": ticket_obj, "review_model_form": review_model_form})
