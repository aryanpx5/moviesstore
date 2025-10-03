from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, CheckoutFeedback, MoviePetition, PetitionVote
from .forms import CheckoutFeedbackForm, MoviePetitionForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Count

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

# CHECKOUT FEEDBACK VIEWS
def checkout_success(request):
    """View that shows after successful checkout - displays the feedback popup"""
    form = CheckoutFeedbackForm()
    context = {
        'feedback_form': form,
        'show_feedback_popup': True
    }
    return render(request, 'checkout/success.html', context)

@require_POST
def submit_feedback(request):
    """AJAX view to handle feedback submission"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = CheckoutFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your feedback!'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return redirect('checkout_success')

def feedback_list(request):
    """View to display all feedback statements on a separate page"""
    feedbacks = CheckoutFeedback.objects.all()
    context = {
        'feedbacks': feedbacks
    }
    return render(request, 'checkout/feedback_list.html', context)

# MOVIE PETITION VIEWS
@login_required
def petition_list(request):
    """Display all movie petitions sorted by vote count"""
    petitions = MoviePetition.objects.annotate(
        vote_count=Count('votes')
    ).order_by('-vote_count', '-created_at')
    
    # Get petitions user has voted on
    user_votes = PetitionVote.objects.filter(user=request.user).values_list('petition_id', flat=True)
    
    context = {
        'petitions': petitions,
        'user_votes': list(user_votes)
    }
    return render(request, 'movies/petitions.html', context)

@login_required
def create_petition(request):
    """Create a new movie petition"""
    if request.method == 'POST':
        form = MoviePetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Petition created successfully!')
            return redirect('petition_list')
    else:
        form = MoviePetitionForm()
    
    return render(request, 'movies/create_petition.html', {'form': form})

@login_required
def vote_petition(request, petition_id):
    """Toggle vote on a petition"""
    petition = get_object_or_404(MoviePetition, id=petition_id)
    
    # Check if user already voted
    existing_vote = PetitionVote.objects.filter(petition=petition, user=request.user).first()
    
    if existing_vote:
        # Remove vote
        existing_vote.delete()
        messages.info(request, 'Vote removed!')
    else:
        # Add vote
        PetitionVote.objects.create(petition=petition, user=request.user)
        messages.success(request, 'Vote added!')
    
    return redirect('petition_list')