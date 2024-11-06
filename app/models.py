import base64
import imghdr
from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from io import BytesIO
from django.utils import timezone
import datetime

class Game(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, default="Undefined")
    description = models.TextField(default="")
    release_date = models.PositiveIntegerField(default=0)
    image_url = models.URLField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Salva o jogo
        super().save(*args, **kwargs)
        
        # Verifica se já existe um fórum associado a este jogo
        if not hasattr(self, 'forum'):
            # Cria o fórum para o jogo, caso não exista
            Forum.objects.create(game=self)

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
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)  # Adiciona o campo comentario

    class Meta:
        unique_together = ('user', 'game')
    
    def __str__(self):
        return f'{self.user.username} - {self.game.title} - {self.rating}'
    
class Forum(models.Model):

    game =  models.OneToOneField(Game, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='users_forum', blank=True)


class Question(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    details = models.TextField(null=False)
    created_date = models.DateTimeField("Created on", auto_now_add=True)
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def _str_(self):
        return "[" + str(self.id) + "] " + self.title
    
    def was_published_recently(self):
        return self.created_date >= timezone.now() - datetime.timedelta(days=1)

    def detail_string(self):
        return "id: " + str(self.id) + "; title: " + self.title + "; details: " + self.details +  "; created_date: " + str(self.created_date) + "; username: " + self.username

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    votes = models.IntegerField(default=0)
    created_date = models.DateTimeField("Created on", auto_now_add=True)
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def _str_(self):
        return "[" + str(self.id) + "] " + self.text
    
    def was_published_recently(self):
        return self.created_date >= timezone.now() - datetime.timedelta(days=1)    