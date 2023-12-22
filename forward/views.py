from django.shortcuts import render, redirect, get_object_or_404
from .models import Forward, FImage
# Create your views here.
from .forms import ForwardForm
from backend.utils import *
from backend.background import BackgroundSingleton
from django.contrib import messages


def index(request):
    forward = Forward.objects.all()
    return render(request , "forward/index.html" , {"forward" : forward})

def add(request):
    if request.method == 'POST':
        form = ForwardForm(request.POST)
        images = request.FILES.getlist('image')
        if form.is_valid():
            forward = form.save()
            for i in images:
                i = FImage(forward=forward, image=i).save()
            return redirect('forward_index') 
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ForwardForm()
    return render(request, 'forward/add.html', {'add_forward_form': form})


def run(request, forward_id):
    forward = get_object_or_404(Forward, id=forward_id)
    images = FImage.objects.filter(forward = forward)
    img = []
    for i in images:
        img.append("./media/" + str(i.image))
    print(img)
    content = forward.content
    channels = forward.channels.all()
    bots = [channel.tbot for channel in channels]

    tokens = [bot.token for bot in bots]
    link_channels = [channel.link for channel in channels]
    channels_id = [get_channel_id(tokens[i] , link_channels[i]) for i in range(len(channels))]

    def task():
        if(len(img)):
            for i in range(len(channels)):
                bot_sendto_channel(tokens[i] , channels_id[i] , img, content)
        else:
            for i in range(len(channels)):
                bot_sendto_channel_no_images(tokens[i] , link_channels[i] , content)
    
    background = BackgroundSingleton()

    job= background.add_job(task , 'interval' , seconds = int(forward.scheduled_time))
    forward.tid = job.id
    forward.is_running = True
    forward.save()

    return redirect(request.META.get('HTTP_REFERER'))


import time
def stop(request, forward_id):
    forward = get_object_or_404(Forward, id=forward_id)
    
    
    background = BackgroundSingleton()
    
    job= background.pause_job(forward.tid)
        
    forward.is_running = False
    forward.tid = ""
    forward.save()

    return redirect(request.META.get('HTTP_REFERER'))


def update(request , forward_id):
    forward = get_object_or_404(Forward, id=forward_id)
    images = FImage.objects.filter(forward = forward)
    
    if request.method == 'POST':
        if(forward.is_running):
            messages.warning(request , "Post đang chạy")
            return redirect(request.META.get('HTTP_REFERER'))
        forward_form = ForwardForm(request.POST, instance=forward)
        images = request.FILES.getlist('image')
        if forward_form.is_valid():
            updated_forward = forward_form.save(commit=False)
            updated_forward.save()

            # Xóa ảnh cũ của bài viết
            FImage.objects.filter(forward = forward).delete()

            # Tạo ảnh mới cho bài viết
            for image in images:
                FImage.objects.create(forward=updated_forward, image=image)

            messages.success(request, "Cập nhật thành công")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        
        forward_form = ForwardForm(instance=forward)

    return render(request, 'forward/update.html', {'forward_form': forward_form, 'forward': forward , 'images' : images})

def delete(request, forward_id):
    background = BackgroundSingleton()
    if request.method == 'POST':
        try:
            forward = get_object_or_404(Forward, id=forward_id)
            try:
                background.remove_job(forward.tid)
            except:
                pass
            forward.delete()
        except:
            messages.warning(request, "Có lỗi khi xóa Forward")
    return redirect(request.META.get('HTTP_REFERER'))