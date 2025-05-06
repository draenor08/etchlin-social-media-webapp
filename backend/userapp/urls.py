from django.urls import path
from . import views  # this imports from userapp/views.py

urlpatterns = [
    path('auth/check/', views.check_auth, name='check_auth'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('me/', views.get_own_profile, name='get_own_profile'),
    path('<str:user_id>/profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
]

'''urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name ="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
]'''