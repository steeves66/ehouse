from django.db import models
from user.models import User

# Create your models here.

class Pays(models.Model):
  nom = models.CharField(max_length=250, null=False, blank=False)
  abrege = models.CharField(max_length=5)
  prefix_telephone = models.CharField(max_length=5)
  date_creation = models.DateTimeField(auto_now_add=True)
  date_maj = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 't_pays'
    
  def __str__(self):
    return self.nom




class TypeLocalite(models.Model):
  nom = models.CharField(max_length=250, null=False, blank=False)
  niveau = models.IntegerField()
  pays = models.ForeignKey(Pays, on_delete=models.SET_NULL, null=True)
  date_creation = models.DateTimeField(auto_now_add=True)
  date_maj = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 't_type_localite'
    
  def __str__(self):
    return self.nom



class Localite(models.Model):
  nom = models.CharField(max_length=250, null=False, blank=False)
  parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
  concat_parent_fils_string = models.CharField(max_length=1000, null=True)
  concat_parent_fils_id = models.CharField(max_length=300, null=True)
  type_localite = models.ForeignKey(TypeLocalite, on_delete=models.SET_NULL, null=True)
  est_actif = models.BooleanField(default=True)
  date_creation = models.DateTimeField(auto_now_add=True)
  date_maj = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 't_localite'
    
  def __str__(self):
    return self.concat_parent_fils_string



class Agence(models.Model):
  nom = models.CharField(max_length=190, null=True)
  logo = models.CharField(max_length=190, null=True)
  slogan = models.TextField(null=True)
  date_creation = models.DateTimeField(default='CURRENT_TIMESTAMP', null=True)
  date_mise_a_jour = models.DateTimeField(null=True)
  emails = models.CharField(max_length=1000, null=True)
  telephones = models.CharField(max_length=1000, null=True)
  cellulaires = models.CharField(max_length=1000, null=True)
  reseaux_sociaux = models.CharField(max_length=1000, null=True)
  est_personne = models.BooleanField(default=False)
  date_creation = models.DateTimeField(auto_now_add=True)
  date_maj = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 't_agence'
    
  def __str__(self):
    return f"{self.nom}"



class Representant(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  agence = models.ForeignKey(Agence, on_delete=models.SET_NULL, null=True)
  date_creation = models.DateTimeField(auto_now_add=True)
  date_maj = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 't_representant'
    
  def __str__(self):
    return f"{self.user.first_name} {self.user.last_name}"



class Typemaison(models.Model):
  nom = models.CharField(max_length=150)
  slug = models.SlugField(max_length=150, unique=True)
  description = models.TextField(max_length=500, blank=True)
  image = models.ImageField(upload_to='image/categorie')

  class Meta:
    db_table = 't_type_maison'
    
  def __str__(self):
    return f"{self.nom}"
  


class Typestanding(models.Model):
  nom = models.CharField(max_length=150)
  slug = models.SlugField(max_length=150, unique=True)
  description = models.TextField(max_length=500, blank=True)
  image = models.ImageField(upload_to='image/standing')

  class Meta:
    db_table = 't_type_standing'
    
  def __str__(self):
    return f"{self.nom}"



class Modecommercial(models.Model):
  nom = models.CharField(max_length=8)

  class Meta:
    db_table = 't_mode_commercial'
    
  def __str__(self):
    return f"{self.nom}"



class Maison(models.Model):
  nb_pieces = models.IntegerField()
  superficie = models.FloatField(null=True)
  coordonnees_gps = models.CharField(max_length=15)
  prix = models.FloatField(null=True)
  a_debattre = models.BooleanField(default=True)
  type_maison = models.ForeignKey(Typemaison, on_delete=models.SET_NULL, null=True)
  type_standing = models.ForeignKey(Typestanding, on_delete=models.SET_NULL, null=True)
  agence = models.ForeignKey(Agence, on_delete=models.SET_NULL, null=True)
  est_actif = models.BooleanField(default=True)
  img_principal = models.ImageField(upload_to='catalog/maison/')
  # plan_principal = models.ImageField(upload_to='catalog/maison')
  quartier = models.CharField(max_length=150)
  secteur =  models.CharField(max_length=150, null=True)
  localite = models.ForeignKey(Localite, on_delete=models.SET_NULL, null=True)
  date_creation = models.DateTimeField(auto_now_add=True)
  date_maj = models.DateTimeField(auto_now=True)
  mode_commercial = models.ForeignKey(Modecommercial, on_delete=models.SET_NULL, null=True)

  class Meta:
    db_table = 't_maison'
    
  def __str__(self):
    return f"{self.type_maison.nom} {self.nb_pieces}"



class Maisonimage(models.Model):
  maison = models.ForeignKey(Maison, on_delete=models.CASCADE)
  images = models.ImageField(upload_to='catalog/maison/')

  class Meta:
    db_table = 't_maison_image'
    
  def __str__(self):
    return f"{self.maison.__str__(self)} image"



class Typemaisonpiece(models.Model):
  nom = models.CharField(max_length=50)
  icons = models.ImageField(upload_to='icon/piece_maison/')

  class Meta:
    db_table = 't_type_maison_piece'
    
  def __str__(self):
    return f"{self.maison.__str__(self)} image"



class Maisonpiece(models.Model):
  type_piece = models.ForeignKey(Typemaisonpiece, on_delete=models.SET_NULL, null=True)
  nombre = models.IntegerField(null=True)
  maison = models.ForeignKey(Maison, on_delete=models.CASCADE)

  class Meta:
    db_table = 't_maison_piece'
    
  def __str__(self):
    return f"{self.maison.__str__(self)} image"