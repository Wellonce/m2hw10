from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from apps.gap.models import Room, Opinion, Comment, OpinionLike
from django.contrib import messages
from .forms import UserLoginForm, UserRegisterForm


class RoomListView(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'gap/rooms.html', {"rooms": rooms})


class RoomDetailView(View):
    def get(self, request, pk):
        room = Room.objects.get(pk=pk)

        opinions = sorted(Opinion.objects.filter(room=room), key=lambda o: o.like_count, reverse=True)
        context = {
            "room": room,
            "opinions": opinions
        }
        return render(request, "gap/opinoins.html", context=context)


class LikeOpinionView(View):
    def get(self, request, pk):
        opinion = Opinion.objects.get(pk=pk)
        like, created = OpinionLike.objects.get_or_create(user=request.user, opinion=opinion)
        if not created:
            like.delete()
        return redirect(reverse("gap:room", kwargs={"pk": opinion.room.pk}))


class OpinionDetailView(View):
    def get(self, request, pk):
        opinion = Opinion.objects.get(pk=pk)
        comments = opinion.comments.all().order_by("-created_at")
        context = {
            "opinion": opinion,
            "comments": comments
        }
        return render(request, "gap/comments.html", context=context)

class Loginview(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "gap/login.html", {'form': form})
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, f"you have logged in as {username}")
                return redirect ('landing_page')
            else:
                messages.erorr(request, "Wrong username or password")
                return render(request, "users/login.html", {"form": form})
        else:
            return render(request, "users/login.html", {"form": form})
        

class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render (request, "gap/register.html", {'form': form})
    
    def post (self, request):
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Sucessfully registered")
            return redirect("gap:login-page")
        else:
            return render(request, "gap/register.html", {'form':form})

class UserLogout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "user successfully logged out!")
        return redirect ('landing_page')