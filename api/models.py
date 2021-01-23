from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User
import datetime as dt


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(
        max_length=100
    )
    year = models.PositiveIntegerField(
        validators=[MaxValueValidator(dt.date.today().year)]
    )
    description = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='Genre_Title',
        through_fields=('title', 'genre'),
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="titles",
    )
    
    class Meta:
        ordering = ['name']


class Review(models.Model):
    text = models.TextField(max_length=2000)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comments(models.Model):
    text = models.TextField(max_length=2000)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Genre_Title(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
