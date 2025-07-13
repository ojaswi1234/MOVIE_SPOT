from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.
from .forms import RegisterUserForm
from django.contrib.auth import login

class Login(LoginView):
    template_name = "users/accounts/login.html"
    redirect_authenticated_user = True
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
    
    def get_success_url(self):
        return '/'
    
    

class Logout(LogoutView):
    next_page = "/"


class RegisterUser(FormView):
    template_name = "users/accounts/register.html"
    form_class= RegisterUserForm
    success_url = "/"

    
    def form_valid(self, form):
       user = form.save()
       login(self.request, user)

       return super().form_valid(form)
    

