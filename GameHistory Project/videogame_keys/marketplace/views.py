from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.db.models import Q
from .forms import ListingForm, GameForm, CommentForm, ReviewForm, SearchForm, OfferForm
from django.contrib.auth.models import AnonymousUser  # Importa l'AnonymousUser
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST


def home(request):
    listings = Listing.objects.filter(is_available=True)  # Filtra solo gli annunci disponibili
    context = {
        'listings': listings,
    }

    return render(request, 'marketplace/home.html', context)

@login_required
def add_review(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    seller = listing.user

    # Controlla se l'utente sta cercando di recensire se stesso
    if request.user == seller:
        messages.error(request, "Non puoi fare una recensione a te stesso.")
        return redirect('listing_detail', listing_id=listing.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.seller = seller
            review.save()
            messages.success(request, f"Recensione inviata con successo!")
            return redirect('listing_detail', listing_id=listing.id)
    else:
        form = ReviewForm()

    return render(request, 'marketplace/add_review.html', {
        'listing': listing,
        'form': form,
    })


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    comments = listing.comments.all()
    reviews = Review.objects.filter(seller=listing.user)
    average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']

    if request.user == listing.user:
        is_owner = True
    else:
        is_owner = False

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.listing = listing
                comment.user = request.user
                comment.save()
                return redirect('listing_detail', listing_id=listing.id)
        else:
            return redirect('login')
    else:
        form = CommentForm()


    return render(request, 'marketplace/listing_detail.html', {
        'listing': listing,
        'is_owner': is_owner,
        'comments': comments,
        'form': form,
        'average_rating': average_rating,
        'reviews': reviews,

    })




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Registrazione completata con successo! Benvenuto su GameHistory Project")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'marketplace/registration/signup.html', {'form': form})

@login_required
def create_listing(request):
    if request.method == 'POST':
        listing_form = ListingForm(request.POST)
        game_form = GameForm(request.POST)

        if listing_form.is_valid() and game_form.is_valid():
            game_instance = game_form.save()  # Salva il gioco nel database
            listing_instance = listing_form.save(commit=False)
            if listing_instance.price > 0:
                listing_instance.game = game_instance
                listing_instance.user = request.user  # Associa l'utente corrente
                listing_instance.save()
                messages.success(request, f"Annuncio inserito con successo!")
                return redirect('home')
            else:
                messages.error(request, f"Non è possibile avere un prezzo in negativo!")
    else:
        listing_form = ListingForm()
        game_form = GameForm()


    return render(request, 'marketplace/create_listing.html', {
        'listing_form': listing_form,
        'game_form': game_form,
    })

@login_required
def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GameForm()
    return render(request, 'marketplace/add_game.html', {'form': form})


@login_required
@require_POST
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user == listing.user:
        listing.delete()
        messages.success(request, 'Annuncio eliminato con successo!')
    return redirect('home')

@login_required
@require_POST
def buy_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if listing.quantity > 0:
                purchase = Purchase(user=request.user, listing=listing)
                purchase.save()

                listing.quantity -= 1

                if listing.quantity == 0:
                    listing.is_available = False

                listing.save()

                messages.success(request, 'Acquisto completato con successo!')
                return redirect('home')
            else:
                messages.error(request, 'L\'annuncio è esaurito.')
        else:
            if isinstance(request.user, AnonymousUser):
                return redirect('login') 
            else:
                messages.error(request, 'Devi effettuare il login per poter acquistare.')

    return render(request, 'listing_detail.html', {'listing': listing})


@login_required
def user_purchases(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'marketplace/user_purchases.html', {'purchases': purchases})

@login_required
def user_profile(request):
    user = request.user

    # acquisti dell'utente
    purchases_no_offer = Purchase.objects.filter(user=user, is_a_offer=False)
    purchases_offer = Purchase.objects.filter(user=user, is_a_offer=True)

    # annunci dell'utente ancora online
    active_listings = Listing.objects.filter(user=user, is_available=True)
    inactive_listings = Listing.objects.filter(user=user, is_available=False)
    
    # recensioni dell'utente
    reviews = Review.objects.filter(seller=user)
    average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']

    # logica delle offerte
    accepted_offers_as_buyer = Offer.objects.filter(user=user, accepted=True)
    accepted_offers_as_seller = Offer.objects.filter(listing__user=user, accepted=True)
    offers = Offer.objects.filter(listing__user=user, accepted=None)  # Solo le offerte non ancora accettate o rifiutate

    return render(request, 'marketplace/user_profile.html', {
        'user': user,
        'purchases_no_offer': purchases_no_offer,
        'purchases_offer': purchases_offer,
        'active_listings': active_listings,
        'inactive_listings': inactive_listings,
        'accepted_offers_as_buyer': accepted_offers_as_buyer,
        'accepted_offers_as_seller': accepted_offers_as_seller,
        'offers': offers,
        'average_rating': average_rating,
        'reviews': reviews,
    })

def search_listings(request):
    query = request.GET.get('query')
    listings = Listing.objects.filter(is_available=True)

    if query:
        listings = listings.filter(
            Q(game__title__icontains=query) |
            Q(game__genre__icontains=query)
        )

    return render(request, 'marketplace/search_results.html', {
        'listings': listings,
        'query': query,
    })


# NECESSARIA PER AVERE LA POSSIBILITA' DI AGGIUNGERE UNA NUOVA QUANTITA' AGLI ANNUNCIO DELL'UTENTE REGISTRATO.
@login_required
@require_POST
def add_quantity(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, user=request.user)
    quantity_to_add = int(request.POST['quantity'])

    if quantity_to_add > 0:
        listing.quantity += quantity_to_add
        listing.save()
        messages.success(request, 'Quantità aggiunta con successo!')
    else:
        messages.error(request, 'Quantità non valida.')

    return redirect('user_profile')

# Parte riguardante l'offerta che è possibile fare ad uno annuncio, con il suo manage_offers

@login_required
def create_offer(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = OfferForm(request.POST, listing=listing)
        if form.is_valid():
            offer = form.save(commit=False)
            if offer.offer_price >=0 and offer.offer_price < listing.price:
                offer.listing = listing
                offer.user = request.user
                offer.save()
                messages.success(request, f"Offerta per {offer.listing.game.title} è stata inviata")
                return redirect('listing_detail', listing_id=listing.id)
            elif offer.offer_price <=0:
               messages.error(request, f"Non è possibile mettere un prezzo negativo o uguale a zero! Non intasare il DB!")
            elif offer.offer_price > listing.price:
                messages.error(request, f"Non è possibile mettere un prezzo superiore al prezzo di vendita! Non intasare il DB!")
    else:
        form = OfferForm(listing=listing)
    return render(request, 'marketplace/create_offer.html', {'form': form, 'listing': listing})

@login_required
def manage_offers(request):
    # trovo tutti gli annunci creati dall'utente
    listings_as_seller = Listing.objects.filter(user=request.user)

    # trovo tutte le offerte sugli annunci creati dall'utente
    offers_as_seller = Offer.objects.filter(listing__in=listings_as_seller)

    # trovo tutte le offerte fatte dall'utente
    offers_as_buyer = Offer.objects.filter(user=request.user)
    return render(request, 'marketplace/manage_offers.html', {
        'offers_as_seller': offers_as_seller,
        'offers_as_buyer': offers_as_buyer,
        }
    )

# utilizzato per generare la chiave per l'offerta
def generate_game_key(): # generatore per la chiave fittizia
    return '-'.join([str(uuid.uuid4().hex)[:4].upper() for _ in range(4)])  # def per la generazione casuale di una chiave in formato XXXX-XXXX-XXXX

@login_required
def respond_to_offer(request, offer_id, response):
    offer = Offer.objects.get(id=offer_id)
    listing = offer.listing
    if response == 'accept' and listing.quantity > 0:
        offer.accepted = True
        listing.quantity -= 1
        listing.save()
        game_key = generate_game_key()
        Purchase.objects.create(listing=listing, user=offer.user, key = game_key, is_a_offer=True)
        messages.success(request, f"Accettata l'offerta di {offer.user.username} per {offer.listing.game.title}!")
    elif response == 'accept' and listing.quantity == 0:
        offer.accepted = False
        messages.error(request, f"Non è possibile accettare l'offerta perchè le quantità sono finite, rifiutata automaticamente")
    elif response == 'reject' and listing.quantity > 0:
        offer.accepted = False
        messages.error(request, f"Rifiutata l'offerta di {offer.user.username} per {offer.listing.game.title}")
    elif response == 'reject' and listing.quantity == 0:
        offer.accepted = False
        messages.error(request, f"Non è possibile rifiutare l'offerta perchè le quantità sono finite, rifiutata automaticamente")

    offer.save()
    return redirect('manage_offers')