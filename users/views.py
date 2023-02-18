from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import login

# Create your views here.
from .forms import UserRegisterForm
from storage.models import settings


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            settings.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('games')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
