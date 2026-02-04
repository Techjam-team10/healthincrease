from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    title = models.CharField(
        max_length=100
    )

    class Meta:
        db_table = "category"
        unique_together = ("parent", "title")
        ordering = ["parent_id", "id"]

    def __str__(self):
        if self.parent:
            return f"{self.parent.title} / {self.title}"
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
    time = models.DecimalField(
        max_digits=5,
        decimal_places=1,
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
    self_evaluation = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
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


class RadarChartData(models.Model):
    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="radar_data"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="radar_values"
    )

    value = models.SmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    class Meta:
        db_table = "radar_chart_data"
        unique_together = ("user", "category")
        ordering = ["user_id", "category_id"]

    def __str__(self):
        return f"{self.user.mail} - {self.category.title}: {self.value}"