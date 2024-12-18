from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path


from app.views import (
    HomeView, LoginView, ExternalUserProfileDisplayView, RegisterView, 
    ManageGameRemovalView, ManageGameAdditionView, GameListView, LogoutView, 
    EditProfileDescriptionView, GamePageView, AddReviewView, DeleteReview, 
    EditReview, ForumListView, ForumDetailView, AddQuestionView, AddAnswerView, 
    GameDetailView, GameSearch, EditQuestionView, EditAnswerView,DeleteAnswerView,DeleteQuestionView
)

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
    path('user/<int:id>/', ExternalUserProfileDisplayView.as_view(), name='userprofile'),
    path('profile/edit/<int:id>/', EditProfileDescriptionView.as_view(), name='edit_profile_description'),

    # URL for non-existing user, redirects to login (you might want to make this an actual "user not found" page later)
    path('user/None/', LoginView.as_view(), name='login'),

    # Game list
    path('gamelist/', GameListView.as_view(), name='gamelist'),

    # Game addition and removal
    path('game/add/<str:action>/<int:id>/', ManageGameAdditionView.as_view(), name='manage_game_addition'),
    path('game/remove/<str:action>/<int:id>/', ManageGameRemovalView.as_view(), name='manage_game_removal'),

    # Game page and reviews
    path('gamepage/<int:game_id>/', GamePageView.as_view(), name='gamepage'), 
    path('gamepage/<int:game_id>/review/', AddReviewView.as_view(), name='add_review'),
    path('game/<int:review_id>/delete_review/', DeleteReview.as_view(), name='delete_review'),
    path('game/<int:review_id>/edit_review/', EditReview.as_view(), name='edit_review'),

    # Forum
    path('forum/', ForumListView.as_view(), name='forum_list'),  
    path('forum/<int:forum_id>/', ForumDetailView.as_view(), name='forum_detail'),  
    path('forum/<int:forum_id>/add-question/', AddQuestionView.as_view(), name='add_question'), 
    path('question/<int:question_id>/add-answer/', AddAnswerView.as_view(), name='add_answer'),
    path('forum/<int:forum_id>/question/edit/<int:question_id>/', EditQuestionView.as_view(), name='edit_question'),
    path('forum/<int:forum_id>/answer/edit/<int:answer_id>/', EditAnswerView.as_view(), name='edit_answer'),
    path('delete_answer/<int:answer_id>/', DeleteAnswerView.as_view(), name='delete_answer'),
    path('delete_question/<int:question_id>/',DeleteQuestionView.as_view(), name='delete_question'),

    

    # Game search and details
    path('search/', GameSearch.as_view(), name='game_search'),
    path('game/<int:game_id>/', GameDetailView.as_view(), name='game_details'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
