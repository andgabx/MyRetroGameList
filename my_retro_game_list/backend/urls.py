from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from frontend.views import HomeView, LoginView, ExternalUserProfileDisplayView, CadastroView, ManageGameRemovalView, ManageGameAdditionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    path('home/', HomeView.as_view(), name="home"),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/<int:id>/', ExternalUserProfileDisplayView.as_view(), name='userprofile'),
    path('user/None/', LoginView.as_view(), name='login'),
    path('game/remove/<str:action>/<int:id>/', ManageGameRemovalView.as_view(), name='manage_game_removal'),
    path('game/add/<str:action>/<int:id>/', ManageGameAdditionView.as_view(), name='manage_game_removal'),
]

# Add media URL pattern only if in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)