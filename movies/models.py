from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class CheckoutFeedback(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, help_text="User's name (optional)")
    feedback = models.TextField(help_text="User's thoughts on the checkout process")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        name_display = self.name if self.name else "Anonymous"
        return f"Feedback from {name_display} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"