from django.shortcuts import get_object_or_404,render,render
from .models import Blog,BlogType
from django.conf import settings
from django.db.models import Count
from django.core.paginator import Paginator
from read_statistics.utils import read_statistics_once_read

def get_blog_list_common_data(request,blogs_all_list):
    paginator=Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS)
    page_num=request.GET.get('page',1)
    page_of_blogs=paginator.get_page(page_num)
    current_page_num=page_of_blogs.number
    page_range=list(range(max(current_page_num-2,1),current_page_num))+\
               list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))
    if page_range[0]-1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages-page_range[-1]>=2:
        page_range.append('...')               
    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1]!=paginator.num_pages:
        page_range.append(paginator.num_pages)
    blog_dates=Blog.objects.dates('creat_time','month',order='DESC')
    blog_dates_dict={}
    for blog_date in blog_dates:
          blog_count=Blog.objects.filter(creat_time__year=blog_date.year,creat_time__month=blog_date.month).count()
          blog_dates_dict[blog_date]=blog_count
    context={}
    context['blogs']=page_of_blogs.object_list
    context['page_of_blogs']=page_of_blogs
    context['blog_types']=BlogType.objects.annotate(blog_count=Count('blog'))
    context['page_range']=page_range
    context['blog_dates']=blog_dates_dict
    return context

def blog_list(request):
    blogs_all_list=Blog.objects.all()
    context=get_blog_list_common_data(request,blogs_all_list)
    return render(request,'blog/blog_list.html',context)

def blog_detail(request,blog_pk):
    blog=get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key=read_statistics_once_read(request,blog)   
    context={}
    context['previous_blog']=Blog.objects.filter(creat_time__gt=blog.creat_time).last()
    context['next_blog']=Blog.objects.filter(creat_time__lt=blog.creat_time).first()
    context['blog']=blog
    response=render(request,'blog/blog_detail.html',context)   
    response.set_cookie(read_cookie_key,'true')
    return response 
    
def blogs_with_type(request,blog_type_pk):
    blog_type=get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list=Blog.objects.filter(blog_type=blog_type)
    context=get_blog_list_common_data(request,blogs_all_list)
    context['blog_type']=blog_type
    return render(request,'blog/blogs_with_type.html',context)
    
def blogs_with_date (request,year,month):
    blogs_all_list=Blog.objects.filter(creat_time__year=year,creat_time__month=month)
    context=get_blog_list_common_data(request,blogs_all_list)
    context['blogs_with_date']='%s年%s月'%(year,month)
    return render(request,'blog/blogs_with_date.html',context) 
