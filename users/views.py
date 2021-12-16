import datetime
import os

from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView
from django.contrib.auth import login, authenticate, logout
from dotenv import load_dotenv
load_dotenv()

from main_app.models import Category, Item
from .models import User
from users.forms import RegistrationForm, UserCreateForm, UserUpdateForm


def registration_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(email=email, password=raw_password)
                login(request, user)
                messages.info(request, 'You have registered and are now logged in!')
                return redirect('main')
            else:
                context['registration_form'] = form
        else:
            form = RegistrationForm()
            context['registration_form'] = form
        return render(request, 'users/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('main')

def demo_user_login_view(request):
    demo_user = authenticate(email=str(os.getenv('LOGIN_DEMO_KEYS')), password=str(os.getenv('PASSWORD_DEMO_KEYS')))
    login(request, demo_user)
    return redirect('main')

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    context_object_name = 'user'
    success_url = '/'

    def get_success_url(self):
        return reverse_lazy('user_update', args=(self.object.slug,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def test_func(self):
        # user must be Admin, or you can only see your own account
        if self.request.user.account_type == 'Admin' or self.request.user.slug == self.kwargs['slug']:
            return True
        else:
            return False


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'user'

    def test_func(self):
        # user must be Admin, or you can only see your own account. Also, same company.
        if (self.request.user.account_type == 'Admin' or self.request.user.slug == self.kwargs['slug']) and \
                self.request.user.company == self.get_object().company:
            return True
        else:
            return False

    # showing 404 instead of 403 for security's sake
    def handle_no_permission(self):
        raise Http404('You have no permission to view this page')

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        now = datetime.datetime.now()
        context['timeout'] = datetime.datetime.now()

        if self.request.user.company is not None:
            # ADMIN (w/ company)
            if self.request.user.account_type == 'Admin':
                context['category_list'] = Category.objects.filter(category_author__company=self.request.user.company)
            # AGENT (w/ company)
            elif self.request.user.account_type == 'Agent':
                context['category_list'] = Category.objects.filter(Q(
                    category_author__company=self.request.user.company) & (Q(
                    item__assigned_to=self.request.user) | Q(item__author=self.request.user))).distinct()

            context['tasks'] = Item.objects.filter(Q(assigned_to__slug=self.kwargs['slug']) | Q(
                author__slug=self.kwargs['slug'])).distinct()

            context['tasks_complete'] = Item.objects.filter(
                Q(complete=True) & (Q(assigned_to__slug=self.kwargs['slug']) | Q(
                    author__slug=self.kwargs['slug']))).distinct()
            context['tasks_ongoing'] = Item.objects.filter(
                Q(complete=False) & (Q(assigned_to__slug=self.kwargs['slug']) | Q(
                    author__slug=self.kwargs['slug']))).distinct()

            context['tasks_overdue'] = Item.objects.filter(
                Q(deadline_date__lte=now) & Q(complete=False) & (Q(assigned_to__slug=self.kwargs['slug']) | Q(
                    author__slug=self.kwargs['slug']))).distinct()
        else:
            context['category_list'] = Category.objects.filter(category_author=self.request.user)
            context['tasks'] = Item.objects.filter(Q(assigned_to=self.request.user) |
                                                   Q(author=self.request.user))
            context['tasks_complete'] = Item.objects.filter(Q(complete=True) & Q(assigned_to__slug=self.kwargs[
                'slug']))
            context['tasks_ongoing'] = Item.objects.filter(Q(complete=False) & Q(assigned_to__slug=self.kwargs[
                'slug']))
            context['tasks_overdue'] = Item.objects.filter(
                Q(deadline_date__lte=now) & Q(complete=False) & Q(assigned_to__slug=self.kwargs['slug']))
        return context


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'users/user_create.html'
    success_url = '/manage_users/'

    # Auto assign user to the company of logged in user
    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.account_type == 'Admin':
            return True
        else:
            return False

    def handle_no_permission(self):
        return redirect('main')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    context_object_name = 'user'
    success_url = '/manage_users/'

    def test_func(self):
        # user must be Admin and cannot delete themself via direct link
        if self.request.user.account_type == 'Admin' and not self.request.user.slug == self.kwargs['slug'] and \
                not self.request.user.username == 'demo_user':
            return True
        else:
            return False

    def handle_no_permission(self):
        return redirect('manage_users')
