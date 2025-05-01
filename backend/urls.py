from django.contrib import admin
from django.urls import include, path
from userapp import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register_user, name='register'),
    path('login/', user_views.login_user, name='login'),
    path('post/', include('postapp.urls')),
    path('comment/', include('commentapp.urls')),
    path('like/', include('likeapp.urls')),
    path('user/', include('userapp.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
