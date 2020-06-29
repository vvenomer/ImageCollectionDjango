from datetime import datetime
from django.http import HttpRequest
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import django.views.generic as djangoViews
from app.models import Image, Comment
from app.forms import ImageForm, BootstrapUserCreationForm
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest

class Home(djangoViews.ListView):
    template_name = 'app/image_list.html'
    queryset = Image.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Główna'
        context['year'] = datetime.now().year
        return context

class AddImage(PermissionRequiredMixin, djangoViews.CreateView):
    login_url = '/login/'
    template_name = 'app/image_create.html'
    permission_required = 'app.add_image'
    form_class = ImageForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dodaj obraz'
        context['year'] = datetime.now().year
        return context

def imageDetails(request, id):
    img = Image.objects.get(id=id)
    comments = img.comment_set.all()
    return render(request, 'app/image_detail.html', {
        'title': f'Obraz: {img.title}',
        'img': img,
        'comments': comments,
        'year': datetime.now().year,
        })

@login_required
def deleteImage(request, id): 
    if request.method == 'POST':
        img = Image.objects.get(id=id)
        if request.user.id == img.user.id:
            img.delete()
            return redirect('/')
        return HttpResponseForbidden()
    return HttpResponseBadRequest()

@login_required
def addComment(request, imageId):
    if not request.user.groups.filter(name='Komentator').exists():
        return HttpResponseForbidden() 
    if Image.objects.filter(id = imageId).exists():
        Comment.objects.create(user_id = request.user.id, content = request.POST['content'], image_id = imageId)
        return redirect(f'/obraz/{imageId}')   
    return HttpResponseBadRequest()


@login_required
def deleteComment(request, id):
    comment = Comment.objects.get(id=id)
    imgId = comment.image_id
    if request.method == 'POST': 
        if request.user.id == comment.user.id:
            comment.delete()
            return redirect(f'/obraz/{imgId}')
        return HttpResponseForbidden() 
    return HttpResponseBadRequest()

def register(request):
    if request.method == 'POST':
        form = BootstrapUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            group = Group.objects.get(name='Komentator')
            user.groups.add(group)
            login(request, user)
            return redirect('/')
    else:
        form = BootstrapUserCreationForm()
    return render(request, 'app/register.html', {
        'title': 'Rejestracja',
        'form': form,
        'year': datetime.now().year,
        })

def bad_request(request, exception):
    return render(request, 'app/400.html', {
        'title': 'Błąd w żądaniu',
        'year': datetime.now().year,
        }, status = 400)

def permission_denied(request, exception):
    return render(request, 'app/403.html', {
        'title': 'Brak dostępu',
        'year': datetime.now().year,
        }, status = 403)

def page_not_found(request, exception):
    return render(request, 'app/404.html', {
        'title': 'Strona nie znaleziona',
        'year': datetime.now().year,
        }, status = 404)

def server_error(request):
    return render(request, 'app/500.html', {
        'title': 'Błąd serwera',
        'year': datetime.now().year,
        }, status = 500)