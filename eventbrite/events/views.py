from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views import generic
from events.models import Event,EventLikes
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

class CreateEvent(LoginRequiredMixin,generic.CreateView):
    fields = ['name','description','date','time','location','image']
    model = Event

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class SingleEvent(generic.DetailView):
    model = Event

class ListEvents(generic.ListView):
    model = Event

class LikeEvent(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("events:single",kwargs={"slug": self.kwargs.get("slug")})
    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event,slug=self.kwargs.get("slug"))
        try:
            EventLikes.objects.create(user=self.request.user,event=event)
        except IntegrityError:
            messages.warning(self.request,"Already liked!")
        else:
            messages.success(self.request,"Added to liked events!")
        return super().get(request, *args, **kwargs)

class UnlikeEvent(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("events:single",kwargs={"slug": self.kwargs.get("slug")})
    def get(self, request, *args, **kwargs):
        try:
            event_likes = models.EventLikes.objects.filter(user=self.request.user,event__slug=self.kwargs.get("slug")).get()
        except models.EventLikes.DoesNotExist:
            messages.warning(self.request,"You never liked this event!")
        else:
            event_likes.delete()
            messages.success(self.request,"Removed from liked events!")
        return super().get(request, *args, **kwargs)

class UserEvents(LoginRequiredMixin, generic.ListView):
    model = models.Event
    template_name = "events/user_event_list.html"
    context_object_name = 'events'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class LikedEvents(LoginRequiredMixin, generic.ListView):
    model = models.EventLikes
    template_name = "events/liked_events.html"
    context_object_name = 'events'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
