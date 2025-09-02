"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from new_app.views import tables_list, reserve_table, register, profile_view, base, delete_reservation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base),
    path('tables/', tables_list, name='tables'),
    path('reservations/new/<int:number>/', reserve_table, name='reservation'),
    path('login/', LoginView.as_view(next_page='/tables/'), name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(next_page='/tables/'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('reservation/delete/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
] + debug_toolbar_urls()+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
