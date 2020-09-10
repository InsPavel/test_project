from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, UserDetailView, UserPasswordChangeView, UserListView, UserDeleteView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/list/', UserListView.as_view(), name='user_list'),
    path('create/user/', RegisterView.as_view(), name='create_user'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('user/<int:pk>/password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
