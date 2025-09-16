from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, CheckoutFeedback
from .forms import CheckoutFeedbackForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

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

# NEW CHECKOUT FEEDBACK VIEWS
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