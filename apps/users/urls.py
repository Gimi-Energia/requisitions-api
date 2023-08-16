from django.urls import path

from apps.users.views import UsersList, UsersDetail

urlpatterns = [
    path("api/users/", UsersList.as_view(), name="users-list"),
    path("api/users/<str:pk>/", UsersDetail.as_view(), name="users-detail"),
]
