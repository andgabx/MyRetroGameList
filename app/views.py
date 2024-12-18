from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from .models import Profile, Game, GameRating, Forum, Question, Answer
from django.db.models import Avg


##############################
# Cadastro de novos usuários #
##############################

class RegisterView(View):
    
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Basic validation
        if not username or not email or not password:
            messages.error(request, 'Please, fill all fields.')
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=user)
            
            messages.success(request, 'User registered!')
            return redirect('login')
        
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('register')
    

####################
#   Autenticação   #
####################

class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username') 
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Error during login! Check your credentials.')
                return redirect('login')
        except Exception as e:
            messages.error(request, f'Error during login: {str(e)}')
            return redirect('login')
        
class LogoutView(View):

    def get(self, request):
        try:
            if request.user.is_authenticated:
                logout(request)
                return redirect('home')
            else:
                messages.error(request, 'You are not logged in!')
                return redirect('home')
        except Exception as e:
            messages.error(request, f'Error during logout: {str(e)}')
            return redirect('home')


################################
#  Mostrar perfis de usuário   #
################################

class ExternalUserProfileDisplayView(View):
    def get(self, request, id):
        profile = get_object_or_404(Profile, user__id=id)
        isProfileOwner = request.user.id == id
        
        context = {
            'profile': profile,
            'isProfileOwner' : isProfileOwner,
        }
        return render(request, 'edit_profile.html', context)
    

class EditProfileDescriptionView(LoginRequiredMixin, View):
    login_url = '/home/'

    def get(self, request, id):
        profile = get_object_or_404(Profile, user__id=id)
        context = {
            'profile': profile
        }
        return render(request, "edit_profile.html", context)

    def post(self, request, id):
        profile = get_object_or_404(Profile, user__id=id)
        profile.user_description = request.POST.get('description')
        profile.save()
        return redirect(reverse("userprofile", args=[profile.user.id]))



################
#  ADICIONAR   #
################

class ManageGameRemovalView(View):
    def post(self, request, action, id):
        game = get_object_or_404(Game, id=id)
        profile = get_object_or_404(Profile, user=request.user)

        if action == 'remove_from_playing_now':
            profile.playing_now.remove(game)
            return redirect('gamelist')

        elif action == 'remove_from_already_played':
            profile.already_played.remove(game)
            return redirect('gamelist')

        elif action == 'remove_from_to_play':
            profile.to_play.remove(game)
            return redirect('gamelist')

        elif action == 'remove_from_favorite_list':
            profile.favorite_list.remove(game)
            return redirect('gamelist')

        else:
            return redirect('gamelist', {'error': 'Invalid action.'})


###########
# REMOVER # 
###########

class ManageGameAdditionView(View):
    def post(self, request, action, id):
        game = get_object_or_404(Game, id=id)
        profile, created = Profile.objects.get_or_create(user=request.user)

        # Verifica a ação e alterna o status
        if action == 'add_to_favorite_list':
            if game in profile.favorite_list.all():
                profile.favorite_list.remove(game)
                added = False
            else:
                profile.favorite_list.add(game)
                added = True
            return JsonResponse({'success': True, 'added': added})

        elif action == 'add_to_already_played':
            if game in profile.already_played.all():
                profile.already_played.remove(game)
                added = False
            else:
                profile.already_played.add(game)
                added = True
            return JsonResponse({'success': True, 'added': added})

        elif action == 'add_to_to_play':
            if game in profile.to_play.all():
                profile.to_play.remove(game)
                added = False
            else:
                profile.to_play.add(game)
                added = True
            return JsonResponse({'success': True, 'added': added})

        # Retorno para outras ações inválidas
        return JsonResponse({'success': False})


####################
#       HOME       #
####################

class HomeView(View):
    def get(self, request):
        context = {
            'top_to_play': Game.top_4_to_play(),
            'top_favorites': Game.top_4_favorite_list(),
            'top_playing_now': Game.top_4_playing_now(),
            'top_already_played': Game.top_4_already_played(),
            'user': request.user,
        }
        return render(request, 'home.html', context)
    

################
#     List     #
################

class GameListView(View):
    def get(self, request):
        add_manager = ManageGameAdditionView()
        remove_manager = ManageGameRemovalView()
        context = {
            "add_manager" : add_manager,
            "remove_manager" : remove_manager,
            "games" : Game.get_all_games(),
            "user" : request.user,
        }
        return render(request, "gamelist.html", context)
    
################
#   Game Page  #
################

class GamePageView(View):
    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        ratings = GameRating.objects.filter(game=game)
        average_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0

        context = {
            'game': game,
            'ratings': ratings,
            'average_rating': round(average_rating, 1),
        }
        return render(request, "gamepage.html", context)

