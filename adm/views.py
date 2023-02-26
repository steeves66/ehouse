from django.shortcuts import render, redirect
from admin_volt.forms import LoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm
# from admin_volt.forms import RegistrationForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from .forms import UserRegistrationForm, LoginForm
from django.http import HttpResponse
from user.models import User
from django.contrib import messages, auth
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from catalog.models import TypeLocalite, Localite
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# Library
import django_tables2 as tables
from django_tables2 import Column


class UserRegister(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/sign-up.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST) 
        if form.is_valid(): 
            user_instance = User(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                username = form.cleaned_data['username'],
                phone_number = form.cleaned_data['phone_number'],
                email = form.cleaned_data['email'],
                password = make_password(form.cleaned_data['password'])
                )
            user_instance.request = request
            user_instance.save()
            messages.success(request, 'Your account is created successfully. We have sent you a verification email to verify your email. Follow the instruction in this email.')   
            to_email =form.cleaned_data['email']
            return redirect('/user/login/?command=verification&email='+to_email)
        return render(request, self.template_name, {'form': form})


class UserLogin(View):
    template_name = 'accounts/sign-in.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_name = User.objects.get(username=username)
        except User.DoesNotExist:
            user_name = User.objects.get(email=username)
        user = auth.authenticate(username=user_name, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(reverse('dashboard'))
        messages.error(request, 'Invalid credentials, please check username/email or password.')
        return render(request, self.template_name, {'form': form})


class UserLogout(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are logged out.')
        return redirect(reverse('login'))


class AddLocalite(View):
  template_name = 'pages/dashboard/add-localites.html'
  #form_class = LoginForm
  loalite = Localite()

  def get(self, request, *args, **kwargs):
    typeLocalites = TypeLocalite.objects.all()
    context = {
      'typeLocalites': typeLocalites
    }
    return render(request, self.template_name, context=context)

  def post(self, request):
    localite_nom = request.POST.get('localite')
    type_localite_id = request.POST.get('type-localite')
    try:
      parent_id = request.POST['parent-localite-id']
    except KeyError:
      parent_id = None
    
    type_localite = TypeLocalite.objects.get(id=type_localite_id)
    
    if parent_id is not None:
      parent_localite = Localite.objects.get(id=parent_id)
      parent_string = Localite.objects.get(id=parent_id)
      localite_path = parent_string.concat_parent_fils_string +'/'+ localite_nom
      localite = Localite.objects.create(nom=localite_nom, type_localite=type_localite, concat_parent_fils_string=localite_path, parent=parent_localite)
      # print(localite)
    else:
      localite = Localite.objects.create(nom=localite_nom, type_localite=type_localite, concat_parent_fils_string=localite_nom)
      # print(localite)
    return redirect(reverse('localites'))


class GetLocaliteParent(View):
  def post(self, request, *args, **kwargs):
    model_id = request.POST.get('model')
    models = Localite.objects.filter(type_localite=model_id).values('id', 'nom')
    print(list(models))
    return JsonResponse(list(models), safe=False)


class Localites_old(View):
  template_name = 'pages/dashboard/localites.html'
  def get(self, request, *args, **kargs):
    localites_list = Localite.objects.all()
    paginator = Paginator(localites_list, 10)
    page = request.GET.get('page', 1)

    try:
        localites = paginator.page(page)
    except PageNotAnInteger:
        localites = paginator.page(1)
    except EmptyPage:
        localites = paginator.page(paginator.num_pages)

    context = {
      'localites': localites
    }
    return render(request, self.template_name, context)


class Localites(ListView):
    model = Localite
    template_name = 'pages/dashboard/localites.html' 
    context_object_name = 'localites'
    paginate_by = 10
    queryset = Localite.objects.all()


class EditLocalite(View):
  template_name = 'pages/dashboard/edit-localites.html'

  def get(self, request, pk):
    localite = get_object_or_404(Localite, pk=pk)
    typeLocalites = TypeLocalite.objects.all()
    context = {
      'localite': localite,
      'typeLocalites': typeLocalites
    }
    return render(request, self.template_name, context)

  def post(self, request, pk):
    localite = get_object_or_404(Localite, pk=pk)
    localite_nom = request.POST.get('localite')
    type_localite_id = request.POST.get('type-localite')
    try:
      parent_id = request.POST['parent-localite-id']
    except KeyError:
      parent_id = None
    
    type_localite = TypeLocalite.objects.get(id=type_localite_id)
    
    if parent_id is not None:
      parent_localite = Localite.objects.get(id=parent_id)
      parent_string = Localite.objects.get(id=parent_id)
      localite_path = parent_string.concat_parent_fils_string +'/'+ localite_nom

      localite.nom = localite_nom
      localite.type_localite = type_localite
      localite.concat_parent_fils_string = localite_path
      localite.parent = parent_localite
      localite.save()
      # print(localite)
    else:
      localite.nom = localite_nom
      localite.type_localite = type_localite
      localite.concat_parent_fils_string = localite_nom
      localite.save()
      # print(localite)
    return redirect(reverse('localites'))


class DeleteLocalite(View):
  def post(self, request, pk, *args, **kwargs):
    localite = get_object_or_404(Localite, pk=pk)
    localite.delete()
    return redirect(reverse('localites'))


class SearchTerm(View):
  def get(self, request, query):
      models = Localite.objects.filter(nom__icontains=query).values('id', 'nom')
      return JsonResponse(list(models), safe=False)


class SearchLocalite(ListView):
    model = Localite
    template_name = 'pages/dashboard/localites.html'
    context_object_name = 'localites'
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search = request.POST.get('search', '').strip()

        if search:
            # filtrez les objets en fonction du terme de recherche
            queryset = queryset.filter(nom__icontains=search)

        paginator = Paginator(queryset, self.paginate_by)
        page = request.GET.get('page')

        try:
            localites = paginator.page(page)
        except PageNotAnInteger:
            localites = paginator.page(1)
        except EmptyPage:
            localites = paginator.page(paginator.num_pages)

        context = {
            'localites': localites,
            'search': search
        }

        return render(request, self.template_name, context)











# Index
def index(request):
  #return HttpResponse('ok')
  return render(request, 'pages/index.html')

# Dashboard
def dashboard(request):
  context = {
    'segment': 'dashboard'
  }
  return render(request, 'pages/dashboard/dashboard.html', context)

# Pages
@login_required(login_url="/accounts/login/")
def transaction(request):
  context = {
    'segment': 'transactions'
  }
  return render(request, 'pages/transactions.html', context)

@login_required(login_url="/accounts/login/")
def settings(request):
  context = {
    'segment': 'settings'
  }
  return render(request, 'pages/settings.html', context)

# Tables
@login_required(login_url="/accounts/login/")
def bs_tables(request):
  context = {
    'parent': 'tables',
    'segment': 'bs_tables',
  }
  return render(request, 'pages/tables/bootstrap-tables.html', context)

# Components
@login_required(login_url="/accounts/login/")
def buttons(request):
  context = {
    'parent': 'components',
    'segment': 'buttons',
  }
  return render(request, 'pages/components/buttons.html', context)

@login_required(login_url="/accounts/login/")
def notifications(request):
  context = {
    'parent': 'components',
    'segment': 'notifications',
  }
  return render(request, 'pages/components/notifications.html', context)

@login_required(login_url="/accounts/login/")
def forms(request):
  context = {
    'parent': 'components',
    'segment': 'forms',
  }
  return render(request, 'pages/components/forms.html', context)

@login_required(login_url="/accounts/login/")
def modals(request):
  context = {
    'parent': 'components',
    'segment': 'modals',
  }
  return render(request, 'pages/components/modals.html', context)

@login_required(login_url="/accounts/login/")
def typography(request):
  context = {
    'parent': 'components',
    'segment': 'typography',
  }
  return render(request, 'pages/components/typography.html', context)


# Authentication
def register_view(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      print("Account created successfully!")
      form.save()
      return redirect('/accounts/login/')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()
  
  context = { 'form': form }
  return render(request, 'accounts/sign-up.html', context)




class UserLoginView(LoginView):
  form_class = LoginForm
  template_name = 'accounts/sign-in.html'

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password-change.html'
  form_class = UserPasswordChangeForm

class UserPasswordResetView(PasswordResetView):
  pass
  template_name = 'accounts/forgot-password.html'
  form_class = UserPasswordResetForm

class UserPasswrodResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/reset-password.html'
  form_class = UserSetPasswordForm

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

def lock(request):
  return render(request, 'accounts/lock.html')

# Errors
def error_404(request):
  pass
  return render(request, 'pages/examples/404.html')

def error_500(request):
  return render(request, 'pages/examples/500.html')

# Extra
def upgrade_to_pro(request):
  return render(request, 'pages/upgrade-to-pro.html')