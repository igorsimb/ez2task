import datetime

from django.contrib import messages

from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML

from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from users.models import User, Company
from .models import Item, Category, Comment
from .forms import ItemCreateForm, ItemUpdateForm, CommentForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'main_app/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        threshold = timezone.now() + timezone.timedelta(days=1)
        context['week_left'] = datetime.datetime.now() + datetime.timedelta(days=7)
        now = timezone.now()
        context['now'] = datetime.datetime.now()
        context['threshold'] = datetime.datetime.now() + datetime.timedelta(hours=24)

        # ADMIN
        if not self.request.user.company and self.request.user.account_type == 'Admin':
            context['tasks'] = Item.objects.filter(author__company__name__exact=self.request.user.company.name)
            context['tasks_completed'] = Item.objects.filter(Q(
                author__company__name__exact=self.request.user.company.name) & Q(
                complete=True))

            context['tasks_not_completed'] = Item.objects.filter(Q(
                author__company__name__exact=self.request.user.company.name) & Q(
                complete=False))

            context['not_overdue'] = Item.objects.filter(Q(
                author__company__name__contains=self.request.user.company.name) & Q(
                deadline_date__gt=threshold))  # task > 24

            context['unhealthy'] = Item.objects.filter(
                Q(author__company__name=self.request.user.company.name) &
                Q(deadline_date__lte=threshold) &
                # Q(deadline_time__lte=now) &
                Q(complete=False)
            )

            # annotate helps access number of items for each category (see main page template: category.items_count)
            context['categories'] = Category.objects.filter(Q
                                                            (category_author__company__name=self.request.user.company.name) & Q(
                item__complete=False)).annotate(items_count=Count('item'))

            context['company_categories'] = Category.objects.filter(Q(
                category_author__company__name=self.request.user.company.name) & Q(
                item__complete=False)).annotate(items_count=Count('item'))

            # per_month = queryset of dictionaries: month + number of tasks in each month
            context['per_month'] = Item.objects.filter(
                Q(author__company__name=self.request.user.company.name)). \
                annotate(month=TruncMonth('date_posted')).values('month'). \
                annotate(c=Count('id')).values('month', 'c').order_by('month')


        # AGENT (w/ company)
        elif self.request.user.company is not None and self.request.user.account_type == 'Agent':
            context['tasks'] = Item.objects.filter(Q(author=self.request.user) | Q(
                assigned_to=self.request.user)).distinct()

            context['tasks_completed'] = Item.objects.filter((Q(
                author=self.request.user) | Q(assigned_to=self.request.user)) & Q(complete=True)).distinct()

            context['tasks_not_completed'] = Item.objects.filter((Q(
                author=self.request.user) | Q(assigned_to=self.request.user)) & Q(complete=False)).distinct()

            context['not_overdue'] = Item.objects.filter(
                (Q(author=self.request.user) | Q(assigned_to=self.request.user))
                & Q(deadline_date__gt=threshold)).exclude(complete=True).distinct()

            context['unhealthy'] = Item.objects.filter(
                (Q(author=self.request.user) | Q(assigned_to=self.request.user)) & Q(
                    deadline_date__lte=now)).exclude(complete=True).distinct()

            # annotate helps access number of items for each category (see main page template)
            context['categories'] = Category.objects.filter(Q
                                                            (category_author__company__name=self.request.user.company.name) &
                                                            Q(item__complete=False) &
                                                            Q(item__assigned_to=self.request.user)
                                                            ).annotate(items_count=Count('item'))

            # same as above, reduces code in template
            context['company_categories'] = Category.objects.filter(
                Q(category_author__company__name=self.request.user.company.name) &
                Q(item__complete=False)).annotate(items_count=Count('item'))

            context['per_month'] = Item.objects.filter \
                (Q(author=self.request.user) | Q(assigned_to=self.request.user)).distinct(). \
                annotate(month=TruncMonth('date_posted')).values('month'). \
                annotate(c=Count('id')).values('month', 'c').order_by('month')

        # AGENT (w/o company)
        else:
            context['tasks'] = Item.objects.filter(Q(author=self.request.user) | Q(
                assigned_to=self.request.user)).distinct()

            context['tasks_completed'] = Item.objects.filter((Q(
                author=self.request.user) | Q(assigned_to=self.request.user)) & Q(complete=True)).distinct()

            context['tasks_not_completed'] = Item.objects.filter((Q(
                author=self.request.user) | Q(assigned_to=self.request.user)) & Q(complete=False)).distinct()

            context['not_overdue'] = Item.objects.filter(
                (Q(author=self.request.user) | Q(assigned_to=self.request.user))
                & Q(deadline_date__gt=threshold)).exclude(complete=True).distinct()

            context['unhealthy'] = Item.objects.filter(
                (Q(author=self.request.user) | Q(assigned_to=self.request.user)) & Q(
                    deadline_date__lte=now)).exclude(complete=True).distinct()

            # annotate helps access number of items for each category
            context['categories'] = Category.objects.filter(Q
                                                            (category_author=self.request.user) &
                                                            Q(item__complete=False)
                                                            ).annotate(items_count=Count('item'))

            # same as above, reduces code in template
            context['company_categories'] = Category.objects.filter(Q
                                                                    (category_author=self.request.user) &
                                                                    Q(item__complete=False)
                                                                    ).annotate(items_count=Count('item'))

            context['per_month'] = Item.objects.filter \
                (Q(author=self.request.user) | Q(assigned_to=self.request.user)).distinct(). \
                annotate(month=TruncMonth('date_posted')).values('month'). \
                annotate(c=Count('id')).values('month', 'c').order_by('month')

        return context


class ManageUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'main_app/manage_users.html'
    context_object_name = 'users'

    # Allow access only to Admins
    def test_func(self):
        if self.request.user.account_type == 'Admin':
            return True
        else:
            return False

    # overriding test_func's False state to redirect instead of showing 403
    # source: https://coderoad.ru/53952412/%D0%98%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-UserPassesTestMixin-class-based-view-AND-redirect-%D1%82%D0%B0%D0%BA%D0%B6%D0%B5
    def handle_no_permission(self):
        return redirect('main')


class ItemListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Item
    template_name = 'main_app/manage_tasks.html'
    context_object_name = 'items'

    # Allow access only to Admins
    def test_func(self):
        if self.request.user.account_type == 'Admin':
            return True
        else:
            return False

    # overriding test_func's False state to redirect instead of showing 403
    # source: https://coderoad.ru/53952412/%D0%98%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-UserPassesTestMixin-class-based-view-AND-redirect-%D1%82%D0%B0%D0%BA%D0%B6%D0%B5
    def handle_no_permission(self):
        return redirect('main')

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)

        context['timeout'] = datetime.datetime.now()
        context['timeout_date'] = timezone.now().date
        context['timeout_time'] = timezone.now().time

        if self.request.user.company is not None:
            context['category_list'] = Category.objects.filter(
                category_author__company=self.request.user.company)
            context['items'] = Item.objects.filter(author__in=self.request.user.company.users.all()).select_related(
                'category').prefetch_related('assigned_to').defer('description')
        else:
            context['category_list'] = Category.objects.filter(category_author=self.request.user)
            context['items'] = Item.objects.filter(author=self.request.user).select_related(
                'category').prefetch_related('assigned_to').defer('description')

        return context


class MyTasksView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'main_app/my_tasks.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super(MyTasksView, self).get_context_data(**kwargs)
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

        else:
            context['category_list'] = Category.objects.filter(category_author=self.request.user)

        return context

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        return Item.objects.filter(assigned_to=user).select_related(
            'category').prefetch_related('assigned_to').defer('description')


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemCreateForm
    template_name = 'main_app/create.html'
    context_object_name = 'items'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Gives access to 'user' from ItemCreateForm's __init__
    # source: https://coderoad.ru/37296102/%D0%97%D0%B0%D0%BF%D1%80%D0%BE%D1%81-%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0-%D0%B2__-init-_-_-in-ModelForm
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return '/'


class ItemDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Item
    template_name = 'main_app/detail.html'
    context_object_name = 'items'

    form = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            item = self.get_object()
            form.instance.user = request.user
            form.instance.item = item
            form.save()

            return redirect(reverse("detail", kwargs={'pk': item.pk}))

    # Allow access only to:
    #     a) users from this company
    #     b) admins from this company
    #     c) agens ONLY if they are author or assigned_to this task
    def test_func(self, *args, **kwargs):
        if self.request.user.company:
            if (self.request.user.company.name == self.get_object().author.company.name) and \
                    (self.request.user.account_type == 'Admin' or
                     self.request.user in self.get_object().assigned_to.all() or
                     self.request.user == self.get_object().author):
                return True
        elif not self.request.user.company:
            if (self.request.user == self.get_object().author):
                return True
        else:
            return False

    # Show 404 if test_func is false (text only shows in Debug = True)
    def handle_no_permission(self):
        raise Http404('Task not found or user has no permission to view this page')

    def get_context_data(self, **kwargs):
        task_comments_count = Comment.objects.all().filter(item=self.object.id).count()
        task_comments = Comment.objects.all().filter(item=self.object.id)
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'task_comments': task_comments,
            'task_comments_count': task_comments_count,
        })
        context['threshold'] = timezone.now() + timezone.timedelta(hours=24)
        context['timeout'] = datetime.datetime.now()
        context['timeout_date'] = timezone.now().date
        context['timeout_time'] = timezone.now().time
        return context


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemUpdateForm
    template_name = 'main_app/update.html'
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)

    # gives access to 'user' from ItemUpdateForm's __init__
    # source: https://coderoad.ru/37296102/%D0%97%D0%B0%D0%BF%D1%80%D0%BE%D1%81-%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0-%D0%B2__-init-_-_-in-ModelForm
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

        # Allow access only to:
        #     a) users from this company
        #     b) admins from this company
        #     c) agens/teamleads ONLY if they are author or assigned_to this task

    def test_func(self, *args, **kwargs):
        if self.request.user.company:
            if (self.request.user.company.name == self.get_object().author.company.name) and \
                    (self.request.user.account_type == 'Admin' or
                     self.request.user in self.get_object().assigned_to.all() or
                     self.request.user == self.get_object().author):
                return True
        elif not self.request.user.company:
            if (self.request.user == self.get_object().author):
                return True
        else:
            return False

    # Show 404 if test_func is false (only shows text in Debug = True)
    def handle_no_permission(self):
        raise Http404('Task not found or user has no permission to view this page')

    def get_context_data(self, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        context['next_url'] = self.request.GET.get('next')

        # Show only items of your company, if no company - your own:
        if self.request.user.company is not None:
            context['items'] = Item.objects.filter(author__in=self.request.user.company.users.all())
            context['assigned_to'] = User.objects.filter(company__name__contains=user.company.name)
        else:
            context['items'] = Item.objects.filter(author=self.request.user)
            context['assigned_to'] = User.objects.filter(id=user.id)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return '/'


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'main_app/delete.html'
    context_object_name = 'items'
    success_url = '/'

    # Allow deleting task only to admin, author and the assigned-to person.
    def test_func(self):
        item = self.get_object()
        if self.request.user == item.author or \
                self.request.user in item.assigned_to.all() or \
                self.request.user.is_admin:
            return True
        return False

    # Making sure we can use ?next={% url '<urlname>' %} in template
    def get_context_data(self, **kwargs):
        context = super(ItemDeleteView, self).get_context_data(**kwargs)
        context['next_url'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:  # if template contains "next"
            return next_url
        else:  # otherwise go to this url
            return '/'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['category_title', 'category_description']
    template_name = 'main_app/category_create.html'
    success_url = reverse_lazy('my_tasks')

    def form_valid(self, form):
        form.instance.category_author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:  # if template contains "next"
            return next_url
        return '/'  # otherwise go to this url

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context

    def __init__(self, *args, **kwargs):
        super(CategoryCreateView, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(

            FloatingField('category_title', autofocus='autofocus', autocomplete=False),
            FloatingField('category_description', style='min-height:15rem'),
            HTML('<input id="category_create_button"'
                 '{% if request.user.username == "demo_user" %} disabled{% endif %}'
                 ' class="btn btn-outline-success mt-2" type="submit" value="Add '
                 'Project">'
                 '<button type="button" class="btn btn-outline-danger mt-2 ms-2" onclick="history.back('
                 ')">Cancel</button>'),
        )


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'main_app/category_delete.html'
    context_object_name = 'category'
    success_url = '/'

    # Making sure we can use ?next={% url '<urlname>' %} in template
    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data(**kwargs)
        context['next_url'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:  # if template contains "next"
            return next_url
        return '/'  # otherwise go to this url

    # Admins from the same company; if no company, user that created the Category (aka Project)
    def test_func(self):
        if self.request.user.account_type == 'Admin' and \
                self.request.user.company.id == self.get_object().category_author.company.id:
            return True
        elif not self.request.user.company and self.request.user.id == self.get_object().category_author.id:
            return True
        else:
            return False


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    template_name = 'main_app/category_update.html'
    fields = ['category_title', 'category_description']
    success_url = '/'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:  # if template contains "next"
            return next_url
        return '/'  # otherwise go to this url

    # Admins from the same company; if no company, user that created the Category (aka Project)
    def test_func(self):
        if self.request.user.account_type == 'Admin' and \
                self.request.user.company.id == self.get_object().category_author.company.id:
            return True
        elif not self.request.user.company and self.request.user.id == self.get_object().category_author.id:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context

    def __init__(self, *args, **kwargs):
        super(CategoryUpdateView, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(

            FloatingField('category_title', autofocus='autofocus', autocomplete=False),
            FloatingField('category_description', style='min-height:15rem'),
            HTML('<input id="category_update_submit_button" class="btn btn-outline-success mt-2"'
                 '{% if request.user.username == "demo_user" %} disabled {% endif %} type="submit" '
                 'value="Update">'
                 '<button type="button" class="btn btn-outline-danger mt-2 mx-2" onclick="history.back('
                 ')">Cancel</button><br>'
                 '<a id="category_delete_submit_button" href="{% url "category_delete" category.id %}" '
                 'class="btn btn-danger mt-2{% if request.user.username == "demo_user" %} disabled{% endif %}">Delete Project</a>'),
        )


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = 'main_app/company-create.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.save()
        form.instance.users.add(self.request.user)  # Adds user to the new company
        user = self.request.user
        user.account_type = 'Admin'
        user.save()
        messages.add_message(
            message='Company has been successfully created! You now have access to Manage Users and Manage Tasks '
                    'pages.',
            request=self.request,
            level=messages.INFO
        )
        return super().form_valid(form)


class CompanyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Company
    template_name = 'main_app/company-update.html'
    fields = ['name', 'description']
    success_url = '/'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:  # if template contains "next"
            return next_url
        return '/'  # otherwise go to this url

    # Allow access only to Admins with a company
    def test_func(self):
        if self.request.user.company.id == self.kwargs['pk'] and self.request.user.account_type == 'Admin':
            return True
        else:
            return False

    # overriding test_func's False state to 404 instead of 403
    def handle_no_permission(self):
        raise Http404('Company not found or user not permitted')


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'main_app/comment_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.object.item.id})

    def test_func(self):
        if self.request.user.account_type == 'Admin' or not self.request.user.company:
            return True
        else:
            return False
