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


class MoviePetition(models.Model):
    movie_title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions')
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.movie_title
    
    def vote_count(self):
        return self.votes.count()

class PetitionVote(models.Model):
    petition = models.ForeignKey(MoviePetition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('petition', 'user')
    
    def __str__(self):
        return f"{self.user.username} voted for {self.petition.movie_title}"