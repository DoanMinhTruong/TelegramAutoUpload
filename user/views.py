from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

# Create your views here.
class MyLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard_index')
    def get_success_url(self):
        return self.success_url
def login(request): 
    if request.user.is_authenticated: 
        return redirect('dashboard_index') 
    else: 
        return MyLoginView.as_view()(request)

def logout_v(request):
    logout(request)
    return redirect('/user/login/')
def reset_password(request):
    return render(request , 'base.html' , {})

def index(request):
    return render(request , 'base.html' , {})