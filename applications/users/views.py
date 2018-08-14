from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.urls import reverse

# Create your views here.


class LoginView(View):

    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        return redirect(reverse("fishes:admin_view"))


class FindPasswordView(View):

    def get(self, request):
        from .models import GrouperUser
        # for i in range(1,250):
        GrouperUser.objects.create_user(username='admin', password='admin', employeeID=0)
        return render(request, "users/forget_password.html")

    def post(self, request):
        return HttpResponse("change your password successfully!")


class Register(View):

    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        pass