@method_decorator(login_required, name='dispatch')
class AddReviewView(View):
    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        rating_value = request.POST.get('rating')
        comentario = request.POST.get('comentario')

        if rating_value and comentario:
            GameRating.objects.create(
                game=game,
                user=request.user,
                rating=int(rating_value),
                comentario=comentario
            )
        
        return redirect('gamepage', game_id=game.id)

@method_decorator(login_required, name='dispatch')
class DeleteReview(View):
    def post(self, request, review_id):
        review = get_object_or_404(GameRating, id=review_id, user=request.user)
        review.delete()
        return redirect('gamepage', game_id=review.game.id)

@method_decorator(login_required, name='dispatch')
class EditReview(View):
    def post(self, request, review_id):
    
        review = get_object_or_404(GameRating, id=review_id, user=request.user)
        
        new_rating = request.POST.get('rating')
        new_comment = request.POST.get('comentario')

        if new_rating and new_comment:
            review.rating = int(new_rating)
            review.comentario = new_comment
            review.save()
        return redirect('gamepage', game_id=review.game.id)

################
#   Forum  #
################
from django.shortcuts import render
from .models import Game, Forum  # Certifique-se de que os modelos estão corretos

class ForumListView(View):
    def get(self, request):
        games = Game.objects.all()  # Supondo que 'Game' seja o modelo para jogos
        forums = Forum.objects.all()  # Supondo que 'Forum' seja o modelo para fóruns

        context = {
            'games': games,
            'forums': forums,
        }
        return render(request, 'forum_list.html', context)
    
class ForumDetailView(View):
    def get(self, request, forum_id):
        forum = get_object_or_404(Forum, id=forum_id)
        questions = forum.question_set.all()
        return render(request, 'forum_detail.html', {'forum': forum, 'questions': questions})

class AddQuestionView(LoginRequiredMixin, View):
    login_url = '/home/'

    def post(self, request, forum_id):
        forum = get_object_or_404(Forum, id=forum_id)
        title = request.POST.get('title')
        details = request.POST.get('details')

        if title and details:
            question = Question(forum=forum, title=title, details=details, username=request.user)
            question.save()
        else:
            messages.error(request, "preencha todos os campos.")

        return redirect('forum_detail', forum_id=forum.id)

class AddAnswerView(LoginRequiredMixin, View):
    login_url = '/home/'

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        text = request.POST.get('text')

        if text:
            answer = Answer(question=question, text=text, username=request.user)
            answer.save()
        else:
            messages.error(request, "Digite algo.")

        return redirect('forum_detail', forum_id=question.forum.id)


class EditQuestionView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, forum_id, question_id):
        question = get_object_or_404(Question, id=question_id)
        if question.username != request.user:
            messages.error(request, "You do not have permission to edit this question.")
            return redirect('forum_detail', forum_id=forum_id)
        return render(request, 'forum_detail.html', {'edit_question': question})

    def post(self, request, forum_id, question_id):
        question = get_object_or_404(Question, id=question_id)
        if question.username == request.user:
            question.title = request.POST.get('title')
            question.details = request.POST.get('details')
            question.save()
        return redirect('forum_detail', forum_id=forum_id)


class EditAnswerView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, forum_id, answer_id):
        answer = get_object_or_404(Answer, id=answer_id)
        if answer.username != request.user:
            messages.error(request, "You do not have permission to edit this answer.")
            return redirect('forum_detail', forum_id=forum_id)
        return render(request, 'forum_detail.html', {'edit_answer': answer})

    def post(self, request, forum_id, answer_id):
        answer = get_object_or_404(Answer, id=answer_id)
        if answer.username == request.user:
            answer.text = request.POST.get('text')
            answer.save()
        return redirect('forum_detail', forum_id=forum_id)
class DeleteQuestionView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        forum_id = question.forum.id
        question.delete()
        return redirect('forum_detail', forum_id=forum_id)
class DeleteAnswerView(View):
    def get(self, request, answer_id):
        answer = get_object_or_404(Answer, id=answer_id)
        forum_id = answer.question.forum.id
        answer.delete()
        return redirect('forum_detail', forum_id=forum_id)

class GameDetailView(View):
    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        ratings = GameRating.objects.filter(game=game)
        average_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0

        context = {
            'game': game,
            'ratings': ratings,
            'average_rating': round(average_rating, 1),
        }
        
        return render(request, 'gamepage.html', context)
    


class GameSearch(View):
    def get(self, request):
        query = request.GET.get('q')
        games = Game.objects.all()
        
        if query:
            # Filtra os jogos pelo nome, ignorando maiúsculas e minúsculas
            games = games.filter(title__icontains=query)
        
        context = {
            'games': games,
            'query': query,
        }
        return render(request, 'game_search_results.html', context)
    


################
#     404      #
################

def not_found(request, exception):
    return render(request, '404.html', status=404)
