from django.urls import path, include
from . import views
from chat_app import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    # path('', views.chat.as_view(), name='chat'),
    path("", chat_views.chatPage, name="chat-page"),

    # login-section
    path("auth/login/", LoginView.as_view
         (template_name="chat_app/LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]
