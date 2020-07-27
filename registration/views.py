from django.core.mail import send_mail
from django.shortcuts import render

from .forms import UserCreationForm2


def send_reg_email(email, password):
    message = f"Your login: {email} \n Your password: {password}"
    send_mail(
        'Thank you for registration',
        message,
        'registration@bestshop.com',
        [email],
        fail_silently=False,
    )


# Create your views here.
def signup(request):
    template = 'registration/signup.html'
    if request.method == "POST":
        form = UserCreationForm2(request.POST)
        if form.is_valid():
            user = form.save()
            context = {"message": f"Пользователь {user} создан. "}
            send_reg_email(form.cleaned_data.get('email'), form.cleaned_data.get('password1 '))
        else:
            context = {"form": form}

    elif request.method == "GET":
        form = UserCreationForm2()
        context = {"form": form}
    else:
        context = {"message": "Запрос не поддерживается"}

    return render(
        request,
        template,
        context=context

    )
