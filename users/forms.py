from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
import secrets
import string
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

# I have to copy the code here, later!
def generate_password():
    pass


def send_email_password(first_name, user_email, password):
    with get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT,  
                        username=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD, 
                        use_tls=settings.EMAIL_USE_TLS) as connection:
         subject = "Team member password"
         email_from = settings.EMAIL_HOST_USER
         recipient_list = [user_email, ]
         message = first_name + ". This '" + password + "' is your password.\nPlease change your password as soon as possible." 
         EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "phone_number", "team_role")
    

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        TEAM_ROLLS = [[item[0], item[0] + " - " + item[1]] for item in CustomUser.TEAM_ROLLS[::-1]]
        widget_team_roll = forms.RadioSelect(attrs={ 'class': 'form-check' })
        self.fields['team_role'] = forms.TypedChoiceField(label="Roles", widget=widget_team_roll, choices=TEAM_ROLLS, initial=TEAM_ROLLS[0], required=True)
        
        for visible in self.visible_fields():
            if visible.auto_id != "id_team_role":
                visible.field.widget.attrs['class'] = 'form-control'
                visible.field.widget.attrs['placeholder'] = visible.field.label


class AutoGenPassCustomUserCreationForm(CustomUserCreationForm):

    def __init__(self, *args, **kwargs):
        super(AutoGenPassCustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'
        # To stop them to show up in template
        self.fields['password1'].widget = self.fields['password1'].hidden_widget()
        self.fields['password2'].widget = self.fields['password2'].hidden_widget()
        # del self.fields['password1']
        # del self.fields['password2']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        instance.set_password(password)
        if commit:
            instance.save()
            # Arsh warrning:
            # send_email_password(instance.first_name, instance.email, password)
            # Google do not allow me set my 'allow less secure ...'
            # It was extra work to do, so I decided to done the job first then retrun back to it.
            print("USER PASSWORD -> " + password)
        return instance


class CustomUserEditForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "phone_number", "team_role")


    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)

        TEAM_ROLLS = [[item[0], item[0] + " - " + item[1]] for item in CustomUser.TEAM_ROLLS[::-1]]
        widget_team_roll = forms.RadioSelect(attrs={ 'class': 'form-check' })
        self.fields['team_role'] = forms.TypedChoiceField(label="Roles", widget=widget_team_roll, choices=TEAM_ROLLS, initial=TEAM_ROLLS[0], required=True)
        
        for visible in self.visible_fields():
            if visible.auto_id != "id_team_role":
                visible.field.widget.attrs['class'] = 'form-control'
                visible.field.widget.attrs['placeholder'] = visible.field.label
