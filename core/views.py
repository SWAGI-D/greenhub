# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Comment, Like, Question
from .forms import PostForm, RegisterForm, QuestionForm, CommentForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import FoodWasteSurveyForm, WaterConservationSurveyForm, CarbonFootprintSurveyForm, SustainabilityEntryForm, ContactForm, EnergyQuizForm
from .models import FoodWasteSurvey, WaterConservationSurvey, SustainabilityEntry, EnergyQuiz
from datetime import date, datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django import forms
from django.contrib.auth.hashers import make_password
from types import SimpleNamespace


class PostListView(ListView):
    model = Post
    template_name = 'core/index.html'
    context_object_name = 'posts'
    ordering = ['-timestamp']

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(caption__icontains=query) | Q(title__icontains=query)
            ).order_by('-timestamp')
        return Post.objects.all().order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['public_entries'] = SustainabilityEntry.objects.filter(is_public=True).order_by('-date')[:6]
        context['query'] = self.request.GET.get('q', '')
        context['visit_data'] = track_user_history(self.request)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comment_form'] = CommentForm()
        context['comments'] = post.comment_set.all()
        context['likes'] = post.like_set.count()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
        return HttpResponseRedirect(reverse('post_detail', args=[post.id]))

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '🎉 Thank you for registering! You can now log in.')
            return redirect('thank_you_register')  # Redirects to a custom thank-you page
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def profile(request):
    posts = Post.objects.filter(user=request.user)
    food_quiz_taken = FoodWasteSurvey.objects.filter(user=request.user).exists()
    water_quiz_taken = WaterConservationSurvey.objects.filter(user=request.user).exists()
    energy_quiz_taken = EnergyQuiz.objects.filter(user=request.user).exists()

    # Get or create profile to safely access carbon footprint score
    profile, created = Profile.objects.get_or_create(user=request.user)
    carbon_score = profile.carbon_footprint_score

    visit_data_dict = track_user_history(request)
    visit_data = SimpleNamespace(**visit_data_dict)

    return render(request, 'core/profile.html', {
        'posts': posts,
        'food_quiz_taken': food_quiz_taken,
        'water_quiz_taken': water_quiz_taken,
        'energy_quiz_taken': energy_quiz_taken,
        'carbon_score': carbon_score,
        'visit_data': visit_data,
    })

@login_required
def upload_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'core/upload_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)  # Only allow deleting own posts
    if request.method == "POST":
        post.delete()
        return redirect('index')
    return render(request, 'core/confirm_delete.html', {'post': post})

