from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *

app_name = "Ranker"

sitemaps = {
    'static': StaticViewSitemap(),
    'about': AboutPageSitemap(),
    'home': HomePageSitemap()
}


urlpatterns = [
    # public pages
    path("", ApartmentsList, name="home"),
    path("about/", aboutPage, name="about_page"),

    # admin pages
    path("maintenance/reports/", ReportsList, name="reports"),
    path("maintenance/searches/", apartmentSearches, name="searches"),
    path("maintenance/value_matrix/", valueMatrix, name="value_matrix"),

    # login/logout/signup
    path("login/", CustomUserLoginView.as_view(), name="login_page"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("signup/", SignUpView.as_view(), name='sign_up'),

    path("account/", MyAccountView.as_view(), name="my_account"),

    # delete account
    path('account/delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    path('account/account_deleted/', AccountDeletedView.as_view(), name='account_deleted'),

    # email verification
    path("account/email_verification_required/", EmailVerificationRequired, name="email_verification_required"),
    path("account/verify_email/<uuid:id>/", verifyEmail, name="click_email_verify_link"),

    #AJAX
    #general user URLs
    path('ajax/save_unit_to_account/', ajax_save_unit, name='ajax_save_unit'),
    path('ajax/remove_save_unit_from_account/', ajax_remove_save, name='ajax_remove_save'),
    path('ajax/not_available_unit/', ajax_not_available_unit, name='ajax_not_available_unit'),
    path('ajax/sucks_unit/', ajax_sucks_unit, name='ajax_sucks_unit'),
    path('ajax/contact_form/', ajax_contact_form, name='ajax_contact_form'),
    path('ajax/save_note/', ajax_save_note, name="ajax_save_note"),

    #staff URLs
    path('ajax/add_unit/', ajax_add_unit, name='ajax_add_unit'),
    path('ajax/update_stop_at/', ajax_update_stop_at, name='ajax_update_stop_at'),
    path('ajax/update_report_status/', update_report_status, name='update_report_status'),
    path('ajax/update_value_matrix/', ajax_update_value_matrix, name='ajax_update_value_matrix'),
    path('ajax/update_unit/', ajax_update_unit, name='ajax_update_unit'),
    path('ajax/delete_unit/', ajax_delete_unit, name="ajax_delete_unit"),
    path('ajax/get_unit_details/<int:unit_id>/', ajax_get_unit_details, name='ajax_get_unit_details'),

    # Password reset URLs
    path('account/password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('account/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
