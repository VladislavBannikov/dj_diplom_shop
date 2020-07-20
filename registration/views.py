from django.shortcuts import render

from .forms import UserCreationForm2


# Create your views here.
def signup(request):
    template = 'registration/signup.html'
    if request.method == "POST":
        form = UserCreationForm2(request.POST)
        if form.is_valid():
            user = form.save()
            context = {"message": f"Пользователь {user} создан. "}
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
