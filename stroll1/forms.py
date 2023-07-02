from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Rating, Destination_Order, Order, Feedback


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ratingForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs = {'class': 'materialize-textarea'}), required=False)
    # rating = forms.ChoiceField(widget=forms.Select(), required=True)
    class Meta:
        model = Rating
        fields = [ 'description', 'rating']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Destination_Order
        fields = ['mobile','payment_method']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method', 'payment_completed']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']
