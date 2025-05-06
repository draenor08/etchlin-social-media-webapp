from django.contrib import admin
from django.urls import include, path
from userapp import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('userapp.urls')),
    path('api/', include('postapp.urls')),
    path('api/', include('commentapp.urls')),
    path('api/', include('likeapp.urls')),
    path('api/', include('messageapp.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
'''urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name ="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
]'''