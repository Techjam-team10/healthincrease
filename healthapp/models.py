from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.title
    

class Target(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="targets"
    )
    term = models.DateField()
    content = models.TextField()
    achievement_level = models.SmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )

    def __str__(self):
        return f"{self.user.mail} - {self.term}"


class LifeStyle(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="life_styles"
    )
    date = models.DateField()
    time = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="life_styles"
    )
    content = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.user.mail} - {self.date}"


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    content = models.TextField()
    favorite = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post {self.id} by {self.user.mail}"


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    content = models.TextField()

    def __str__(self):
        return f"Comment {self.id}"


class RadarChart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="radar_chart"
    )
    data1 = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    data2 = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    data3 = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    data4 = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    data5 = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    data6 = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"RadarChart for {self.user.mail}"