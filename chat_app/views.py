from django.views import View
from django.http import HttpResponse

# Create your views here.


# class chat(View):
#     def get(self, request):
#         return HttpResponse('hello', 200)

from django.shortcuts import render, redirect


def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat_app/chatPage.html", context)
