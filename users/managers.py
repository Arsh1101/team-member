from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager.
    Email is the unique identifier.
    """
    def create_user(self, email, password, first_name, last_name , phone_number, team_role, **extra_fields):
        """
        Create and save a user with the given infromation.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        # Used this value for super user or any other empty team_role:
        if team_role:
            user = self.model(email=email, first_name=first_name, last_name=last_name , phone_number=phone_number, team_role= team_role, **extra_fields)
        else:
            user = self.model(email=email, first_name=first_name, last_name=last_name , phone_number=phone_number, **extra_fields)
        # Temprorary value, brfore create a send a random password service.
        password = "temp"
        user.set_password(password)
        
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given infromation.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        #Validations
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        #Internal users (super users) can fill these parameters later.
        #Super users are not team admins in the definition of the team.
        #I used None, to add defult value for admins.
        first_name, last_name , phone_number, team_role = "", "", "", None
        return self.create_user(email, password, first_name, last_name , phone_number, team_role, **extra_fields)
