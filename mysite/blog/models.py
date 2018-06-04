from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
	author=models.ForeignKey('auth.User',on_delete=models.CASCADE)	#new superuser created through this
	title=models.CharField(max_length=125)
	text=models.TextField()
	created_date=models.DateTimeField(default=timezone.now())	#created date is now
	published_date=models.DateTimeField(blank=True,null=True)	#this date will be added through below func which will be triggered through btn
	  
	#publish() will set the published date for a particular post when the publish btn is clicked
	def publish(self):
		self.published_date=timezone.now()
		self.save()
		
	#A post can have multiple comments some will be approved and sm nt, we will filter only apporved ones and show them	under the post
	def approve_comments(self):
		return self.comments.filter(approved_comment=True)
	
	#where to go when the post is created,so it will go to post_detail page having primary key of the post we just created
	def get_absolute_url(self):	
		return reverse("post_detail",kwargs={'pk':self.pk})  
	
	def __str__(self):
		return self.title
		
class Comment(models.Model):
	#each comment will be connected to blog post app,related_name will create backward relation from blog.Post to Comment model
	post=models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
	#here author is just a simple charfield while in Post it was authenticated user,this means that post can be written only by superuser
	#but comments can be written by anyone
	author=models.CharField(max_length=125)
	text=models.TextField()
	created_date=models.DateTimeField(default=timezone.now())
	#by default a comment will be unapproved, it will be approved when approve btn clicked and approve gets triggered(approve func below)
	approved_comment=models.BooleanField(default=False)	
	
	def approve(self):
		self.approved_comment=True
		self.save()
	
	#after a comment is added, approval will be done bu superuser, for now comment tyoer will be redirected to page of all posts
	def get_absolute_url(self):
		return reverse('post_list')
	
	def __str__(self):
		return self.text