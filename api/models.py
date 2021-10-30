from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from users.models import User

from api.validators import my_year_validator


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'


class Genre(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)


class Title(models.Model):
    name = models.CharField(max_length=250)
    year = models.SmallIntegerField(validators=[my_year_validator], blank=True)
    category = models.ForeignKey(Category,
                                 related_name='title',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 )
    genre = models.ManyToManyField(Genre, related_name='title')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='just_one_review_per_author')
        ]


class Comments(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments'
                               )
    text = models.TextField()
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments'
                               )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-pub_date']
