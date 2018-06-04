from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from blog.models import Post,Comment
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext

# Create your views here.

#************** functions and views for Posts *********************#

class AboutView(TemplateView):
	template_name='about.html'

#This will 	give list of all posts in the model
class PostListView(ListView):
	model=Post
	
	'''
	below method is used to fire sql like query on model Post
	Post.objects.filter->from model "Post",get all "Objects", and filter those
	published_date__lte=timezone.now()->having published_date less than or equal to current time zone
	order_by('-published_date')->order by published date in descending order
	'''
	def get_queryset(self):
		return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
	model=Post
	
class CreatePostView(LoginRequiredMixin,CreateView):
	login_url='/login/'
	redirect_field_name='blog/post_detail.html'
		
	form_class=PostForm
		
	model=Post
	
class PostUpdateView(LoginRequiredMixin,UpdateView):
	login_url='/login/'	#after login user should go to login page
	redirect_field_name='blog/post_detail.html'	#redirect user to this page after login
	form_class=PostForm
	model=Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
	model=Post
	success_url=reverse_lazy('post_list')	#redirect the user to post_list page after successful deletion
	
#A view that displays all unpublished drafts	
class DraftListView(LoginRequiredMixin,ListView):
	login_url='/login/'
	redirect_field_name='blog/post_list.html'
	model=Post
	
	#this get_queryset method will get those posts which do not have a published_date meaning they are drafts
	def get_queryset(self):
		#filter those Objects from Post model having published dt as null
		return Post.objects.filter(published_date__isnull=True).order_by('created_date')
		
#************** functions and views for comments *********************#		

@login_required
def add_comment_to_post(request,pk):
	#get object or 404(file not found error)from Post model	with primary key =the primary key received as param for this func
	#inshort display that post which user has clicked on 
	post=get_object_or_404(Post,pk=pk)
	
	#if user filled the form and clicked "submit"
	if request.method=="POST":
		form=CommentForm(request.POST)
		
		if form.is_valid():	#if details filled by user r all correct
			comment=form.save(commit=False)	#saving the values given by user in the form
			
			#we are having a field 'post' in the comment model which is fk to Post model
			#hence we are setting that value as the post which user had clicked at the beginning
			comment.post=post
			comment.save()
			return redirect('post_detail',pk=post.pk)	#redirect to post_detail pg having pk as the one clicked by user initally to write cmnt
	
	else:
		form=CommentForm()
	return render(request,'blog/comment_form.html',{'form':form})

@login_required	
def comment_approve(request,pk):
	#here we are selecting the comment to approve so instead of posts, 
	#we have the comments list we will just click on the comment, which we want to be approved,hence param below is Comment(the model refered)
	#and primary key as the comment's pk on which we clicked
	comment=get_object_or_404(Comment,pk=pk)
	comment.approve()	#method under comments class in models
	return redirect('post_detail',pk=comment.post.pk)

@login_required	
def comment_remove(request,pk):
	comment=get_object_or_404(Comment,pk=pk)
	post_pk=comment.post.pk
	comment.delete()
	#for below line, we cant write pk=comment.post.pk bcoz in the earlier line comment is already deleted and no ref is there for comment
	#hence we are storing it in variable earlier i.e post_pk
	return redirect('post_detail',pk=post_pk)
	
@login_required
def post_publish(request,pk):
	post=get_object_or_404(Post,pk=pk)
	post.publish()
	return redirect('post_detail',pk=pk)