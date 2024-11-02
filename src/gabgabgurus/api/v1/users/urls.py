from django.urls import path

from gabgabgurus.api.v1.users import views

app_name = "users"

urlpatterns = [
    path("", views.MemberListView.as_view(), name="list"),
    path("last-activity/", views.UserLastActivityView.as_view(), name="presence"),
    path("<int:pk>/", views.MemberDetailView.as_view(), name="detail"),
    path("iam/", views.IAmView.as_view(), name="iam"),
    path("me/", views.MyProfileView.as_view(), name="me"),
    path("me/avatar/", views.MyAvatarUpdateView.as_view(), name="me_avatar"),
    path("me/languages/", views.MyLanguagesUpdateView.as_view(), name="me_languages"),
    path("me/blocked-users/", views.MyBlockedUsersUpdateView.as_view(), name="me_blocked_users"),
    path("feedback/", views.FeedbackView.as_view(), name="feedback"),
]
