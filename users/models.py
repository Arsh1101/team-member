from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # I assumed first_name, last_name, email , phone_number, and team_roll should not be blank.
    # If you want to be optional fields, I can change them.
    email = models.EmailField("Email address", unique=True)
    first_name = models.CharField("First name", max_length=150)
    last_name = models.CharField("Last name", max_length=150)
    # Phone numbers could be unique too, but for now, is not.
    phone_number = PhoneNumberField("Phone number", null=False, blank=False)
    # I decided to use choices for team roles.
    # The other option was the Boolean field.
    # I think 'choices' is a better approach.
    # In the future, if we want to add different roles, it is easier to extend the functionality.
    # Seperation with use of variables for error prevention and logic separation.
    # For more complex roles in future we can have a differente table or use django roles.
    ADMIN = "Admin"
    REGULAR = "Regular"
    TEAM_ROLLS = [ 
        (ADMIN, "Can delete members"),
        (REGULAR, "Can't delete members"),
        ]
    team_roll = models.CharField("Team Roll",
        # Automatically set the max value of the keys, to max_length.
        max_length=max([len(i[0]) for i in TEAM_ROLLS]),
        choices=TEAM_ROLLS,
        default=REGULAR,
    )
    #Super user properties.
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    #For future data managment is good to have this field. 
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    # I will check the REQUIRED_FIELDS on form, to solve the add create super error.
    REQUIRED_FIELDS = [ ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email