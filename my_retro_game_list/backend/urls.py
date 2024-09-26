from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from frontend.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('profilea/', ProfileView.as_view(), name='profilee'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('add_to_list/<int:game_id>/<str:list_type>/', add_to_list, name='add_to_list'),
    path('remove_from_list/<int:game_id>/<str:list_type>/', remove_from_list, name='remove_from_list'),
]

# Add media URL pattern only if in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)