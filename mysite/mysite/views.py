from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from read_statistics.utils import get_days_read_data 
def home(request):
    blog_content_type=ContentType.objects.get_for_model(Blog)
    read_nums=get_days_read_data(blog_content_type)
    context={}
    context['read_nums']=read_nums
    # context['dates']=dates
    return render_to_response('home.html',context)