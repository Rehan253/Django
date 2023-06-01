from sqlite3 import IntegrityError
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView,DetailView,ListView,UpdateView,DeleteView,RedirectView
from groups.models import Group,GroupMember
from django.contrib import messages
from groups.models import Group,GroupMember
from groups import models
# Create your views here.

 
class CreateGroup(LoginRequiredMixin,CreateView):
    fields = ('name','description')
    model = Group
    

 
class ListGroup(ListView):
    model = Group


class SingleGroup(DetailView):
    model = Group
    

class JoinGroup(LoginRequiredMixin,RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args , **kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning("You are already member of this Group!")

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))
        
        return super().get(request, *args, **kwargs)




class LeaveGroup(LoginRequiredMixin,RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
             membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request,"Sorry you are not member of this group!")

        else:
            membership.delete()
            messages.success(self.request,"You have left the group!")

        return super().get(request,*args,**kwargs)

        



















































    

