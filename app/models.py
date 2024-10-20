import base64
import imghdr
from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User

class Game(models.Model):

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, default="Undefined")
    description = models.TextField(default="")
    release_date = models.PositiveIntegerField(default=0)
    image = models.BinaryField(blank=True, null=True)
    
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
    
    # O Azure não dá persistência aos arquivos de imagem upados durante uma sessão.
    # Sempre que o servidor reinicia, ele descarta as imagens.
    # Para contornar o problema, reescrevi o save de Game.
    # Agora as imagens são salvas diretamente no banco de dados como arquivos binários.
    # Para lê-las, convertemos de volta de binário para base 64 no get_image.
    
    def set_image(self, image_file):
        self._image_file = image_file
    
    def save(self, *args, **kwargs): 
        if hasattr(self, '_image_file'):
            self.image = self._image_file.read()
        super().save(*args, **kwargs)

    def get_image(self):
        if self.image:
            img_ext = imghdr.what(None, h=self.image)
            if img_ext:
                return f"data:image/{img_ext};base64," + base64.b64encode(self.image).decode('utf-8')
        return ""


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
