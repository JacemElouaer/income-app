from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.mail import EmailMessage


# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # get the data
        # Validate
        # create a user account
        context = {
            'validField': request.POST
        }
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'password too short');
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                email_subject = "activate your  account "
                email_body = ""
                email = EmailMessage(
                    email_subject,
                    email_body,

                    'jassemelwaar@gmail.com',
                    [email],
                )
                email.fail_silently = False
                email.send()
                user.save();
                messages.success(request, 'user created successful');
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')

        # messages.success(request , "Registration was successfully :) ")
        # return  render(request,'authentication/register.html')


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({"username_error": "username should only contain alphanumeric characters"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "sorry username already used"}, status=409)
        return JsonResponse({"username_valid": True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        print(email)
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"email_error": "this email is invalid  !! "}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "sorry email already used"}, status=409)
        return JsonResponse({"email_valid": True})


class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('login')
