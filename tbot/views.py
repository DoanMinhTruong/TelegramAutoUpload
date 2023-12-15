from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .forms import AddTbotForm
from .models import Tbot
from backend.utils import is_from_one_bot , is_valid_bot
# Create your views here.
def index(request):
    tbot = Tbot.objects.all()
    return render(request , "tbot/index.html" , {'tbot' : tbot})

def check_token_bot_existence(token):
    try:
        bot = get_object_or_404(Tbot, token=token)
        return True
    except:
        return False
def check_link_bot_existence(link):
    try:
        bot = get_object_or_404(Tbot, link=link)
        return True
    except:
        return False

def add(request):
    if request.method == 'POST':
        form = AddTbotForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            token = form.cleaned_data['token']
            if(is_valid_bot(token) 
               and is_from_one_bot(link, token) 
               and (not check_token_bot_existence(token)) 
               and (not check_link_bot_existence(link))):
                form.save()
            else:
                messages.warning(request, "Bot không hợp lệ, có thể do: Token hoặc Link lỗi, hoặc đã tồn tại trong hệ thống")
                referer = request.META.get('HTTP_REFERER')
                if referer:
                    return redirect(referer)
            return redirect('tbot_index')  # Điều hướng tới danh sách các bot
    else:
        form = AddTbotForm()
    return render(request, 'tbot/add.html', {'add_tbot_form': form})

def delete(request, tbot_id):
    if request.method == 'POST':
        try:
            tbot = get_object_or_404(Tbot, id=tbot_id)
            tbot.delete()
        except:
            messages.warning(request, "Có lỗi khi xóa Bot")
    return redirect('tbot_index')  
