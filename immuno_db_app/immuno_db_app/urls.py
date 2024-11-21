from django.contrib import admin
from django.urls import path
from query import views
from query.views import PSMView
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    # db
    path('', views.home, name='home'),
    path('psms/', PSMView.as_view(), name='psms'),
    path('psm_spectrum_info/<int:psm_code>/', views.psm_spectrum_info, name='psm_spectrum_info'),
    path('overview/', views.overview, name='overview'),
    path('legal_notice/', views.legal_notice, name='legal_notice'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
]
