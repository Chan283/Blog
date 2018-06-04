from django import forms
from blog.models import Comment,Post

class PostForm(forms.ModelForm):
	class Meta():
		model=Post	#we are telling that we want data from user to be filled into model 'Post'
		fields=('author','title','text')	#all these 3 will be displayed in the form as per described in model
		
		#Now title should be large length textbox, while text should be a large rectangular size box, this can be told through widgets
		
		widgets = {
			'title':forms.TextInput(attrs={'class':'textinputclass'}),	#textinputclass is our own defined css class
			'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}) 
			#this class is css class where editable means we should be able to edit this field, 
			#2nd class tells that it should have extra properties like editng text within textarea and postcontent is our own defined css class
		}
		
		
class CommentForm(forms.ModelForm):
	class Meta():
		model=Comment
		fields=('author','text')
		
		widgets = {
			'author':forms.TextInput(attrs={'class':'textinputclass'}),
			'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
		}