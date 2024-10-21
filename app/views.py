from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .models import Profile, Game

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

        if action == 'add_to_playing_now':
            profile.playing_now.add(game)
            return redirect('gamelist')

        elif action == 'add_to_to_play':
            profile.to_play.add(game)
            return redirect('gamelist')

        elif action == 'add_to_already_played':
            profile.already_played.add(game)
            return redirect('gamelist')

        elif action == 'add_to_favorite_list':
            profile.favorite_list.add(game)
            return redirect('gamelist')

        elif action == 'remove_from_favorite_list':
            profile.favorite_list.remove(game)
            return redirect('gamelist')

        else:
            messages.error(request, 'Invalid action.')
            return redirect('gamelist')
        


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
#     404      #
################

def not_found(request, exception):
    return render(request, '404.html', status=404)
