from django.shortcuts import render,get_object_or_404
from blogapp.models import Post,Comment
from blogapp.forms import Comment_form,AddPost_form
from taggit.models import Tag
import sendgrid
from sendgrid.helpers.mail import *
import os
import smtplib
from django.core.mail import EmailMessage
s = smtplib.SMTP('smtp.gmail.com', 25)
s.ehlo()
s.starttls()
# Create your views here.
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.filter(status__iexact='Published')
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])
    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try: 
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blogapp/post_list.html',{'post_list':post_list})
def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published', publish__year=year,publish__month=month, publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=Comment_form(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=Comment_form()
            
    return render(request,'blogapp/post_detail.html',{'post':post,'csubmit':csubmit,'form':form,'comments':comments})
from . import forms
from django.core.mail import send_mail
def send_by_mail(request,id):
    post=get_object_or_404(Post,id=id,status="published")
    sent = False
    if request.method=='POST':
        form=forms.email_send(request.POST)
        if form.is_valid():
            sg = sendgrid.SendGridAPIClient(os.environ.get('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'))
            cd=form.cleaned_data
            subject='{} ({}) recomends you to read {} post'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message='read post at :\n {} \n{}\'s comments :\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject, message, 'patelrajkumar3600@gmail.com', [cd['to']])
            sent=True
    else:
        form=forms.email_send()
    return render(request,'blogapp/share_by_mail.html',{'form':form,'post':post,'sent':sent})
def AddPost_view(request):
    form=AddPost_form()
    if request.method=='POST':
        form=AddPost_form(request.POST)
        if form.is_valid():
            form.save()
            form=AddPost_form()
    return render(request, 'blogapp/AddPost.html',{'form':form})