from django.urls import path
# from admin_volt import views
from adm import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Index
    path('', views.index, name="index"),

    # Authentication
    path('accounts/register/', views.UserRegister.as_view(), name="register"),
    path('accounts/login/', views.UserLogin.as_view(), name="login"),
    path('accounts/logout/', views.UserLogout.as_view(), name="logout"),
    path('dashboard/localites/', views.Localites.as_view(), name="localites"),
    # path('dashboard/localites_for_tables2/', views.LocaliteListView.as_view(), name="localitesTables2"),
    path('dashboard/localites/add/', views.AddLocalite.as_view(), name="add_localite"),
    path('dashboard/localites/edit/<pk>/', views.EditLocalite.as_view(), name="edit_localite"),
    
    path('dashboard/localites/search/<query>/', views.SearchTerm.as_view(), name="searchTerm"),
    path('dashboard/localites/search/', views.SearchLocalite.as_view(), name="search_localite"),

    path('dashboard/localites/delete/<pk>/', views.DeleteLocalite.as_view(), name="delete_localite"),
    path('dashboard/localites/get-localite-parent/', views.GetLocaliteParent.as_view(), name="get_localite_parent"),






    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password-change-done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
    path('accounts/password-reset-confirm/<uidb64>/<token>/',
        views.UserPasswrodResetConfirmView.as_view(), name="password_reset_confirm"
    ),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password-reset-done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password-reset-complete.html'
    ), name='password_reset_complete'),
    path('accounts/lock/', views.lock, name="lock"),

    # Pages
    path('pages/dashboard/', views.dashboard, name="dashboard"),
    path('pages/transaction/', views.transaction, name="transaction"),
    path('pages/settings/', views.settings, name="settings"),

    # Tables
    path('tables/bs-tables/', views.bs_tables, name="bs_tables"),

    # Components
    path('components/buttons/', views.buttons, name="buttons"),
    path('components/notifications/', views.notifications, name="notifications"),
    path('components/forms/', views.forms, name="forms"),
    path('components/modals/', views.modals, name="modals"),
    path('components/typography/', views.typography, name="typography"),

    # Errors
   path('error/404/', views.error_404, name="error_404"),
   path('error/500/', views.error_500, name="error_500"),

    # Extra
   path('pages/upgrade-to-pro/', views.upgrade_to_pro, name="upgrade_to_pro"),
]
