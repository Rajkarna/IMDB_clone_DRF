from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



from django.urls import path
from .views import RegisterAV, logout_view


urlpatterns = [
    path('login/', obtain_auth_token, name="login"),
    path('register/', RegisterAV, name="register"),
    path('logout/', logout_view, name="logout"),
    
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
