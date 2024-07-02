# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid


class Game(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    genre = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    platform = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title

# classe che rappresenta il fulcro del programma, perchè di creare degli annunci
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign Key sullo user
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # Foreign Key sul gioco collegato
    price = models.DecimalField(max_digits=10, decimal_places=2) # campo del prezzo
    quantity = models.PositiveIntegerField(default=1)  # campo della quantità disponibile dell'annuncio
    created_at = models.DateTimeField(auto_now_add=True)  # campo che riguarda la data di pubblicazione)
    is_available = models.BooleanField(default=True)  # campo che riguarda la disponibilità per la visione sulla home principale

    def save(self, *args, **kwargs):  # salvataggio sul dataset
        self.is_available = self.quantity > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.game.title} - {self.price} €"
    
# classe che permette di comprare i diversi annunci presenti sul sito
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Foreign Key sullo user
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)  #  Foreign Key sull'annuncio
    purchase_date = models.DateTimeField(auto_now_add=True) # campo della data
    key = models.CharField(max_length=19, null=True, blank=True)  # campo della chiave
    is_a_offer = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):  # salva sul dataset
        if not self.key:
            # Generate game key if not already set
            self.key = self.generate_game_key()
        super().save(*args, **kwargs)

    def generate_game_key(self): # generatore per la chiave fittizia
        # Example of generating a random game key
        return '-'.join([str(uuid.uuid4().hex)[:4].upper() for _ in range(4)])  # def per la generazione casuale di una chiave in formato XXXX-XXXX-XXXX

    def __str__(self): 
        return f"Acquisto di {self.listing.game.title} da {self.user.username} nel giorno {self.purchase_date}"

# classe che permette di commentare i diversi annunci presenti sul sito
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commento di {self.user.username} sul gioco/annuncio: {self.listing.game.title}"
    
# Classe che permette la di recensire i diversi annunci presenti sul sito
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recensione di {self.user.username} per {self.seller.username} di {self.rating} stelle"

# Classe che permette di effettuare un'offerta ad un'annuncio
class Offer(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='offers')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    accepted = models.BooleanField(null=True, blank=True)  # True: Accepted, False: Rejected, None: Pending
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offerta: {self.offer_price} €, da {self.user.username} per il gioco/annuncio: {self.listing.game.title}"
