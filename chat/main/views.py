from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    return render(template_name='main/index.html', request=request)

class Chat(LoginRequiredMixin, TemplateView):
    template_name = 'main/chat.html'
    
class CharRoom(LoginRequiredMixin, TemplateView):
    template_name = 'main/chat_room.html'
    