from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login as lg
from django.contrib.auth.models import User
from .models import *
from .forms import *

class ProfileView(View):
    # Método que lida com as requisições GET
    def get(self, request):
        # Verifica se o usuário está autenticado
        if request.user.is_authenticated:
            # Filtra os jogos na lista "Quero Jogar" do usuário logado
            want_to_play = UserGameList.objects.filter(user=request.user, list_type='w')
            # Filtra os jogos na lista "Já Joguei" do usuário logado
            played = UserGameList.objects.filter(user=request.user, list_type='p')
            # Passa o contexto para o template com o nome do usuário e as listas de jogos
            all_games = Game.objects.all()
            # Pega todos os jogos para exibir na pag profile
            context = {
                "title": request.user.username,
                "want_to_play": want_to_play,
                "played": played,
                "all_games": all_games,
            }
        else:
            # Se o usuário não estiver logado, define o nome como "Visitante"
            # É AQUI QUE VAMOS ADICIONAR LISTA DE JOGOS MAIS POPULARES, MAIS JOGADOS E MAIS BEM AVALIADOS
            context = {"nome": "Visitante"}
        # Renderiza o template profile.html com o contexto
        return render(request, 'profile.html', context)

###################################################
# View para realizar o cadastro de novos usuários #
###################################################

class CadastroView(View):
    # Metodo que lida com as requisições GET e exibe o formulário de cadastro
    def get(self, request):
        return render(request, 'cadastro.html')

    # Metodo que lida com as requisições POST para criar um novo usuário
    def post(self, request):
        # Coleta os dados do formulário de cadastro
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Chama a função que cria o novo usuário
        self.criarUsuario(username, email, password)
        return redirect('profile')  # Redireciona para a pagina inicial após o cadastro

    # Função que cria um novo usuário, validando se ele já existe
    def criarUsuario(self, username, email, password):
        if self.obterUsuarioPorNome(username) is not None:
            raise ValueError("Usuário já existe")  # Erro caso o usuário já exista (possiveis ajustes futuros)
        else:
            # Cria um novo usuário e salva no banco de dados
            user = User.objects.create_user(username, email, password)
            user.save()

    # Função que verifica se um usuário já existe pelo nome de usuário
    def obterUsuarioPorNome(self, name):
        return User.objects.filter(username=name).first()
    
###########################################
# View para realizar o login dos usuários #
###########################################

class LoginView(View):
    # Método que lida com as requisições GET e exibe o formulario de login
    def get(self, request):
        return render(request, 'login.html')

    # Método que lida com as requisições POST para autenticar o usuário
    def post(self, request):
        # Coleta os dados do formulário de login
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Chama a função de autenticação
        self.loginUsuario(request, username, password)
        return redirect('profile')  # Redireciona para a página inicial após o login

    # Função que autentica o usuário com as credenciais fornecidas
    def loginUsuario(self, request, username, password):
        user = authenticate(username=username, password=password)  # Autentica o usuário

        if user is None:
            raise ValueError("Usuário ou senha inválidos")  # Erro se a autenticação falhar (possiveis ajustes futuro)
        else:
            lg(request, user)  # Realiza o login se a autenticação de tudo certo
            return


###################
#    Funções      #
###################

# Função para adicionar um jogo na lista de "Quero Jogar" ou "Já Joguei"
def add_to_list(request, game_id, list_type):
    # Obtem o jogo pelo ID
    game = Game.objects.get(id=game_id)
    # Verifica se o jogo já está na lista do usuário, evitando duplicação
    if not UserGameList.objects.filter(user=request.user, game=game, list_type=list_type).exists():
        # Adiciona o jogo na lista do usuário
        UserGameList.objects.create(user=request.user, game=game, list_type=list_type)
    return redirect('profile')  # Redireciona para a pgina inicial após adicionar o jogo

# Função para remover um jogo de uma lista
def remove_from_list(request, game_id, list_type):
    # Obtem o jogo pelo ID
    game = Game.objects.get(id=game_id)
    # Remove o jogo da lista do usuário
    UserGameList.objects.filter(user=request.user, game=game, list_type=list_type).delete()
    return redirect('profile')  # Redireciona para a pagina inicial após remover o jogo


class UserProfile(View):
    def get(self, request):

        context = {
            "games": Game.objects.all(),
        }

        return render(request, 'userprofile.html', context)
    

class CadastroView(View):
    # Metodo que lida com as requisições GET e exibe o formulário de cadastro
    def get(self, request):
        return render(request, 'cadastro.html')

    # Metodo que lida com as requisições POST para criar um novo usuário
    def post(self, request):
        # Coleta os dados do formulário de cadastro
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Verifica se o nome de usuário já existe no banco de dados
        if self.obterUsuarioPorNome(username) is not None:
            # Adiciona uma mensagem de erro se o usuário já existir
            messages.error(request, 'Usuário já existe.')
            return redirect('cadastro')  # Redireciona para a página de cadastro novamente
        elif self.obterUsuarioPorEmail(username) is not None:
            # Adiciona uma mensagem de erro se o usuário já existir
            messages.error(request, 'Usuário já existe.')
            return redirect('cadastro')  # Redireciona para a página de cadastro novamente
        else:
            self.criarUsuario(username, email, password)
            messages.success(request, 'Usuário cadastrado com sucesso.')
            return redirect('profile')
        
        

    # Função que cria um novo usuário, validando se ele já existe
    def criarUsuario(self, username, email, password):
        if self.obterUsuarioPorNome(username) is not None:
            raise ValueError("Usuário já existe")  # Erro caso o usuário já exista (possiveis ajustes futuros)
        else:
            # Cria um novo usuário e salva no banco de dados
            user = User.objects.create_user(username, email, password)
            user.save()

    # Função que verifica se um usuário já existe pelo nome de usuário
    def obterUsuarioPorNome(self, name):
        return User.objects.filter(username=name).first()
    
    def obterUsuarioPoremail(self, email):
        return User.objects.filter(email=email).first()
    
###########################################
# View para realizar o login dos usuários #
###########################################

class LoginView(View):
    # Método que lida com as requisições GET e exibe o formulario de login
    def get(self, request):
        return render(request, 'login.html')

    # Método que lida com as requisições POST para autenticar o usuário
    def post(self, request):
        # Coleta os dados do formulário de login
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentica o usuário com as credenciais fornecidas
        user = authenticate(username=username, password=password)

        if user is None:
            # Adiciona uma mensagem de erro se o usuário ou senha estiverem incorretos
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')  # Redireciona para a página de login novamente
        else:
            # Realiza o login do usuário se a autenticação for bem-sucedida
            lg(request, user)
            return redirect('profile') # Redireciona para a página de perfil após o login bem-sucedido