# core/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('upload/', views.upload_post, name='upload_post'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('questionnaire/', views.sustainability_questions, name='sustainability_questions'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('search/', views.search, name='search'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('thank-you-register/', views.thank_you_register, name='thank_you_register'),
    path('food-quiz/', views.food_waste_quiz, name='food_waste_quiz'),
    path('water-quiz/', views.water_conservation_quiz, name='water_conservation_quiz'),
    path('blogs/food-scraps/', views.blog_food_scraps, name='blog_food_scraps'),
    path('blog/plastic-pollution/', views.blog_plastic_pollution, name='blog_plastic_pollution'),
    path('carbon-footprint-quiz/', views.carbon_footprint_quiz, name='carbon_footprint_quiz'),
    path('blog-green-energy/', views.blog_green_energy, name='blog_green_energy'),
    path('blog/urban-gardening/', views.blog_urban_gardening, name='blog_urban_gardening'),
    path('blog/5rs-sustainability/', views.blog_5rs_sustainability, name='blog_5rs_sustainability'),
    path('diary/', views.sustainability_diary, name='sustainability_diary'),
    path('log/', views.log_sustainability_entry, name='log_sustainability_entry'),
    path('log-summary/', views.public_log_summary, name='public_log_summary'),
    path('browse-logs/', views.browse_public_logs, name='browse_public_logs'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('plant-a-tree/', views.plant_tree_view, name='plant_a_tree'),
    path('team/', views.meet_the_team_view, name='meet_the_team'),
    path('terms/', views.terms_view, name='terms'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:username>/', views.reset_password, name='reset_password'),
    path('energy-quiz/', views.energy_quiz, name='energy_quiz'),


]
