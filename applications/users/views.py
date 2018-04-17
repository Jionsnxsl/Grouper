from django.shortcuts import render, HttpResponse
from django.views import View

# Create your views here.


class LoginView(View):

    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        return HttpResponse("in login post method")


class FindPasswordView(View):

    def get(self, request):
        return render(request, "users/forget_password.html")

    def post(self, request):
        return HttpResponse("change your password successfully!")