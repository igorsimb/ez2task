from django import forms
from django.contrib.auth.forms import UserCreationForm

from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field

from users.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(

            FloatingField('email', autofocus='autofocus', autocomplete=False),
            FloatingField('username'),
            FloatingField('password1'),
            FloatingField('password2'),
            HTML('<button type="submit" class="btn btn-primary">Register</button>'),
        )


# to be used as the ImageField widget below; prevents the useless "Currently" image field from showing
class ClearableFileInputCustom(forms.ClearableFileInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['is_initial'] = False
        return context


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ('image', 'username', 'email', 'first_name', 'last_name', 'account_type')
        fields = ('username', 'email', 'first_name', 'last_name', 'account_type')

        widgets = {'image': ClearableFileInputCustom()}

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.company is not None:
            # only admins can change account type, this is a redundant failsafe to make sure Agents don't promote
            # themselves to Admin
            if not user.account_type == 'Admin':
                self.fields['account_type'].disabled = True

        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(

            # Field('image'),
            FloatingField('username'),
            FloatingField('email'),
            FloatingField('first_name'),
            FloatingField('last_name'))



class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'account_type', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(

            FloatingField('email', autofocus='autofocus', autocomplete=False),
            FloatingField('username'),
            FloatingField('first_name'),
            FloatingField('last_name'),
            FloatingField('account_type'),
            FloatingField('password1'),
            FloatingField('password2'),
            HTML('<button class="btn btn-success" id="user_create_button"'
                 '{% if request.user.username == "demo_user" %} disabled {% endif %}'
                 ' type="submit">Add</button>'
                 '<a href="{% url "manage_users" %}"class="btn btn-danger ms-2">Cancel</a>'),
        )
