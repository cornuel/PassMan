from django.shortcuts import  render, redirect
from .forms import NewUserForm, PassManForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import PassMan
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request=request, template_name='app/index.html')

def login(request):
    form = AuthenticationForm()
    errors = []
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main_page")
            else:
                errors = form.errors.values()
                messages.error(request,"Invalid username or password.")
        else:   
            errors = form.errors.values()
            messages.error(request,"Invalid username or password.")
    return render(request=request, template_name="app/login.html", context={"login_form":form, "errors":errors})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="app/register.html", context={"register_form":form})

def main(request):
    return render(request=request, template_name="app/main.html", context={})

def get_password(request):
    if request.user.is_authenticated:
        passwords = PassMan.objects.filter(user=request.user.id)
        data = []
        for password in passwords:
            password = password.to_json()
            data.append(password)
        return JsonResponse({'passwords': data})
    else:
        return redirect("index")

def save_password(request):
    if request.POST:
        form = PassManForm(request.POST)
        if form.is_valid():
            password = form.save()
            messages.success(request, "Password successfully saved.")
    form = PassManForm()
    return render(request=request, template_name="app/main.html", context={"save_form":form})
    
            
        
    