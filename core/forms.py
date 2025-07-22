# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Question, Comment, FoodWasteSurvey, WaterConservationSurvey, CarbonFootprintSurvey, SustainabilityEntry, EnergyQuiz

# Auth form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Post form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']

# Question form
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'user_response']

# Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class FoodWasteSurveyForm(forms.ModelForm):
    COMPOST_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    composts = forms.TypedChoiceField(
        label="Do you compost your food scraps?",
        choices=COMPOST_CHOICES,
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',  # ensure value is cast properly to boolean
        required=False
    )

    class Meta:
        model = FoodWasteSurvey
        exclude = ['user', 'timestamp']
        widgets = {
            'leftovers_discarded': forms.RadioSelect(),
            'expiry_check': forms.RadioSelect(),
            'meal_planning': forms.RadioSelect(),
            'eat_out_before_clearing_fridge': forms.RadioSelect(),
        }
        labels = {
            'leftovers_discarded': "How often do you throw away leftovers?",
            'expiry_check': "Do you check expiry dates before discarding food?",
            'meal_planning': "Do you plan meals to reduce food waste?",
            'eat_out_before_clearing_fridge': "Do you eat out before finishing perishable food at home?",
        }

class WaterConservationSurveyForm(forms.ModelForm):
    TAP_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    turns_off_tap = forms.TypedChoiceField(
        label="Do you turn off the tap while brushing your teeth?",
        choices=TAP_CHOICES,
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
        required=False,
    )

    water_efficient_appliances = forms.TypedChoiceField(
        label="Do you use water-efficient appliances?",
        choices=TAP_CHOICES,
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
        required=False,
    )

    class Meta:
        model = WaterConservationSurvey
        exclude = ['user', 'timestamp']
        widgets = {
            'short_showers': forms.RadioSelect(choices=[('Never', 'Never'), ('Sometimes', 'Sometimes'), ('Often', 'Often'), ('Always', 'Always')]),
            'washing_machine_load': forms.RadioSelect(choices=[('Full Load', 'Full Load'), ('Half Load', 'Half Load'), ('Small Load', 'Small Load')]),
            'rainwater_usage': forms.RadioSelect(choices=[('Never', 'Never'), ('Occasionally', 'Occasionally'), ('Regularly', 'Regularly')]),
        }
        labels = {
            'short_showers': "Do you take short showers (under 5 minutes)?",
            'tap_off_while_brushing': "Do you turn off the tap while brushing your teeth?",
            'washing_machine_load': "How full is your washing machine when you run it?",
            'water_efficient_appliances': "Do you use water-efficient appliances?",
            'rainwater_usage': "How often do you use rainwater for gardening or cleaning?",
        }

class CarbonFootprintSurveyForm(forms.ModelForm):
    class Meta:
        model = CarbonFootprintSurvey
        exclude = ['user', 'timestamp']
        widgets = {
            'transport_mode': forms.RadioSelect,
            'diet_type': forms.RadioSelect,
            'electricity_usage': forms.RadioSelect,
            'shopping_habits': forms.RadioSelect,
        }

class SustainabilityEntryForm(forms.ModelForm):
    actions = forms.MultipleChoiceField(
        choices=SustainabilityEntry.ACTION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = SustainabilityEntry
        fields = ['date', 'actions', 'is_public']
        widgets = {
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea, label='Your Message')

class EnergyQuizForm(forms.ModelForm):
    class Meta:
        model = EnergyQuiz
        fields = [
            'turn_off_lights',
            'efficient_appliances',
            'heating_cooling',
            'unplug_devices',
            'renewable_energy',
        ]
        widgets = {
            'turn_off_lights': forms.RadioSelect(choices=[
                ('always', 'Always'), ('sometimes', 'Sometimes'), ('never', 'Never')
            ]),
            'efficient_appliances': forms.RadioSelect(choices=[
                ('yes', 'Yes'), ('some', 'Some'), ('no', 'No')
            ]),
            'heating_cooling': forms.RadioSelect(choices=[
                ('efficient', 'Efficient'), ('moderate', 'Moderate'), ('inefficient', 'Inefficient')
            ]),
            'unplug_devices': forms.RadioSelect(choices=[
                ('always', 'Always'), ('rarely', 'Rarely'), ('never', 'Never')
            ]),
            'renewable_energy': forms.RadioSelect(choices=[
                ('yes', 'Yes'), ('planning', 'Planning to'), ('no', 'No')
            ]),
        }
