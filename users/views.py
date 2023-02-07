from .models import CustomUser
from django.views import generic
from django.urls import reverse_lazy
from .forms import CustomUserEditForm, AutoGenPassCustomUserCreationForm, generate_password
#
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


class IndexView(generic.ListView):
    model = CustomUser
    context_object_name = 'user_list'
    template_name = 'users/index.html'
    # By defult I used order_by added date, we can change it to show in differente order.
    # I filtered de activated users, this way super users (or in a future team admins),
    #   can hide a member for any reason.
    queryset = CustomUser.objects.filter(is_active=True, is_staff=False).order_by('-date_joined').values('id', 'first_name', 'last_name', 'team_role', 'email', 'phone_number')
    paginate_by = 9


class AddMemberView(generic.CreateView):
    form_class = AutoGenPassCustomUserCreationForm
    success_url = reverse_lazy("users:index")
    template_name = "users/form.html"


class EditMemberView(generic.UpdateView):
    model = CustomUser
    form_class = CustomUserEditForm
    success_url = reverse_lazy("users:index")
    template_name = "users/form.html"

   # Sending user object to the form, to verify which fields to display/remove (depending on group)
    def get_form_kwargs(self):
        kwargs = super(EditMemberView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class DeleteMemberView(generic.DeleteView):
    model = CustomUser
    success_url = reverse_lazy("users:index")
    template_name = "users/delete.html"


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


def reset_password(request, pk):
    tempUser = CustomUser.objects.filter(id=pk).first()
    password = generate_password()
    tempUser.set_password(password)
    tempUser.save()
    # WARNING: The main idea is send 'password' to email of the user
    print(tempUser.email + " new password is : " + password)
    return redirect('/')


def error404(request, exception):
    return render(request,'404.html', status=404)