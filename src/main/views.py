from django.shortcuts import render, redirect,render_to_response
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

from .models import Tutorial
from .forms import UserCreateForm
from uuid import uuid1
import requests
import os, sys



# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name='main/home.html',
                  context = {"tutorials":Tutorial.objects.all})


def form(request):
    if request.method == "POST":
        return redirect("main:homepage")

    uvi = str(uuid1())
    form_link = "https://theaicademy.typeform.com/to/DFq2iT?visitor_uuid="+uvi

    response = render(request= request, template_name = "main/form.html",
                          context={"form_link":form_link})

    response.set_cookie('visitor_uuid', uvi)
    os.makedirs('/tmp/uploads/'+ uvi  )
    return  response

import json
from subprocess import check_output
token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1UTkJRamhFUmpZd05VRXlRakpFUkRGRk5rSXpPRGc0T0RZMlFqWTNSamd3TURoRVFUVTROZyJ9.eyJpc3MiOiJodHRwczovL2F1dGgudmlkZW9hc2suaXQvIiwic3ViIjoiYXV0aDB8NWRhMWY2NWQxMzAzYTkwZTIxMWY0OWViIiwiYXVkIjpbImh0dHBzOi8vYXBpLnZpZGVvYXNrLml0LyIsImh0dHBzOi8vdmlkZW9hc2suZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU3MDkzNDY2OCwiZXhwIjoxNTcxMDIxMDY4LCJhenAiOiJ6TjJ3R2hxOVBta2xQUEIzTVRSYTA4T3BKTkdvdUVLQSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgb2ZmbGluZV9hY2Nlc3MifQ.lLzAEefiaEPk1N19jJSNUYjZOw0c5EKcdbLH01fJ-BAnXNMqVEGzzUFtQJRzkH27YOv8kXyoTkpoYnmk6bxxwywe1fVcMpzFYvdcdhu1wT3NRliXJeWQpZEsns2jdNQq_kJEbAKBpz-OcAZ8hHKnYjLRLhNL-PuMv6Cnw3_Ca7dTOkrHBmKqAnIHcYywlIzbY1tkrBdvLySOCzAfYktURSf6P5G26c6CeUI7g4a5L3YSPIYQAlq_4ZJRdQlodBMS4y0PWCDPiFRyLTYO-CUXYiImC3dg6qlECFIocvFtXyeeScVRtyfTG_4ddQzlqDoicWZLbtzTJi-DOYlXbP3fjg"
def result(request):
    if request.method == "POST":
        return redirect("main:homepage")
    if 'visitor_uuid' in request.COOKIES:
        uvi = request.COOKIES['visitor_uuid']
        r = requests.get('https://api.videoask.it/questions/89dae0ef-f42d-466e-98c4-d072525dabfd/answers', headers={"Authorization": token}) 
        data = json.loads(r.content)
        print(data)
        video_link = data[0]["media_url"]
        out = check_output(["python", "./asl.py", "--url", video_link, "--name", "video1", "--output", uvi])
        frames = os.listdir('/tmp/uploads/'+uvi)
        return render(request=request, template_name = "main/result.html", context={"frames":frames})



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

