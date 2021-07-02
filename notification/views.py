from django.shortcuts import render, redirect
from notification.models import Notification

def seen_notify(request):
    notify = Notification.objects.filter(user=request.user)
    for notification in notify:
        notification.is_seen = True
        notification.save()
    return redirect('index')
