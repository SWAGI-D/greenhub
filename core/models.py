# core/models.py

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/')
    caption = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')  # Prevent double likes

    def __str__(self):
        return f"{self.user.username} liked post {self.post.id}"

class Question(models.Model):
    text = models.TextField()
    OPTIONS = [
        ('Bad', 'Bad'),
        ('Moderate', 'Moderate'),
        ('Good', 'Good'),
        ('Excellent', 'Excellent'),
    ]
    user_response = models.CharField(max_length=10, choices=OPTIONS, null=True, blank=True)

    def __str__(self):
        return self.text

class EnergyQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    turn_off_lights = models.CharField(max_length=20)
    efficient_appliances = models.CharField(max_length=20)
    heating_cooling = models.CharField(max_length=20)
    unplug_devices = models.CharField(max_length=20)
    renewable_energy = models.CharField(max_length=20)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Energy Quiz"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carbon_footprint_score = models.FloatField(null=True, blank=True)  # or CharField if text

    def __str__(self):
        return f"{self.user.username}'s Profile"

class WaterConservationSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    short_showers = models.CharField(max_length=20)
    turns_off_tap = models.BooleanField(null=True, blank=True)
    washing_machine_load = models.CharField(max_length=20)
    water_efficient_appliances = models.BooleanField()
    rainwater_usage = models.CharField(max_length=20)

# core/models.py

class FoodWasteSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    leftovers_discarded = models.CharField(max_length=20, choices=[
        ('Never', 'Never'),
        ('Rarely', 'Rarely'),
        ('Often', 'Often'),
        ('Always', 'Always'),
    ])

    composts = models.BooleanField()

    expiry_check = models.CharField(max_length=20, choices=[
        ('Always', 'Always'),
        ('Sometimes', 'Sometimes'),
        ('Never', 'Never'),
    ])

    meal_planning = models.CharField(max_length=20, choices=[
        ('Every Week', 'Every Week'),
        ('Sometimes', 'Sometimes'),
        ('Never', 'Never'),
    ])

    eat_out_before_clearing_fridge = models.CharField(max_length=20, choices=[
        ('Always', 'Always'),
        ('Sometimes', 'Sometimes'),
        ('Rarely', 'Rarely'),
        ('Never', 'Never'),
    ])

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Food Waste Survey"

class CarbonFootprintSurvey(models.Model):
    TRANSPORT_CHOICES = [
        ('car', 'Car'),
        ('transit', 'Public Transit'),
        ('bike_walk', 'Walk/Bike'),
    ]

    DIET_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('mixed', 'Mixed'),
        ('meat_heavy', 'Meat-heavy'),
    ]

    ELECTRICITY_USAGE_CHOICES = [
        ('low', 'Low (<200 kWh/month)'),
        ('medium', 'Medium (200-500 kWh/month)'),
        ('high', 'High (>500 kWh/month)'),
    ]

    FLIGHT_CHOICES = [
        ('none', 'None'),
        ('few', '1-3 per year'),
        ('frequent', '4+ per year'),
    ]

    SHOPPING_CHOICES = [
        ('rare', 'Rare'),
        ('occasional', 'Occasional'),
        ('frequent', 'Frequent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transport_mode = models.CharField(max_length=20, choices=TRANSPORT_CHOICES)
    diet_type = models.CharField(max_length=20, choices=DIET_CHOICES)
    electricity_usage = models.CharField(max_length=20, choices=ELECTRICITY_USAGE_CHOICES)
    flight_frequency = models.CharField(max_length=20, choices=FLIGHT_CHOICES)
    shopping_habits = models.CharField(max_length=20, choices=SHOPPING_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carbon Survey - {self.user.username} @ {self.timestamp.strftime('%Y-%m-%d')}"


class SustainabilityEntry(models.Model):
    ACTION_CHOICES = [
        ('composted', 'Composted'),
        ('public_transit', 'Used Public Transit'),
        ('recycled', 'Recycled'),
        ('bike', 'Biked to Work'),
        ('meatless', 'Had Meatless Meal'),
        ('reusable_bags', 'Used Reusable Bags'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    actions = models.JSONField()  # Store list of selected actions
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
