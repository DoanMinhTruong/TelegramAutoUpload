from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from .forms import AddChannelForm , UpdateChannelForm
from tbot.models import Tbot
from .models import Channel
from backend.utils import *
from post.forms import   PostForm
from backend.background import BackgroundSingleton
import telebot
# Create your views here.
def index(request):
    channel = Channel.objects.all()
    return render(request , "channel/index.html" , {"channel" : channel})

def add(request):
    if request.method == 'POST':
        form = AddChannelForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            tbot = form.cleaned_data['tbot']
            # tbot = Tbot.objects.get(id = tbot_id)
            tbot_link = tbot.link
            tbot_token = tbot.token
            if(check_bot_in_channel(tbot_token,link , tbot_link)):
                print(form.cleaned_data['tbot'] , type(form.cleaned_data['tbot']) )
                form.save()
            else:
                messages.warning(request, "Bot chưa được thêm vào Channel, hoặc không có quyền send_message")
                referer = request.META.get('HTTP_REFERER')
                if referer:
                    return redirect(referer)
            return redirect('channel_index')  # Điều hướng tới danh sách các bot
            # form.save()
    else:
        form = AddChannelForm()
    return render(request, 'channel/add.html', {'add_channel_form': form})

def update(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)

    if request.method == 'POST':
        form = UpdateChannelForm(request.POST, instance=channel)
        if form.is_valid():
            link = form.cleaned_data['link']
            tbot = form.cleaned_data['tbot']
            # tbot = Tbot.objects.get(id = tbot_id)
            tbot_link = tbot.link
            tbot_token = tbot.token
            if(check_bot_in_channel(tbot_token,link , tbot_link)):
                # print(form.cleaned_data['tbot'] , type(form.cleaned_data['tbot']) )
                form.save()
                messages.success(request,"Cập nhật Channel thành công")
            else:
                messages.error(request,"Cập nhật Channel thất bại")
        else:
            messages.error(request,"Cập nhật Channel thất bại")
        return redirect('channel_update', channel_id=channel_id)
        
    else:
        form = UpdateChannelForm(instance=channel)
    
    return render(request, 'channel/update.html', {'update_channel_form': form})

def delete(request, channel_id):
    if request.method == 'POST':
        try:
            tbot = get_object_or_404(Channel, id=channel_id)
            tbot.delete()
        except:
            messages.warning(request, "Có lỗi khi xóa Channel")
    return redirect('channel_index')  


def detail(request, channel_id):
    try:
        channel = get_object_or_404(Channel, id=channel_id)
        post = Post.objects.filter(channel_id = channel_id )
        
        return render(request , "channel/detail.html" , {"channel" : channel , "post" : post})
    except Exception as ex:
        messages.warning(request, "Có lỗi khi lấy thông tin: " + str(ex))
        return redirect(request.META.get('HTTP_REFERER'))
    


from post.models import Post, Image

def add_post(request, channel_id ):
    channel = get_object_or_404(Channel, id=channel_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        images = request.FILES.getlist('image')
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.channel = channel
            post.save()
            for i in images:
                i = Image(post=post, image=i).save()
                # Image.objects.create(post = post , image= i)
            

            messages.success(request, "Tạo Post thành công")
            return redirect('channel_detail' ,channel_id = channel.id)  # Thay thế 'your_redirect_url' bằng đường dẫn chuyển hướng của bạn
    else:
        post_form = PostForm()

    return render(request, 'channel/add_post.html', {'post_form': post_form})


def update_post(request, channel_id, post_id):
    channel = get_object_or_404(Channel, id=channel_id)
    post = get_object_or_404(Post, id=post_id, channel=channel)
    images = Image.objects.filter(post = post)
    
    if request.method == 'POST':
        if(post.is_running):
            messages.warning(request , "Post đang chạy")
            return redirect(request.META.get('HTTP_REFERER'))
        post_form = PostForm(request.POST, instance=post)
        images = request.FILES.getlist('image')
        if post_form.is_valid():
            updated_post = post_form.save(commit=False)
            updated_post.channel = channel
            updated_post.save()

            # Xóa ảnh cũ của bài viết
            Image.objects.filter(post = post).delete()

            # Tạo ảnh mới cho bài viết
            for image in images:
                Image.objects.create(post=updated_post, image=image)

            messages.success(request, "Cập nhật Post thành công")
            return redirect('channel_detail', channel_id=channel.id)
    else:
        
        post_form = PostForm(instance=post)

    return render(request, 'channel/post_detail.html', {'post_form': post_form, 'post': post , 'images' : images})

def post_delete(request, post_id):
    background = BackgroundSingleton()
    if request.method == 'POST':
        try:
            post = get_object_or_404(Post, id=post_id)
            try:
                background.remove_job(post.tid)
            except:
                pass
            post.delete()
        except:
            messages.warning(request, "Có lỗi khi xóa Post")
    return redirect(request.META.get('HTTP_REFERER'))


def index_post(request , post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        images = Image.objects.filter(post_id = post.id)
        return render(request , "channel/post_detail.html" , {"post" : post , "images" : images})
    except Exception as ex:
        messages.warning(request, "Có lỗi khi lấy thông tin: " + str(ex))
        return redirect(request.META.get('HTTP_REFERER'))
    

def post_run(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    images = Image.objects.filter(post = post)
    img = []
    for i in images:
        img.append("./media/" + str(i.image))
    print(img)
    content = post.content
    channel = post.channel
    bot = channel.tbot

    token = bot.token
    link_channel = channel.link
    channel_id = get_channel_id(token , link_channel)

    def task():
        if(len(img)):
            bot_sendto_channel(token , channel_id , img, content)
        else:
            bot_sendto_channel_no_images(token , link_channel , content)
    
    background = BackgroundSingleton()

    job= background.add_job(task , 'interval' , seconds = int(post.scheduled_time))
    post.tid = job.id
    post.is_running = True
    post.save()

    return redirect(request.META.get('HTTP_REFERER'))


import time
def post_stop(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    
    background = BackgroundSingleton()
    while(True):
        time.sleep(10)
        try:
            job= background.pause_job(post.tid)
            break
        except:
            continue
    post.is_running = False
    post.tid = ""
    post.save()

    return redirect(request.META.get('HTTP_REFERER'))
