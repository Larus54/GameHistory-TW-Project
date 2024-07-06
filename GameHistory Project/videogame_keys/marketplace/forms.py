# marketplace/forms.py
from django import forms
from .models import Game, Listing, Comment, Review, Offer


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['price', 'quantity']

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'release_date', 'genre', 'category', 'platform', 'description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=255)

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['offer_price']

    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing')
        super(OfferForm, self).__init__(*args, **kwargs)