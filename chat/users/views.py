from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password

from .models import User
from .forms import SignUpForm, SignInForm



# Create your views here.
def Logout(request):
    logout(request)
    messages.add_message(
        request,
        messages.SUCCESS,
        message='You successfully logged out'
        )
    return HttpResponseRedirect(reverse_lazy('index'))


class SignIn(FormView):
    model = User
    form_class = SignInForm
    success_url = reverse_lazy('index')
    template_name = 'sign_in.html'
    
    def form_valid(self, form):
        user = User.objects.filter(
            Q(username=form.data['username_email']) |
            Q(email=form.data['username_email'])
            ).first()
        
        if user:
            if check_password(form.data['password'], user.password):
                login(self.request, user=user)
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    'You successfully logged in'
                )
                return super().form_valid(form)
        messages.add_message(
            self.request, 
            messages.ERROR,
            message='Incorrect username/email or password'
            )
        self.success_url = reverse_lazy('sign_in')
        
        return super().form_valid(form)


class SignUp(FormView):
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('sign_in')
    template_name = 'sign_up.html'
    
    def form_valid(self, form):
        user = User.objects.filter(Q(username=form.data['username']) |
                                   Q(email=form.data['email']))
        if user:
            messages.add_message(
                self.request,
                messages.ERROR,
                message='Profile with such username or email alredy created'
                )
            self.success_url = reverse_lazy('sign_up')
            return super().form_valid(form)
        elif form.data['password1'] != form.data['password2']:
            messages.add_message(
                self.request,
                messages.ERROR,
                message='Password must be the same'
                )
            self.success_url = reverse_lazy('sign_up')
            return super().form_valid(form)
        User.objects.create(
            username=form.data['username'],
            password=make_password(form.data['password1']),
            email=form.data['email']
            )
        
        return super().form_valid(form)