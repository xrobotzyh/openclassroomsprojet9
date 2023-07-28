from itertools import chain

from django.shortcuts import render, redirect

from LiteReview.models import User, Ticket, Review


def user_posts(request):
    # to display user's self made tickets and reviews,method is the same as feed but more simple
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
