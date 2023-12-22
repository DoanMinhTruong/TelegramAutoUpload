from django.shortcuts import render, redirect
from .models import Forward
# Create your views here.
from .forms import ForwardForm


def index(request):
    forward = Forward.objects.all()
    return render(request , "forward/index.html" , {"forward" : forward})

def add(request):
    if request.method == 'POST':
        form = ForwardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forward_index') 
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ForwardForm()
    return render(request, 'forward/add.html', {'add_forward_form': form})