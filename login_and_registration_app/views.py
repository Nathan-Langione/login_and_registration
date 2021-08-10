from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt
# Create your views here.

def index(request):
    return render(request,'index.html')

def success(request):
    try:
        if len(User.objects.filter(id=request.session['userid'])) > 0:
            pass
    except:
        return redirect("/")
    one_user = User.objects.get(id=request.session['userid'])
    context = {
        'this_user': one_user
        }
    return render(request,'success.html', context)

def register(request):
    if request.method=="POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST['password']
            birth_date = request.POST['birth_date']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
            request.session['userid'] = new_user.id
            return redirect("/success")


""" def login(request):
    if request.method=="POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
    else:
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/success')
    return redirect("/") """

def login(request):
    if request.method=="POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            user = User.objects.filter(email=request.POST['email'])
            if user:
                logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/success')
        return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")
