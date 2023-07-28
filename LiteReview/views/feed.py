from itertools import chain

from django.shortcuts import render

from LiteReview.models import Ticket, Review, User


def get_users_viewable_tickets(user):
    # get all the tickets of connecting user's followers who have makes
    ticket_objects = []

    user_followers = user.following.all()

    for user_follower in user_followers:
        tickets_object = Ticket.objects.filter(user_id=user_follower.followed_user_id).all()
        for ticket in tickets_object:
            ticket_objects.append(ticket)
    return ticket_objects


def get_users_viewable_reviews(user):
    # get all the reviews of connecting user's followers and also the review's of follower's ticket even the ticket is
    # not made by user's connecting followers
    review_object = []
    review_id = []
    user_followers = user.following.all()
    ticket_objects = get_users_viewable_tickets(user)

    for ticket_object in ticket_objects:
        # use ticket id to find all the related reviews
        reviews_object = Review.objects.filter(ticket_id=ticket_object.id).all()
        for review in reviews_object:
            review_object.append(review)
            review_id.append(review.id)

    for user_follower in user_followers:
        # get all the reviews of of connecting user's followers
        review_objects = Review.objects.filter(user_id=user_follower.followed_user_id).all()
        for review in review_objects:
            # check if the review is already get in the total review's list
            if review.id not in review_id:
                review_object.append(review)
                review_id.append(review.id)

    # get the connecting user's made reviews
    userself_reviews = Review.objects.filter(user_id=user.id).all()
    for userself_review in userself_reviews:
        # check if the review is already get in the total review's list
        if userself_review.id not in review_id:
            review_object.append(userself_review)
            review_id.append(userself_review.id)
    return review_object


def feed(request):
    flux_reviews = []
    flux_tickets = []
    reviews = get_users_viewable_reviews(User.objects.get(username=request.session.get("info")["username"]))
    user = User.objects.get(username=request.session.get("info")["username"])
    # returns queryset of reviews
    for review in reviews:
        if review:
            # give a attribute to separate review and ticket
            review.content_type = 'REVIEW'
            flux_reviews.append(review)

    tickets = get_users_viewable_tickets(User.objects.get(username=request.session.get("info")["username"]))

    # returns queryset of tickets
    for ticket in tickets:
        if ticket:
            ticket.content_type = 'TICKET'
            flux_tickets.append(ticket)

    # current user's made tickets
    tickets_user_connect = Ticket.objects.filter(user_id=user.id)
    for ticket_user_connect in tickets_user_connect:
        if ticket_user_connect:
            ticket_user_connect.content_type = 'TICKET'
            flux_tickets.append(ticket_user_connect)

    # combine and sort the two types of posts
    posts = sorted(chain(flux_reviews, flux_tickets), key=lambda post: post.time_created, reverse=True)
    return render(request, 'feed.html', context={'posts': posts})
