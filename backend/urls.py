from django.contrib import admin
from django.urls import path
from userapp import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register_user, name='register'),
    path('login/', user_views.login_user, name='login'),
] + + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
