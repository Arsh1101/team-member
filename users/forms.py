from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
import secrets
import string


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
        return instance


class CustomUserEditForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "phone_number", "team_role")


    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)

        #password

        TEAM_ROLLS = [[item[0], item[0] + " - " + item[1]] for item in CustomUser.TEAM_ROLLS[::-1]]
        widget_team_roll = forms.RadioSelect(attrs={ 'class': 'form-check' })
        self.fields['team_role'] = forms.TypedChoiceField(label="Roles", widget=widget_team_roll, choices=TEAM_ROLLS, initial=TEAM_ROLLS[0], required=True)
        
        for visible in self.visible_fields():
            if visible.auto_id != "id_team_role":
                visible.field.widget.attrs['class'] = 'form-control'
                visible.field.widget.attrs['placeholder'] = visible.field.label
