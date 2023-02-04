from .models import CustomUser
from django.views import generic
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm


class IndexView(generic.ListView):
    model = CustomUser
    context_object_name = 'user_list'
    template_name = 'users/index.html'
    # By defult I used order_by added date, we can change it to show in differente order.
    # I filtered de activated users, this way super users (or in a future team admins),
    #   can hide a member for any reason.
    queryset = CustomUser.objects.filter(is_active=True, is_staff=False).order_by('-date_joined').values('first_name', 'last_name', 'team_role', 'email', 'phone_number')


class AddMemberView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("")
    template_name = "users/form.html"