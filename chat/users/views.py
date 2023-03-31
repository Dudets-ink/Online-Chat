from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .models import User
from .forms import SignUpForm, SignInForm
from utils import mails, tokens



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
    template_name = 'users/sign_in.html'
    
    def form_valid(self, form):
        user = User.objects.filter(
            Q(username=form.data['username_email']) |
            Q(email=form.data['username_email'])
            ).first()
        
        if user:
            if check_password(form.data['password'], user.password) and user.is_active:
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
    success_url = reverse_lazy('index')
    template_name = 'users/sign_up.html'
    
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
        
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        template = render_to_string('users/activ_acc_email.html', {
            'domain': get_current_site(self.request),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)), 
            'token': tokens.generate_acc_token.make_token(user)
        })
        
        mails.send_email(self.request, user.email,
                   user.username, user.password, template)
        
        return super().form_valid(form)
    
    
def activation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist, OverflowError):
        user = None
        
    if user is not None and tokens.generate_acc_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.add_message(request, messages.INFO, 'You activated your account.')
        return HttpResponseRedirect(reverse_lazy('sign_in'))
    else:
        messages.add_message(request, messages.ERROR, 'Your activation link is invalid.')
        return HttpResponseRedirect(reverse_lazy('index'))
    