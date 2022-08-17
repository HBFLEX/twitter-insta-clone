from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import edit
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from .models import Post, Comment
from .forms import PostForm, CommentForm
from accounts.models import Profile


class FeedView(View):
    def get(self, request):
        feeds = Post.objects.filter(author__profile__followers__in=[request.user])
        people = User.objects.all().order_by('?')[:2]
        post_form = PostForm()
        context = {
            'feeds': feeds, 'people': people, 'form': post_form, 'page': 'feed',
        }
        return render(request, 'feeds/feeds.html', context)

    def post(self, request):
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            p_form = post_form.save(commit=False)
            p_form.author = request.user
            p_form.save()
            messages.success(request, 'Successfully Added a new post! Check your timeline in your profile page')
            return redirect(reverse('feeds:feed-detail-page', kwargs={'pk':p_form.id}))


class FeedDetailView(View, LoginRequiredMixin):
    def get(self, request, pk):
        comment_form = CommentForm()
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post)
        context = {
            'feed': post, 'comments': comments, 'comment_form': comment_form, 
            'page': 'feed_detail',
        }
        return render(request, 'feeds/feed_detail.html', context)

    def post(self, request, pk):
        comment_form = CommentForm(request.POST)
        post = get_object_or_404(Post, pk=pk)
        if comment_form.is_valid():
            c_form = comment_form.save(commit=False)
            c_form.author = request.user
            c_form.post = post
            c_form.save()
            return redirect(reverse('feeds:feed-detail-page', kwargs={'pk': post.pk}))
        context = {'feed': post, 'comment_form': comment_form,}
        return render(request, 'feeds/feed_detail.html', context)


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, edit.UpdateView):
    model = Post
    fields = ['body', 'image']
    template_name = 'feeds/feed_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('feeds:feed-detail-page', kwargs={'pk': pk})

    def test_func(self):
        object = self.get_object()
        if object.author == self.request.user:
            return True
        else:
            return False


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, edit.DeleteView):
    model = Post
    template_name = 'feeds/feed_delete.html'
    success_url =  reverse_lazy('feeds:feeds-page')

    def test_func(self):
        object = self.get_object()
        if object.author == self.request.user:
            return True
        else:
            return False


class CommentUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author == request.user:
            form = CommentForm(instance=comment)
            context = {'form': form, 'title': 'comment',}
            return render(request, 'feeds/edit_comment.html', context) 
        else:
            messages.warning(request, 'You are not allowed to view that page')
            return redirect('feeds:feeds-page')       

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            c_form = form.save(commit=False)
            c_form.author = request.user
            c_form.post = comment.post
            c_form.save()
            return redirect(reverse('feeds:feed-detail-page', kwargs={'pk': comment.post.pk}))


class CommentDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author == request.user:
           return render(request, 'feeds/delete_comment.html')
        else:
            messages.warning(request, 'You are not allowed to view that page')
            return redirect('feeds:feeds-page')

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return redirect(reverse('feeds:feed-detail-page', kwargs={'pk': comment.post.pk}))


class LikeFeedView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        likes = post.likes.all()

        if request.user in likes:
            liked = True
        else:
            liked = False

        if liked == False:
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

