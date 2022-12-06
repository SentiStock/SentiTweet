from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q


class CustomUser(AbstractUser):
    MODE_CHOICES = (
        ('private', 'PRIVATE'),
        ('public', 'PUBLIC'),
    )
    mode = models.CharField(
        max_length = 20,
        choices = MODE_CHOICES,
        default = 'private'
    )


class UserFollowing(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(
        CustomUser, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following_user'],  name="unique_followers")
        ]

        ordering = ["-created"]

    def __str__(self):
        f"{self.user} follows {self.following_user}"


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, related_name='favorites', on_delete=models.CASCADE)
    favorite_ct = models.ForeignKey(
        ContentType, 
        related_name='favorite_obj', 
        on_delete=models.CASCADE
    )
    favorite_id = models.PositiveIntegerField()
    favorite = GenericForeignKey('favorite_ct', 'favorite_id')

    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.user} likes {self.favorite}'

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
