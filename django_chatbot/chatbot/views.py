from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone


openai_api_key = 'Your-Api-key'
openai.api_key = openai_api_key


def Ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    answer = response.choices[0].message.content.strip()
    return answer

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = Ask_openai(message)
        char = Chat(user=request.user, message=message, response=response,created_at=timezone.now())
        char.save()
        return JsonResponse({'message':message, 'response':response})
    return render(request,'chatbot.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try :
                user = User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request,user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
        else:
            error_message = 'password does not match'
            return render(request, 'register.html', {'error_message':error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)

def login(request):
    return render(request, 'login.html')