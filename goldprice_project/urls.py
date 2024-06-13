"""
URL configuration for goldprice_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from goldprice_app import views as goldprice_views  

urlpatterns = [
    # Only one entry for the admin:
    path('admin/', admin.site.urls),
    # Include the goldprice_app urls:
    path('', include('goldprice_app.urls')),  # Assuming you want the app accessible from the root

    # Django's built-in authentication system (if you're using it):
    path('accounts/', include('django.contrib.auth.urls')),

]


