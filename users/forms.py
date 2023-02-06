from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser


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
