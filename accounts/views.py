from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from .forms import RegisterUserForm, UserProfileForm
from .models import Profile


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class RegisterUserView(View):
    def get(self, request):
        form = RegisterUserForm()
        context = {'form': form, 'title': 'register',}
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account created successfully')
            form.save()
            return redirect('login-page')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        user = profile.user
        followers = profile.followers.all()
        num_of_followers = len(followers)

        if num_of_followers == 0:
            following = False

        if request.user in followers:
            following = True
        else:
            following = False

        form = UserProfileForm(instance=profile)
        context = {
            'profile': profile, 'user': user, 'num_of_followers': num_of_followers, 
            'following': following, 'form': form, 'title': 'profile',
        }
        return render(request, 'accounts/user_profile.html', context)

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            messages.success(request, 'Successfully Updated Profile')
            return redirect('profile-page', pk=profile.pk)


class PeopleView(LoginRequiredMixin, View):
    def get(self, request):
        people = User.objects.all().order_by('?')
        context = {'people': people, 'title': 'Discover People'}
        return render(request, 'accounts/people.html', context)


class FollowView(LoginRequiredMixin, View):
    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        profile.followers.add(request.user)

        return redirect('profile-page', pk=pk)


class UnFollowView(LoginRequiredMixin, View):
    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        profile.followers.remove(request.user)

        return redirect('profile-page', pk=pk)