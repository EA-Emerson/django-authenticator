from multiprocessing import context
from django.shortcuts import redirect, render
from .models import Post
from django.views import generic
from .forms import CommentForm

# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = 'index.html'
    
    
class DetailView(generic.DetailView):
    model=Post
    template_name = 'post_detail.html'
    
def index(request):
    posts=Post.objects.all()
    
    return render(request, "index.html", {"posts": posts})

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    
    if request.method == "POST":
        form=CommentForm(request.POST)
        
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post = post
            comment.save()
            
            return redirect('post_detail', slug=post.slug)
        
    else:
        form=CommentForm()
    
    return render(request, "post_detail.html", {'post':post, 'form':form})