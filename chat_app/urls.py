from django.urls import path, include
from . import views
from chat_app import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    # path('', views.chat.as_view(), name='chat'),
    path("", chat_views.loginPage, name="login-page"),
    path("home-page/", chat_views.homePage, name="home-page"),
    path("chat-page/", chat_views.chatPage, name="chat-page"),

    # login-section
    # path("auth/login/", LoginView.as_view(template_name="chat_app/LoginPage.html"),
    #      name="login-user"),
    path('login_API/', views.login_api, name='login_api'),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path('api/users/', views.UserListView.as_view(), name='user-list'),
    path('chat/<int:user_id>/', views.ChatPageView.as_view(), name='chat_page'),


]
