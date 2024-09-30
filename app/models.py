from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User

class Game(models.Model):

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, default="Undefined")
    description = models.TextField(default="")
    release_date = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='games/', default='Undefined.jpg')
    
    def __str__(self):
        return self.title
    
    @classmethod
    def get_all_games(cls):
        return cls.objects.all()

    def get_to_play_count(self):
        return self.user_set.filter(to_play=self).count()
    
    def get_playing_count(self):
        return self.user_set.filter(playing_now=self).count()
    
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_description = models.CharField(max_length=500, blank=True)
    favorite_list = models.ManyToManyField(Game, related_name='favorited_by', blank=True)
    to_play = models.ManyToManyField(Game, related_name="will_be_played_by", blank=True)
    playing_now = models.ManyToManyField(Game, related_name="being_played_by", blank=True)
    already_played = models.ManyToManyField(Game, related_name='played_by', blank=True)

    def set_user_description(self, description: str):
        """Modify and save the user's description."""
        self.user_description = description
        self.save()


# Modelo que permite aos usuários avaliarem os jogos
class GameRating(models.Model):

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Relaciona a avaliação a um usuário
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # Relaciona a avaliação a um jogo
    rating = models.IntegerField()  # Avaliação (nota) do jogo pelo usuário

    class Meta:
        # Assegura que um usuário só pode avaliar um jogo uma vez
        unique_together = ('user', 'game')

    def __str__(self):
        # Retorna uma string que exibe o nome do usuário, o jogo e a avaliação
        return f'{self.user.username} - {self.game.nome} - {self.rating}'
