from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q


class Favorite(models.Model):
    user = models.ForeignKey('authentication.Contributor', related_name='favorites', on_delete=models.CASCADE)
    favorite_ct = models.ForeignKey(
        ContentType, 
        related_name='favorite_obj', 
        on_delete=models.CASCADE
    )
    favorite_id = models.PositiveIntegerField()
    favorite = GenericForeignKey('favorite_ct', 'favorite_id')

    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.user} follows {self.favorite}'

    class Meta:
        ordering = ['favorite_ct']


class FavoritesModelMixin(models.Model):
    @property
    def favorites(self):
        return Favorite.objects.filter(
            Q(favorite_id=self.id) & Q(favorite_ct__model=self._meta.model_name)
        )

    class Meta:
        abstract = True


class Contributor(AbstractUser, FavoritesModelMixin):
    MODE_CHOICES = (
        ('private', 'PRIVATE'),
        ('public', 'PUBLIC'),
    )
    mode = models.CharField(
        max_length = 20,
        choices = MODE_CHOICES,
        default = 'private'
    )

