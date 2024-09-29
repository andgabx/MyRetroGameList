from django.db import models
from django.db.models import Count
from django.contrib.auth.models import AbstractUser

class Game(models.Model):

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, default="Undefined")
    description = models.TextField()
    release_date = models.PositiveIntegerField()
    image = models.ImageField(upload_to='games/', default='Undefined.jpg')
    
    def __str__(self):
        return self.title
    
    @classmethod
    def get_all_games(cls):
        return cls.objects.all()

    def get_to_play_count(self):
        return self.user_set.filter(to_play=self).count()
    
    def get_playing_count(self):
        return self.user_set.filter(playing=self).count()
    
    def get_already_played_count(self):
        return self.user_set.filter(already_played=self).count()
    

    @classmethod
    def top_4_to_play(cls):
        top_games = cls.objects.annotate(
            num_users=Count('will_be_played_by')
        ).order_by('-num_users')[:4]

        return top_games
    
    @classmethod
    def top_4_favorite_list(cls):
        top_games = cls.objects.annotate(
            num_users=Count('favorited_by')
        ).order_by('-num_users')[:4]

        return top_games
    
    @classmethod
    def top_4_playing_now(cls):
        top_games = cls.objects.annotate(
            num_users=Count('being_played_by')
        ).order_by('-num_users')[:4]

        return top_games
    
    @classmethod
    def top_4_already_played(cls):
        top_games = cls.objects.annotate(
            num_users=Count('played_by')
        ).order_by('-num_users')[:4]

        return top_games


class User(AbstractUser):
    user_description = models.CharField(max_length=500)
    favorite_list = models.ManyToManyField(Game, related_name='favorited_by')
    to_play = models.ManyToManyField(Game, related_name="will_be_played_by")
    playing_now = models.ManyToManyField(Game, related_name="being_played_by")
    already_played = models.ManyToManyField(Game, related_name='played_by')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Change this to something unique
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Change this to something unique
        blank=True
    )

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def set_user_description(self, description: str):
        """Modifica e salva a descrição do usuário."""
        self.user_description = description
        self.save()

    # Defs de add

    def add_to_playing_now(self, id):
        """Adds a game to the 'Playing Now' list of a user."""
        try:
            game = Game.objects.get(id=id)
            if not self.playing_now.filter(id=game.id).exists():
                self.playing_now.add(game)
                self.save()
        except Game.DoesNotExist:
            pass

    def add_to_to_play(self, id):
        """Adds a game to the 'To Play' list of a user."""
        try:
            game = Game.objects.get(id=id)
            if not self.to_play.filter(id=game.id).exists():
                self.to_play.add(game)
                self.save()
        except Game.DoesNotExist:
            pass

    def add_to_already_played(self, id):
        """Adds a game to the 'Already Played' list of a user."""
        try:
            game = Game.objects.get(id=id)
            if not self.already_played.filter(id=game.id).exists():
                self.already_played.add(game)
                self.save()
        except Game.DoesNotExist:
            pass

    def add_to_favorite_list(self, id):
        """Adiciona um jogo a "Favorite List" de um usuário."""
        try:
            game = Game.objects.get(id=id)
            if not self.favorite_list.filter(id=game.id).exists():
                self.favorite_list.add(game)
                self.save()
        except:
            pass

        

# Defs de remover 

    def remove_playing_now(self, id):
        """Adiciona um jogo a "Already Played" de um usuário."""
        try:
            game = Game.objects.get(id=id)
            self.playing_now.remove(game)
            self.save()
        except Game.DoesNotExist:
            pass

    def remove_from_already_played(self, id):
        """Adiciona um jogo a "Already Played" de um usuário."""
        try:
            game = Game.objects.get(id=id)
            self.already_played.remove(game)
            self.save()
        except Game.DoesNotExist:
            pass

    def remove_from_to_play(self, id):
        """Adiciona um jogo a "Already Played" de um usuário."""
        try:
            game = Game.objects.get(id=id)
            self.to_play.remove(game)
            self.save()
        except Game.DoesNotExist:
            pass

    def remove_from_already_played(self, id):
        """Adiciona um jogo a "Already Played" de um usuário."""
        try:
            game = Game.objects.get(id=id)
            self.already_played.remove(game)
            self.save()
        except Game.DoesNotExist:
            pass

    def remove_from_favorite_list(self, id):
        """Adiciona um jogo a "Already Played" de um usuário."""
        try:
            game = Game.objects.get(id=id)
            self.favorite_list.remove(game)
            self.save()
        except Game.DoesNotExist:
            pass
    
    @staticmethod
    def get_public_profile_details(**kwargs):
        return User.objects.prefetch_related('favorite_list', 'to_play', 'playing_now', 'already_played').get(**kwargs)


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
