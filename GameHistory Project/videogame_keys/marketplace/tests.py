from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Game, Listing, Purchase, Comment, Review, Offer
from decimal import Decimal


# Tutti i test eventuali sui diversi modelli presenti
class EventModelsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_game_creation(self):
        self.game = Game.objects.create(
            title='Test Game',
            release_date='2023-01-01',
            genre='Action',
            category='AAA',
            platform='PC',
            description='A test game description'
        )
        self.assertEqual(str(self.game), 'Test Game')

    def test_listing_creation(self):
        self.game = Game.objects.create(
            title='Test Game',
            release_date='2023-01-01',
            genre='Action',
            category='AAA',
            platform='PC',
            description='A test game description'
        )
        self.listing = Listing.objects.create(
            user=self.user,
            game=self.game,
            price='50',
            quantity=5,
            is_available=1
        )        
        self.assertEqual(str(self.listing), 'Test Game - 50 €')

    def test_listing_availability(self):
        self.game = Game.objects.create(
            title='Test Game',
            release_date='2023-01-01',
            genre='Action',
            category='AAA',
            platform='PC',
            description='A test game description'
        )
        self.listing = Listing.objects.create(
            user=self.user,
            game=self.game,
            price='50',
            quantity=0,
            is_available=1
        )       
        self.listing.save()
        self.assertFalse(self.listing.is_available)

    def test_purchase_creation(self):
        self.game = Game.objects.create(
            title='Test Game',
            release_date='2023-01-01',
            genre='Action',
            category='AAA',
            platform='PC',
            description='A test game description'
        )
        self.listing = Listing.objects.create(
            user=self.user,
            game=self.game,
            price='50',
            quantity=5,
            is_available=1
        )       
        purchase = Purchase.objects.create(user=self.user, listing=self.listing)
        self.assertEqual(purchase.listing, self.listing)
        self.assertEqual(purchase.user, self.user)
        self.assertTrue(purchase.key) 
        self.assertEqual(len(purchase.key.split('-')), 4)

    def test_comment_creation(self):
        self.game = Game.objects.create(
            title='Test Game',
            release_date='2023-01-01',
            genre='Action',
            category='AAA',
            platform='PC',
            description='A test game description'
        )
        self.listing = Listing.objects.create(
            user=self.user,
            game=self.game,
            price='50',
            quantity=5,
            is_available=1
        )        
        comment = Comment.objects.create(
            listing=self.listing,
            user=self.user,
            content='Commento'
        )
        self.assertEqual(comment.listing, self.listing)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(str(comment), f"Commento di {self.user.username} sul gioco/annuncio: {self.listing.game.title}")

    def test_review_creation(self):
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        review = Review.objects.create(
            user=self.user,
            seller=self.other_user,
            rating=5,
            comment='Ottimo venditore!'
        )
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.seller, self.other_user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(str(review), f"Recensione di {self.user.username} per {self.other_user.username} di 5 stelle")

    def test_offer_creation(self):
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.game = Game.objects.create(
            title='Test Game',
            release_date='2023-01-01',
            genre='Action',
            category='AAA',
            platform='PC',
            description='A test game description'
        )
        self.listing = Listing.objects.create(
            user=self.user,
            game=self.game,
            price='50',
            quantity=5,
            is_available=1
        )        
        offer = Offer.objects.create(
            listing=self.listing,
            user=self.other_user,
            offer_price=40
        )
        self.assertEqual(offer.listing, self.listing)
        self.assertEqual(offer.user, self.other_user)
        self.assertEqual(offer.offer_price, 40)
        self.assertEqual(str(offer), f"Offerta: 40 €, da {self.other_user.username} per il gioco/annuncio: {self.listing.game.title}")
    
# Invece in questa sezione proviamo le diverse caratteristiche principali funzionali del programma
class EventViewTest(TestCase):

    # account di prova
    def setUp(self):
        self.client = Client()
        self.game = Game.objects.create(title='Test Game', release_date='2023-12-12',genre='TestGenre', category='TestGame', platform='TestPC', description='TestDesc')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.listing = Listing.objects.create(user=self.user, game_id=self.game.id, price=10, quantity=5, is_available=True)

    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {'username': 'newuser', 'password1': 'testpassword', 'password2': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_create_listing_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('create_listing'), {'title': 'New Listing', 'price': 10, 'quantity': 5})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Listing.objects.filter(game__title='Test Game').exists())

    def test_delete_listing_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_listing', args=[self.listing.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Listing.objects.filter(id=self.listing.id).exists())

    def test_buy_listing_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('buy_listing', args=[self.listing.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Purchase.objects.filter(user=self.user, listing=self.listing).exists())