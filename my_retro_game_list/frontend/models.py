from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Modelo de um jogo
class Game(models.Model):
    title = models.CharField(max_length=100)  # Nome do jogo
    genre = models.CharField(max_length=100, default="Undefined")  # Gênero do jogo (com valor padrão)
    description = models.TextField()  # Descrição do jogo
    release_date = models.DateField()  # Data de lançamento do jogo
    like_count = models.PositiveIntegerField(default=0)  # Número de likes (preferências)
    to_play_count = models.PositiveIntegerField(default=0)  # Número de vezes que foi adicionado à lista "Quero Jogar"
    already_played_count = models.PositiveIntegerField(default=0)  # Número de vezes que foi adicionado à lista "Já Joguei"
    image = models.ImageField(upload_to='games/', default='Undefined.jpg')
    

    def __str__(self):
        return self.title  # Exibe o nome do jogo como sua representação em string
    
    @classmethod
    def get_id(self):
        """Returns the unique ID of a Game."""
        return self.id
    
    @classmethod # apagar esse troço aqui antes do release @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def get_all_games(cls):
        for game in Game.objects.all():
            print(game.title)
    

# Modelo que gerencia as listas de "Quero Jogar" e "Já Joguei" de cada usuário
class UserGameList(models.Model):
    # Tipos de listas disponíveis: 'w' para "Quero Jogar" e 'p' para "Já Joguei"
    LIST_TYPE_CHOICES = [
        ('w', 'Quero Jogar'),
        ('p', 'Já Joguei'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona um usuário à lista
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # Relaciona um jogo à lista
    list_type = models.CharField(max_length=1, choices=LIST_TYPE_CHOICES)  # Define o tipo de lista

    class Meta:
        # Assegura que um usuário só pode ter um jogo em uma lista específica (evita duplicações)
        unique_together = ('user', 'game', 'list_type')

    def __str__(self):
        # Retorna uma string que exibe o nome do usuário, o jogo e o tipo de lista
        return f'{self.user.username} - {self.game.nome} - {self.get_list_type_display()}'

# Modelo que permite aos usuários avaliarem os jogos
class GameRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona a avaliação a um usuário
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # Relaciona a avaliação a um jogo
    rating = models.IntegerField()  # Avaliação (nota) do jogo pelo usuário

    class Meta:
        # Assegura que um usuário só pode avaliar um jogo uma vez
        unique_together = ('user', 'game')

    def __str__(self):
        # Retorna uma string que exibe o nome do usuário, o jogo e a avaliação
        return f'{self.user.username} - {self.game.nome} - {self.rating}'


class UserInfo(models.Model):
    username = models.CharField(max_length=100)
    user_description = models.CharField(max_length=500)
    favorite_list = models.ManyToManyField(Game, related_name='faved_by')
    to_play = models.ManyToManyField(Game, related_name="will_be_played_by")
    already_played = models.ManyToManyField(Game, related_name='played_by')

    def clean(self):
        # Get all games in to_play and already_played
        to_play = set(self.to_play.all())
        already_played = set(self.already_played.all())

        # Check for intersection between to_play and already_played lists
        intersection = to_play.intersection(already_played)
        if intersection:
            raise ValidationError(
                f"The following games cannot be in both 'to_play' and 'already_played' lists: "
                f"{', '.join(game.title for game in intersection)}"
            )

    def save(self, *args, **kwargs):
        # Ensure clean is called before saving
        self.clean()
        super().save(*args, **kwargs)

@classmethod
def add_game_to_favorites(cls, request):
    game = Game.objects.get(id=request.id)
    
    # Check if the game is already in the user's favorite list
    if not UserGameList.objects.filter(user=request.user, game=game, list_type='favorite_list').exists():
        # Add the game to the user's favorite list
        UserGameList.objects.create(user=request.user, game=game, list_type='favorite_list')
        return True  # Game was successfully added
    
    return False  # Game was not added because it already exists



