from django.shortcuts import render, redirect
from django.contrib import messages

from LiteReview.models import User, UserFollows


def followers(request):
    # render the follower's page by conditions
    if request.method == "GET":
        # get user's input data
        search_data = request.GET.get("query")
        user = User.objects.get(username=request.session.get("info")["username"])
        # get user's following people
        user_followers = user.following.all()
        # get user's followers
        users_followed_by = user.followed_by.all()
        if search_data:
            # fuzzy search the user's input data
            username_found = User.objects.filter(username__icontains=search_data)
            if username_found:
                if user_followers:
                    if users_followed_by:
                        # if user's data has a result and current user have followers and following people
                        return render(request, "followers.html",
                                      {"usernames_found": username_found, "show_table_username_found": True,
                                       "user_followers": user_followers, "show_table_user_followers": True,
                                       "users_followed_by": users_followed_by, "show_table_user_followed_by": True})
                    else:
                        # if user's data has a result and current user have followers but not have following people
                        return render(request, "followers.html",
                                      {"usernames_found": username_found, "show_table_username_found": True,
                                       "user_followers": user_followers, "show_table_user_followers": True,
                                       "show_table_user_followed_by": False})
                else:
                    # if user's data has a result and current user have no followers
                    return render(request, "followers.html",
                                  {"usernames_found": username_found, "show_table_username_found": True,
                                   "show_table_user_followers": False, "show_table_user_followed_by": False})
            else:
                # if user's data return a none obeject
                messages.warning(request, 'Utilisateur non trouvé, Veuillez faire une nouvelle recherche')
                return redirect('/followers/')
        if user_followers:
            # current user have following people and followers
            if users_followed_by:
                return render(request, "followers.html",
                              {"user_followers": user_followers, "show_table_user_followers": True,
                               "users_followed_by": users_followed_by, "show_table_user_followed_by": True})
            else:
                # current user have following people but not followers
                return render(request, "followers.html",
                              {"user_followers": user_followers, "show_table_user_followers": True,
                               "show_table_user_followed_by": False})

    return render(request, "followers.html", {"show_table_user_name_found": False, "show_table_user_followers": False})


def add_follower(request):
    # add follower by their user id
    nid = request.GET.get('nid')
    user_id = request.session.get('info')['id']
    # write to the database
    UserFollows.objects.create(user_id=user_id, followed_user_id=nid)
    return redirect('/followers/')


def delete_follower(request):
    # delete follower by their user id
    nid = request.GET.get('nid')
    # write to the database
    UserFollows.objects.filter(id=nid).delete()
    return redirect('/followers/')
