import datetime
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render,redirect
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.contrib import auth
from django.urls import reverse
from read_statistics.utils import get_days_read_data,get_today_hot_data,get_yesterday_hot_data
from .forms import LoginForm

def get_seven_days_hot_blogs():
    today=timezone.now().date()
    date=today-datetime.timedelta(days=7)
    blogs=Blog.objects.filter(read_details__date__lt=today,read_details__date__gte=date).values('id','title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs[:7]
def home(request):
    blog_content_type=ContentType.objects.get_for_model(Blog)
    read_nums=get_days_read_data(blog_content_type)
    today_hot_data=get_today_hot_data(blog_content_type)
    yesterday_hot_data=get_yesterday_hot_data(blog_content_type)
    #缓存
    seven_days_hot_data=cache.get('seven_days_hot_data')
    if seven_days_hot_data is None:
        seven_days_hot_data=get_seven_days_hot_blogs()
        cache.set('seven_days_hot_data',seven_days_hot_data,5) 
    context={}
    context['read_nums']=read_nums
    context['today_hot_data']=today_hot_data
    context['yesterday_hot_data']=yesterday_hot_data    
    context['seven_days_hot_data']=seven_days_hot_data
    # context['dates']=dates
    return render(request,'home.html',context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user=login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))         
    else: 
        login_form = LoginForm()
    
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)
            
           
