from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse

# authentication classes
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.models import User

# import models and forms
from order.models import Order
from account.models import User, Profile
from account.forms import SignUpForm, ProfileForm
from payment.forms import BillingAddressForm
from payment.models import BillingAddress

from django.shortcuts import redirect

# messages classes
from django.contrib import messages

from coupon.models import Message, Notification


def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "Happy Shopping!")
        return redirect('index')
    else:
        form = SignUpForm()
        if request.method == 'post' or request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()

                current_username = user.email
                current_user = user.id
                notific_obj = Notification.objects.get(user=current_user)
                instance = Message.objects.create(
                    message=f"Dear {current_username} Thanks For Registration to Cleveranfe.Com")
                instance.notification.add(notific_obj)

                messages.success(request, "Your account has been created successfully!")
                return HttpResponseRedirect(reverse('login'))
            else:
                messages.warning(request, "Server Problems please try again!")
                return HttpResponseRedirect(reverse('register'))

        context = {
            'form': form
        }
        return render(request, 'account/login.html', context)


def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, "You are Logged In!")
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "Shopping Unlimited with 25% off!")
                return redirect('index')
            else:
                messages.info(request, "Username OR Password is incorrect!")
    context = {
        'login_form': 'True'
    }
    return render(request, 'account/login.html', context)


@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(instance=profile)
        saved_address = BillingAddress.objects.get_or_create(user=request.user)
        saved_address = saved_address[0]
        billing_form = BillingAddressForm(instance=saved_address)
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                form = ProfileForm(instance=profile)
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {
            'orders': orders,
            'form': form,
            'billing_form': billing_form
        }
    except:
        messages.warning(request, "You haven't an active order!")
        return redirect('index')

    return render(request, 'account/dashboard.html', context)


@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "Login to your account.")
    return HttpResponseRedirect(reverse('index'))


@login_required
def is_read_notific(request):
    current_user = request.user.id
    notific_obj = Notification.objects.get(user=current_user)
    message_obj = Message.objects.filter(notification=notific_obj.id)[0]
    message_obj.notification.remove(notific_obj)
    return redirect('index')
