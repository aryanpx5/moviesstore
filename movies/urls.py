from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/feedback/submit/', views.submit_feedback, name='submit_feedback'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('petitions/', views.petition_list, name='petition_list'),
    path('petitions/create/', views.create_petition, name='create_petition'),
    path('petitions/<int:petition_id>/vote/', views.vote_petition, name='vote_petition'),
]