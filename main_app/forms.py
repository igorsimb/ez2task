import datetime
from django.utils import timezone

from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field

from django import forms

from users.models import User
from .models import Item, Category, Comment


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'title', 'description', 'assigned_to', 'priority', 'deadline_date', 'deadline_time']
        date = timezone.now().date
        time = timezone.localtime(timezone.now()).strftime("%H:%M")

        widgets = {'deadline_date': DateInput(attrs={'value': date}),
                   'deadline_time': TimeInput(attrs={'value': time}),
                   }

    # Show only users from logged in user's company in assigned_to list (self.fields['assigned_to'].queryset)
    # source: https://simpleisbetterthancomplex.com/questions/2017/03/22/how-to-dynamically-filter-modelchoices-queryset-in-a-modelform.html
    def __init__(self, user, *args, **kwargs):
        super(ItemCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(

            FloatingField('category'),
            FloatingField('title', id='item_create_title_field'),
            Field('description'),
            Field('assigned_to'),
            FloatingField('priority', wrapper_class='w-25'),
            FloatingField('deadline_date', wrapper_class='w-25'),
            FloatingField('deadline_time', wrapper_class='w-25'),
            HTML('<button id="task_create_button" class="btn btn-success mb-2"'
                 '{% if request.user.username == "demo_user" %} disabled {% endif %}'
                 ' type="submit">Create</button>'
                 '<button type="button" class="btn btn-outline-danger mb-2 ms-2" onclick="history.back('
                 ')">Cancel</button>'),
        )


        if user.company is not None:
            if user.account_type == 'Admin':
                self.fields['assigned_to'].queryset = User.objects.filter(company__name=user.company.name)
            else:
                self.fields['assigned_to'].queryset = User.objects.filter(id=user.id)
                self.fields['assigned_to'].label_from_instance = lambda obj: "Me"
            self.fields['category'].queryset = Category.objects.filter(
                category_author__company__name__contains=user.company.name)
        else:
            self.fields['assigned_to'].queryset = User.objects.filter(id=user.id)
            self.fields['category'].queryset = Category.objects.filter(category_author=user)
            self.fields['assigned_to'].label_from_instance = lambda obj: "Me"

class ItemUpdateForm(forms.ModelForm):
    deadline = forms.DateTimeInput(attrs={'type': 'datetime-local'})
    class Meta:
        model = Item
        time = timezone.now()
        fields = ['category', 'title', 'description', 'assigned_to', 'priority', 'deadline_date', 'deadline_time', 'complete']

        widgets = {'deadline_date': DateInput(),
                   'deadline_time': TimeInput(),
                   }

    # Show only users from logged in user's company in assigned_to list
    # source: https://simpleisbetterthancomplex.com/questions/2017/03/22/how-to-dynamically-filter-modelchoices-queryset-in-a-modelform.html
    def __init__(self, user, *args, **kwargs):
        super(ItemUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(

            FloatingField('category', autofocus='autofocus'),
            FloatingField('title'),
            Field('description'),
            Field('assigned_to'),
            FloatingField('priority', wrapper_class='w-25'),
            FloatingField('deadline_date', wrapper_class='w-25'),
            FloatingField('deadline_time', wrapper_class='w-25'),
            'complete',
            HTML('<button id="task_update_submit_button" class="btn btn-success mb-2" '
                 '{% if request.user.username == "demo_user" %} disabled {% endif %}'
                 'type="submit">Update</button>'
                 '<button type="button" class="btn btn-outline-danger mb-2 ms-2" onclick="history.back('
                 ')">Cancel</button>'),
        )

        if user.company is not None:
            if user.account_type == 'Admin':
                self.fields['assigned_to'].queryset = User.objects.filter(company__name__contains=user.company.name)
            else:
                self.fields['assigned_to'].queryset = User.objects.filter(id=user.id)
                self.fields['assigned_to'].label_from_instance = lambda obj: "Me"
            self.fields['category'].queryset = Category.objects.filter(
                category_author__company__name__contains=user.company.name)
        else:
            self.fields['assigned_to'].queryset = User.objects.filter(id=user.id)
            self.fields['category'].queryset = Category.objects.filter(category_author=user)
            self.fields['assigned_to'].label_from_instance = lambda obj: "Me"


class AccountTypeUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['account_type']

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Add comment',
        'rows': '4',
    }))

    class Meta:
        model = Comment
        fields = ('content',)