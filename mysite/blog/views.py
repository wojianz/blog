from django.shortcuts import render_to_response,get_object_or_404,render
from .models import Blog,BlogType
from django.conf import settings
from django.core.paginator import Paginator
def blog_list(request):
    blogs_all_list=Blog.objects.all()
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
    context={}
    context['blogs']=page_of_blogs.object_list
    context['page_of_blogs']=page_of_blogs
    context['blog_types']=BlogType.objects.all()
    context['page_range']=page_range
    context['blog_dates']=Blog.objects.dates('creat_time','month',order='DESC')
    return render_to_response('blog/blog_list.html',context)
def blog_detail(request,blog_pk):
    context={}
    blog=get_object_or_404(Blog,pk=blog_pk)
    context['previous_blog']=Blog.objects.filter(creat_time__gt=blog.creat_time).last()
    context['next_blog']=Blog.objects.filter(creat_time__lt=blog.creat_time).first()
    context['blog']=blog
    return render_to_response('blog/blog_detail.html',context)    
def blogs_with_type(request,blog_type_pk):
    context={}
    blog_type=get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list=Blog.objects.filter(blog_type=blog_type)
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
    context['blog_type']=blog_type
    context['blogs']=page_of_blogs.object_list
    context['page_of_blogs']=page_of_blogs
    context['page_range']=page_range
    context['blog_types']=BlogType.objects.all()
    return render_to_response('blog/blogs_with_type.html',context)    
def blogs_with_date (request,year,month):
    pass