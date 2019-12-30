from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView)
from .models import Ticket, Upvoted, Comments
from .forms import CommentForm

class BugListView(ListView):
    paginate_by = 5
    model = Ticket

    def get_queryset(self, *args, **kwargs):
        return Ticket.objects.filter(issue='Bug').order_by('-date_posted')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['type'] = 'Bugs'
        is_paginated = True
        return context


class UserBugListView(ListView):
    paginate_by = 5
    model = Ticket

    def get_queryset(self, *args, **kwargs):
        username = get_object_or_404(User, username=self.kwargs.get('username'))
        return Ticket.objects.filter(issue='Bug', username=username).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['type'] = 'Bugs'
        is_paginated = True
        return context


class FeaturesListView(ListView):
    paginate_by = 5
    model = Ticket

    def get_queryset(self, *args, **kwargs):
        return Ticket.objects.filter(issue='Feature').order_by('-date_posted')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['type'] = 'Features'
        is_paginated = True
        return context


class UserFeatureListView(ListView):
    paginate_by = 5
    model = Ticket

    def get_queryset(self, *args, **kwargs):
        username = get_object_or_404(User, username=self.kwargs.get('username'))
        return Ticket.objects.filter(issue='Feature', username=username).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['type'] = 'Features'
        is_paginated = True
        return context


class TicketDetailView(DetailView):
    model = Ticket


class TicketCreateView(LoginRequiredMixin ,CreateView):
    model = Ticket
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.username = self.request.user

        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.username = self.request.user

        return super().form_valid(form)

    def test_func(self):
        ticket = self.get_object()
        if self.request.user == ticket.username:
            return True
        return False


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = '/'

    def test_func(self):
        ticket = self.get_object()
        if self.request.user == ticket.username:
            return True
        return False


@login_required
def add_comment_to_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            print(request.user)
            comment.username = request.user
            comment.save()
            return redirect('tickets:detail', pk=ticket.pk)
    else:
        form = CommentForm()
    return render(request, 'tickets/comment_form.html', {'form': form})