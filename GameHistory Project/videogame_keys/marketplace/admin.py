from django.contrib import admin
from .models import *

# classi per far in modo che ci sia una visione migliore nella parte admin
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'genre', 'platform')  # Campi visualizzati nella lista
    search_fields = ('title', 'genre', 'platform')  # Campi di ricerca

class ListingAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'quantity', 'price', 'created_at')
    search_fields = ('game__title', 'user__username')
    list_filter = ('created_at', 'user')
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'purchase_date', 'key', 'is_a_offer')
    list_filter = ('purchase_date', 'user')

class OfferAdmin(admin.ModelAdmin):
    list_display = ('id' , 'offer_price', 'accepted', 'created_at', 'listing_id', 'user_id')
    list_filter = ('listing_id', 'user_id')
# Registra i modelli con le classi di amministrazione personalizzate
admin.site.register(Game, GameAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Offer)