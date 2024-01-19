from rest_framework.generics import ListAPIView
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Message
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json
from django.conf import settings


# @csrf_protect
def loginPage(request):
    context = {
        'BASE_API_URL': settings.BASE_API_URL,
    }
    return render(request, 'chat_app/LoginPage.html', context)


def login_api(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body.decode('utf-8'))

            # Extract username and password from the data
            username = data.get('username', '')
            password = data.get('password', '')

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                login(request, user)

                # Return a JSON response indicating successful login
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def homePage(request, *args, **kwargs):
    context = {
        'BASE_API_URL': settings.BASE_API_URL,
    }
    return render(request, "chat_app/homePage.html", context)


def chatPage(request, *args, **kwargs):
    context = {
        'BASE_API_URL': settings.BASE_API_URL,
    }
    return render(request, "chat_app/chatPage.html", context)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


User = get_user_model()


class ChatPageView(LoginRequiredMixin, TemplateView):
    template_name = 'chatPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current user and the receiver
        current_user = self.request.user
        receiver = get_object_or_404(User, id=self.kwargs['user_id'])

        # Get or create the chat room
        sorted_ids = sorted([current_user.id, receiver.id])
        room_name = f"chat_{sorted_ids[0]}_{sorted_ids[1]}"

        # Retrieve messages for the chat room
        messages = Message.objects.filter(room_name=room_name)

        context['current_user'] = current_user
        context['receiver'] = receiver
        context['messages'] = messages

        return context
