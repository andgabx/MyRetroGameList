from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.views import HomeView, LoginView, ExternalUserProfileDisplayView, RegisterView, ManageGameRemovalView, ManageGameAdditionView, GameListView, LogoutView, EditProfileDescriptionView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Home
    path('', HomeView.as_view(), name="home"),
    path('home/', HomeView.as_view(), name="home"),

    # Login / Register
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    
    # User profile routing
    path('user/None/', LoginView.as_view(), name='login'), #trocar posteriormente para uma página de "user Not found"
    path('user/<int:id>/', ExternalUserProfileDisplayView.as_view(), name='userprofile'),
    path('profile/edit/<int:id>/', EditProfileDescriptionView.as_view(), name='edit_profile_description'),

    # Game list / Temporary
    path('gamelist/', GameListView.as_view(), name='gamelist'),

    # Game addition and removal (debug for now)
    path('game/add/<str:action>/<int:id>/', ManageGameAdditionView.as_view(), name='manage_game_addition'),
    path('game/remove/<str:action>/<int:id>/', ManageGameRemovalView.as_view(), name='manage_game_removal'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
