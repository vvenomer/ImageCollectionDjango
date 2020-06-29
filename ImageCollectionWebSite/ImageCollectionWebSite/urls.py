"""
Definition of urls for ImageCollectionWebSite.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import views, forms
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

handler400 = 'app.views.bad_request'
handler403 = 'app.views.permission_denied'
handler404 = 'app.views.page_not_found'
handler500 = 'app.views.server_error'


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('dodajObraz', views.AddImage.as_view(), name='addImage'),
    path('obraz/<int:id>', views.imageDetails, name='image'),
    path('usunObraz/<int:id>', views.deleteImage, name='deleteImage'),
    path('dodajKomentarz/<int:imageId>', views.addComment, name='addComment'),
    path('usunKomentarz/<int:id>', views.deleteComment, name='deleteComment'),

    path('login/', LoginView.as_view(
        template_name = 'app/login.html',
        authentication_form = forms.BootstrapAuthenticationForm,
        extra_context = {
            'title': 'Logowanie',
            'year' : datetime.now().year,
        }), name='login'),
    path('rejestracja/', views.register, name='register'),
    path('wylogowanie/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls, name='admin'),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
