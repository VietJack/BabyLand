from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from shop.models import Customer, Cart

# Create your views here.

def login_user(request):
    login_form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            next_path = request.GET.get('next')
            if next_path:
                return redirect(next_path)
            return redirect('shop:home')
        else:
            return render(request, 'accounts/login.html', {'form':login_form, 'method':request.method})
    return render(request, 'accounts/login.html', {'form':login_form})


@login_required()
def logout_user(request):
    logout(request)
    return redirect(reverse('shop:home'))


def signup(request):
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            customer = Customer.objects.create(user=user)
            Cart.objects.create(customer=customer)
            return redirect(reverse('accounts:login'))
        else:
            return render(request, 'accounts/signup.html', {'form':signup_form, 'method':request.method})
    else:
        signup_form = UserCreationForm()
        return render(request, 'accounts/signup.html', {'form':signup_form, 'method':request.method})
