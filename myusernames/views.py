from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('newsapp:home')
    else:
        form = SignUpForm()
    return render(request, 'myusernames/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'myusernames/login.html'



from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def manual_logout(request):
    """
    Logs out the current user and redirects them to login page.
    Works with GET links (no 405 error).
    """
    logout(request)
    messages.success(request, "You've been logged out successfully 👋")
    return redirect('myusernames:login')

