from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from fileupload import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('success/', views.success, name='success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
