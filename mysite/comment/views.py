from django.shortcuts import render,redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.urls import reverse
from .forms import CommentForm

def update_comment(request):
    referer=request.META.get('HTTP_REFERER',reverse('home'))
    comment_form=CommentForm(request.POST,user=request.user)
    if comment_form.is_valid():        
        comment=Comment()
        comment.user=comment_form.cleaned_data['user']
        comment.text=comment_form.cleaned_data['text']
        comment.content_object=comment_form.cleaned_data['content_object']
        comment.save() 
        return redirect(referer)
    else:
        return render(request,'error.html',{'message':comment_form.errors,'redirect_to':referer})
        
            
        
        

