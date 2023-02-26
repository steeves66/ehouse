from django.contrib import admin
from .models import Pays, Localite, TypeLocalite
from django import forms

class PaysAdmin(admin.ModelAdmin):
  list_display = ('nom', 'abrege', 'prefix_telephone')

admin.site.register(Pays, PaysAdmin)


@admin.register(TypeLocalite)
class TypeLocaliteAdmin(admin.ModelAdmin):
  list_display = ('nom', 'niveau', 'pays') 
  ordering = ['niveau']
