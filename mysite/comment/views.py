from django.shortcuts import render
from .models import Comment

def update_comment(request):
    user=request.user
    text=request.POST.get('text','')
    content_type=request.POST.get('content_type','')
    object_id=int(request.POST.get('object_id'))