@login_required
def sustainability_questions(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = QuestionForm()
    return render(request, 'core/question_form.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()  # unlike
    return redirect('post_detail', pk=post.id)

def search(request):
    query = request.GET.get('q')
    results = Post.objects.filter(Q(caption__icontains=query)) if query else []
    return render(request, 'core/search_results.html', {'results': results, 'query': query})

# core/views.py

@login_required
def food_waste_quiz(request):
    if request.method == 'POST':
        form = FoodWasteSurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.user = request.user
            survey.save()
            return redirect('thank_you')
    else:
        form = FoodWasteSurveyForm()
    return render(request, 'core/food_quiz.html', {'form': form})

@login_required
def water_conservation_quiz(request):
    if request.method == 'POST':
        form = WaterConservationSurveyForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.user = request.user
            quiz.save()
            return redirect('thank_you')
    else:
        form = WaterConservationSurveyForm()
    return render(request, 'core/water_conservation_quiz.html', {'form': form})

@login_required
def energy_quiz(request):
    if request.method == 'POST':
        form = EnergyQuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.user = request.user
            quiz.save()
            return redirect('thank_you')
    else:
        form = EnergyQuizForm()
    return render(request, 'core/energy_quiz.html', {'form': form})


def thank_you(request):
    return render(request, 'core/thank_you.html')

def thank_you_register(request):
    return render(request, 'core/thank_you_register.html')

def blog_food_scraps(request):
    return render(request, 'core/blog_food_scraps.html')

def blog_plastic_pollution(request):
    return render(request, 'core/blog_plastic_pollution.html')

def blog_green_energy(request):
    return render(request, 'core/blog_green_energy.html')

def blog_urban_gardening(request):
    return render(request, 'core/blog_urban_gardening.html')

def blog_5rs_sustainability(request):
    return render(request, 'core/blog_5rs_sustainability.html')


@login_required
def carbon_footprint_quiz(request):
    if request.method == 'POST':
        form = CarbonFootprintSurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.user = request.user
            survey.save()

            # Scoring logic
            score = 0
            if survey.transport_mode == 'Car':
                score += 3
            elif survey.transport_mode == 'Public Transit':
                score += 2
            else:
                score += 1

            if survey.diet_type == 'Meat-heavy':
                score += 3
            elif survey.diet_type == 'Mixed':
                score += 2
            else:
                score += 1

            flight_score_map = {
                'none': 0,
                'rare': 1,
                'occasional': 2,
                'frequent': 3,
            }
            score += flight_score_map.get(survey.flight_frequency, 0)

            shopping_score_map = {
                'rare': 1,
                'occasional': 2,
                'frequent': 3,
            }
            score += shopping_score_map.get(survey.shopping_habits, 0)

            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.carbon_footprint_score = score
            profile.save()

            # Result message
            if score <= 5:
                result = "Low carbon footprint – keep it up!"
            elif score <= 9:
                result = "Moderate – good, but can improve."
            else:
                result = "High carbon footprint – time for some eco-friendly changes!"

            return render(request, 'core/carbon_result.html', {'result': result})
    else:
        form = CarbonFootprintSurveyForm()

    return render(request, 'core/carbon_footprint_survey_form.html', {'form': form})



@login_required
def log_sustainability_entry(request):
    if request.method == 'POST':
        form = SustainabilityEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            print("Saved entry:", entry.date, entry.is_public, entry.actions)
            return redirect('sustainability_diary')
    else:
        form = SustainabilityEntryForm(initial={'date': date.today()})

    return render(request, 'core/log_entry.html', {
        'form': form,
        'today': date.today().isoformat()
    })

@login_required
def sustainability_diary(request):
    entries = SustainabilityEntry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'core/diary.html', {'entries': entries})


def index(request):
    public_entries = SustainabilityEntry.objects.filter(is_public=True).order_by('-date')[:6]  # show latest 6
    visit_data_dict = track_user_history(request)
    visit_data = SimpleNamespace(**visit_data_dict)
    print("PUBLIC ENTRIES:", SustainabilityEntry.objects.filter(is_public=True).values())

    return render(request, 'core/index.html', {
        'public_entries': public_entries,
        'visit_data': visit_data
    })

def public_log_summary(request):
    from django.db.models import Count
    from .models import SustainabilityEntry

    summaries = (
        SustainabilityEntry.objects
        .filter(is_public=True)
        .values('user__username')
        .annotate(total_logs=Count('id'))
        .order_by('-total_logs')
    )

    return render(request, 'core/public_log_summary.html', {
        'summaries': summaries
    })

def browse_public_logs(request):
    public_entries = SustainabilityEntry.objects.filter(is_public=True).order_by('-date')
    return render(request, 'core/browse_logs.html', {'public_entries': public_entries})

def about(request):
    return render(request, 'core/about.html')

def contact_view(request):
    storage = get_messages(request)
    list(storage)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print("Contact Form Submitted:", form.cleaned_data)
            messages.success(request, 'Thanks for reaching out! We’ll get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})

class TreePledgeForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    number_of_trees = forms.IntegerField(min_value=1, label="How many trees will you plant?")

def plant_tree_view(request):
    if request.method == 'POST':
        form = TreePledgeForm(request.POST)
        if form.is_valid():
            # You can save to database or send email here
            messages.success(request, "🌳 Thank you for pledging to plant trees!")
            return redirect('plant_a_tree')
    else:
        form = TreePledgeForm()
    return render(request, 'core/plant_a_tree.html', {'form': form})

def meet_the_team_view(request):
    return render(request, 'core/meet_the_team.html')

def terms_view(request):
    return render(request, 'core/terms.html')

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            return redirect('reset_password', username=user.username)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
    return render(request, 'core/forgot_password.html')

def reset_password(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            pwd1 = form.cleaned_data['new_password']
            pwd2 = form.cleaned_data['confirm_password']
            if pwd1 == pwd2:
                user.password = make_password(pwd1)
                user.save()
                messages.success(request, "Password updated! You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
    else:
        form = PasswordResetForm()
    return render(request, 'core/reset_password.html', {'form': form, 'username': username})


from datetime import datetime, date
from django.shortcuts import render



def track_user_history(request):
    today_str = date.today().isoformat()

    visit_data = request.session.get('visit_data', {
        'total_visits': 0,
        'visits_today': 0,
        'last_visited': '',
        'last_day': today_str,
    })

    visit_data['total_visits'] += 1

    if visit_data['last_day'] == today_str:
        visit_data['visits_today'] += 1
    else:
        visit_data['visits_today'] = 1
        visit_data['last_day'] = today_str

    visit_data['last_visited'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['visit_data'] = visit_data
    return visit_data




