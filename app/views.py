import json
from django.shortcuts import  render, redirect
from .forms import NewUserForm, PassManForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import PassMan
from django.http import JsonResponse
from .generate_pass import generate_password
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

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

def generate_pass(request):
    generated_pass = generate_password();
    return JsonResponse({'generated_pass': generated_pass})

def delete_pass(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    logger.error(body)
    try:
        password = PassMan.objects.get(website=body["website"],
                       email=body["username"],
                       password=body["password"],
                       user=User(body["user_id"])
                       )
        password.delete()
    except PassMan.DoesNotExist:
        logger.error(f"Does not exist\n{body}")
    message_OK = 'Deleted'
    return JsonResponse({'message': message_OK})
    
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
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    logger.error(body)
    # password = PassMan(website = request.POST['website'],
    #         username = request.POST['username'],
    #         password = request.POST['password'],
    #         user = request.POST['user_id']
    # )
    new_password = PassMan(website=body["website"],
                       email=body["username"],
                       password=body["password"],
                       user=User(body["user_id"])
                       )
    new_password.save()
    messages.success(request, "Password successfully saved.")
    message_OK = 'Saved'
    return JsonResponse({'message': message_OK})
    return render(request=request, template_name="app/main.html", context={})