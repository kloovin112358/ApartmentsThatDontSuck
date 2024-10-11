from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q, Prefetch
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *
from .forms import CustomUserLoginForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.views.generic import RedirectView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Exists, OuterRef
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView
from django.contrib.auth.password_validation import password_validators_help_text_html
from django.utils import timezone
from django.utils.formats import date_format
from django.db.models import Count, Q
from django.contrib.auth.decorators import user_passes_test

# def testAnything(request):
#     # send_mail(
#     #     'Subject here',
#     #     'Here is the message.',
#     #     'from@example.com',
#     #     ['to@example.com'],
#     #     fail_silently=False,
#     # )
#     return render(request, 'verify_email.html')

def is_user_staff(user):
    if user.is_authenticated:
        return user.is_user_account_valid_and_verified_and_staff()

def is_user_verified(user):
    if user.is_authenticated:
        return user.is_user_account_valid_and_verified()

class LogoutView(RedirectView):
    url = reverse_lazy('Ranker:home')  # Redirect to home or any other page after logout
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

def aboutPage(request):
    return render(request, "about.html")

def ApartmentsList(request):
    if request.user.is_authenticated:
        saved_units = SavedUnit.objects.filter(user=request.user, unit=OuterRef('pk'))
        sucks_reports = UnitSucksReport.objects.filter(user=request.user, unit=OuterRef('pk'))
        not_available_reports = UnitNotAvailableReport.objects.filter(user=request.user, unit=OuterRef('pk'))

        units = Unit.objects.filter(
            status="Live"
        ).annotate(
            is_saved=Exists(saved_units),
            is_sucks_reported=Exists(sucks_reports),
            is_not_available_reported=Exists(not_available_reports)
        ).order_by('-is_saved', '-datetime_added', '-is_sucks_reported', '-is_not_available_reported')
    else:
        units = Unit.objects.filter(status="Live").order_by('-datetime_added')
    status_choices = [{'value': c[0], 'label': c[1]} for c in Unit.status.field.choices]

    return render(request, "apartments_list.html", {
        "units": units,
        "unit_statuses": status_choices,
        "categories": Unit.CATEGORY_CHOICES,
        'neighborhoods': Neighborhood.objects.all(),
        'unit_types': UnitType.objects.all()
    })

@user_passes_test(is_user_staff)
@login_required
def ReportsList(request):
    # Filter reports by status 'Open'
    open_not_available_reports = UnitNotAvailableReport.objects.filter(status='Open')
    open_sucks_reports = UnitSucksReport.objects.filter(status='Open')

    units = Unit.objects.filter(
        status="Live"
    ).prefetch_related(
        Prefetch('unitnotavailablereport_set', queryset=open_not_available_reports, to_attr='open_not_available_reports'),
        Prefetch('unitsucksreport_set', queryset=open_sucks_reports, to_attr='open_sucks_reports')
    ).annotate(
        open_sucks_reports_count=Count(
            'unitsucksreport',
            filter=Q(unitsucksreport__status='Open')
        ),
        open_not_available_reports_count=Count(
            'unitnotavailablereport',
            filter=Q(unitnotavailablereport__status='Open')
        ),
    ).filter(
        Q(open_sucks_reports_count__gt=0) | Q(open_not_available_reports_count__gt=0)    
    ).order_by('id')

    context = {
        'units': units,
    }
    return render(request, "reports_list.html", context)

@user_passes_test(is_user_staff)
@login_required
def apartmentSearches(request):
    unitTypes = UnitType.objects.annotate(
        live_search_count=Count('searches', filter=Q(searches__live_search=True))
    )
    
    # Prefetch related searches that have live_search=True
    unitTypes = unitTypes.prefetch_related(
        Prefetch(
            'searches', 
            queryset=Search.objects.filter(live_search=True),
            to_attr='live_searches'
        )
    )
    neighborhoods = Neighborhood.objects.filter().order_by('name')
    categories = Unit.CATEGORY_CHOICES
    return render(request, "searches.html", {"unitTypes": unitTypes, "neighborhoods": neighborhoods, "categories": categories})

def send_verification_email(requestedUser):
    verifEmailInst, created = EmailVerification.objects.get_or_create(account=requestedUser)
    html_message = render_to_string('verification_email.html', {
        'emailVerificationInst': verifEmailInst,
        'protocol': settings.DEFAULT_PROTOCOL,
        'domain': settings.DEFAULT_DOMAIN,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        "Verify your email for Apartments That Don't Suck",
        plain_message,
        'host@atds.com',
        [requestedUser.email],
        html_message=html_message
    )

@login_required
def EmailVerificationRequired(request):
    if request.user.verified_account:
        messages.info(request, "email is already verified.")
        return redirect('Ranker:my_account')
    
    emailSent = False
    if request.GET.get('prefillSend', None) == 'true':
        send_verification_email(request.user)
        emailSent = True
    
    if request.method == "POST":
        send_verification_email(request.user)
        userAccount = request.user
        userAccount.verified_account = True
        userAccount.save()
        emailSent = True
    
    if request.GET.get('emailSent', None) == 'true':
        emailSent = True

    return render(request, "email_verification_required.html", {'sent_email': emailSent})

@login_required
def verifyEmail(request, id):
    emailVerifInst = get_object_or_404(EmailVerification, id=id)
    if request.method == "POST":
        if not emailVerifInst.verified_datetime:
            emailVerifInst.verified_datetime = timezone.now()
            emailVerifInst.save()
            messages.success(request, "account verified.")
        else:
            messages.info(request, "Note: your account is already verified.")
        return redirect(reverse('Ranker:my_account'))

    else:
        accountInst = emailVerifInst.account
        if accountInst.verified_account and emailVerifInst.verified_datetime:
            messages.info(request, "email is already verified.")
            return redirect(reverse('Ranker:my_account'))
        return render(request, "verify_email.html")

@user_passes_test(is_user_staff)
@login_required
def valueMatrix(request):
    return render(request, "value_matrix.html", {
        'unit_types': UnitType.objects.all(),
        'quality_ratings': QualityRating.objects.all(),
        'quality_values': QualityValue.objects.all(),
        'min_maxes': QualityValuePriceMinMax.objects.all()
    })

class CustomUserLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomUserLoginForm

class MyAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'my_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        # Subquery to check if a UnitSucksReport exists for each unit
        sucks_report_exists = UnitSucksReport.objects.filter(
            user=self.request.user,
            unit=OuterRef('unit'),
        )

        # Subquery to check if a UnitNotAvailableReport exists for each unit
        not_available_report_exists = UnitNotAvailableReport.objects.filter(
            user=self.request.user,
            unit=OuterRef('unit'),
        )

        # Annotate the SavedUnit queryset
        saved_units = SavedUnit.objects.filter(user=self.request.user, unit__status="Live").annotate(
            has_sucks_report=Exists(sucks_report_exists),
            has_not_available_report=Exists(not_available_report_exists)
        )

        context['savedUnits'] = saved_units

        return context

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('Ranker:email_verification_required')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            user = form.save()
            # Log the user in after signing up
            login(self.request, user)
            return response
        
        except IntegrityError as e:
            form.add_error(None, 'An unexpected error occurred.')
            # Re-render the form with the error
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Add a custom message or log the error here if needed
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_help_text'] = password_validators_help_text_html()
        return context

class AccountDeletedView(TemplateView):
    template_name = 'account_deleted.html'

class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('Ranker:account_deleted')  # Redirect after successful deletion
    template_name = 'delete_account.html'

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        # Call the superclass's post method to handle the deletion
        response = super().post(request, *args, **kwargs)
        
        # Log out the user after deletion
        logout(request)
        
        # Redirect to a confirmation page or home page
        return redirect(self.success_url)

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'password_reset_email.html'
    success_url=reverse_lazy('Ranker:password_reset_done')
    template_name='password_reset_form.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name='password_reset_confirm.html'
    success_url=reverse_lazy('Ranker:password_reset_complete')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_help_text'] = password_validators_help_text_html()
        return context
    
def ajax_get_units(request):
    # Extract the query parameters from the request
    unit_types = request.GET.get('unit_types')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    locations = request.GET.get('locations')
    location_type = request.GET.get('location_type')

    # Parse the JSON strings back to Python objects (lists)
    if unit_types:
        try:
            unit_types = json.loads(unit_types)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid unit_types parameter'}, status=400)

    if locations:
        try:
            locations = json.loads(locations)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid locations parameter'}, status=400)

    # Handle the case where min_price or max_price is missing
    if min_price is not None:
        try:
            min_price = float(min_price)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid min_price parameter'}, status=400)

    if max_price is not None:
        try:
            max_price = float(max_price)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid max_price parameter'}, status=400)

    # Now you have all your parameters parsed, you can use them to query your database
    # Example (dummy response):
    units = []  # Replace this with the actual logic to get units

    # Respond with the data
    return JsonResponse({
        'success': True,
        'units': units,
        'unit_types': unit_types,
        'min_price': min_price,
        'max_price': max_price,
        'locations': locations,
        'location_type': location_type,
    })

@user_passes_test(is_user_staff)
@login_required
@require_POST
def ajax_add_unit(request):
    # Extract form data
    unit_type_id = request.POST.get('unit-type')
    # category = request.POST.get('category')
    neighborhood_id = request.POST.get('neighborhood')
    price = request.POST.get('price')
    # quality_rating = request.POST.get('quality-rating')
    link = request.POST.get('link')

    # Validate data and create model instance
    try:
        unit_type = UnitType.objects.get(id=unit_type_id)
        neighborhood = Neighborhood.objects.get(id=neighborhood_id)
        
        unit = Unit(
            status='Live',  # Set default or calculate status as needed
            datetime_added=timezone.now(),
            neighborhood=neighborhood,
            unitType=unit_type,
            listing_link=link,
            price=price,
            # category=category,
            # quality_rating=quality_rating
        )
        unit.save()

        return JsonResponse({'success': True})

    except Exception as e:
        # Handle exceptions and return error response
        return JsonResponse({'success': False, 'error': str(e)})

@user_passes_test(is_user_verified)
@login_required
@require_POST
def ajax_save_unit(request):
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            unit_id = data.get('unit_id')

            if unit_id is not None:
                unit = Unit.objects.get(pk=unit_id)
                saved_unit, created = SavedUnit.objects.get_or_create(user=request.user, unit=unit)
                
                if created:
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'message': 'Unit already saved.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid unit ID.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'})
    else:
        return JsonResponse({'success': False, 'message': 'User not authenticated.'})

@user_passes_test(is_user_verified)
@login_required
@require_POST
def ajax_remove_save(request):
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            unit_id = data.get('unit_id')
            
            if unit_id is not None:
                unit = Unit.objects.get(pk=unit_id)
                saved_unit = SavedUnit.objects.filter(user=request.user, unit=unit).first()
                
                if saved_unit:
                    saved_unit.delete()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'message': 'Unit not found in saved units.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid unit ID.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'})
    else:
        return JsonResponse({'success': False, 'message': 'User not authenticated.'})

@user_passes_test(is_user_verified)
@login_required
@require_POST
def ajax_sucks_unit(request):
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            unit_id = data.get('unit_id')
            description = data.get('description')
            
            if unit_id and description:
                unit = Unit.objects.get(pk=unit_id)
                if not UnitSucksReport.objects.filter(user=request.user, unit=unit).exists():
                    UnitSucksReport.objects.create(
                        user=request.user, 
                        unit=unit, 
                        description=description,
                        datetime_submitted=timezone.now()
                    )
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'message': 'You have already reported this unit.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid data.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'})
    else:
        return JsonResponse({'success': False, 'message': 'User not authenticated.'})

@user_passes_test(is_user_verified)
@login_required
@require_POST
def ajax_not_available_unit(request):
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            unit_id = data.get('unit_id')
            
            if unit_id:
                unit = Unit.objects.get(pk=unit_id)
                if not UnitNotAvailableReport.objects.filter(user=request.user, unit=unit).exists():
                    UnitNotAvailableReport.objects.create(
                        user=request.user, 
                        unit=unit, 
                        datetime_submitted=timezone.now()
                    )
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'message': 'You have already reported this unit.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid data.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'})
    else:
        return JsonResponse({'success': False, 'message': 'User not authenticated.'})

@require_POST
def ajax_contact_form(request):
    email = request.POST.get('email')
    message = request.POST.get('message')

    if not email or not message:
        return JsonResponse({'success': False, 'message': 'Email and message are required.'})

    # Save the message to the database
    ContactFormMessage.objects.create(email=email, message=message)

    # Send the email
    send_mail(
        subject="New Contact Form Message",
        message=message,
        from_email='host@atds.com',
        recipient_list=[email],  # You can change this to the email where you want to receive messages
        fail_silently=False,
    )

    return JsonResponse({'success': True})

@user_passes_test(is_user_staff)
@login_required
@require_POST
def ajax_update_stop_at(request):
    data = json.loads(request.body)
    search_id = data.get('search_id')
    last_item_note = data.get('last_item_note')

    try:
        search = Search.objects.get(id=search_id)
        search.last_item_note = last_item_note
        search.last_updated = timezone.now()
        search.save()

        formatted_last_updated = date_format(
            timezone.localtime(search.last_updated),
            format='N j, Y, g:i a',
            use_l10n=True
        )

        return JsonResponse({'success': True, 'last_updated': formatted_last_updated})
    except Search.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Search not found.'})

@user_passes_test(is_user_staff)
@login_required
@require_POST
def update_report_status(request):
    report_id = request.POST.get('report_id')
    action = request.POST.get('action')
    report_type = request.POST.get('report_type')

    # Validate input
    if not report_id or action not in ['dismiss', 'accept'] or not report_type:
        return JsonResponse({'success': False, 'error': 'Invalid data.'})

    # Update the report status
    if report_type == "sucks":
        report = get_object_or_404(UnitSucksReport, id=report_id)
    elif report_type == "not_available":
        report = get_object_or_404(UnitNotAvailableReport, id=report_id)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid data.'})

    if action == 'dismiss':
        report.status = 'Dismissed'
    elif action == 'accept':
        report.status = 'Actioned'
        if isinstance(report, UnitSucksReport):
            unit = report.unit
            unit.status = 'Sucks'
        elif isinstance(report, UnitNotAvailableReport):
            unit = report.unit
            unit.status = 'Sold'
        unit.save()
        
    report.save()
    
    return JsonResponse({'success': True})

@user_passes_test(is_user_staff)
@login_required
@csrf_exempt
def ajax_update_value_matrix(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for item in data:
            quality_value_id = item.get('quality_value_id')
            quality_rating_id = item['quality_rating_id']
            min_max_id = item['min_max_id']
            unit_type_id = item['unit_type_id']
            value_rating = item['value_rating']

            if quality_value_id:
                # Update existing record
                quality_value = QualityValue.objects.get(id=quality_value_id)
                if quality_value.value_rating != value_rating:
                    quality_value.value_rating = value_rating
                    quality_value.save()
            else:
                # Create a new record
                QualityValue.objects.create(
                    unit_type_id=unit_type_id,
                    quality_rating_id=quality_rating_id,
                    min_max_id=min_max_id,
                    value_rating=value_rating
                )

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@user_passes_test(is_user_staff)
@login_required
@csrf_exempt
def ajax_update_unit(request):
    if request.method == 'POST':
        unit_id = request.POST.get('unitId')
        unit = get_object_or_404(Unit, id=unit_id)
        preSaveUnitStatus = unit.status
        # Update the Unit instance with the form data
        form = UnitUpdateForm(request.POST, instance=unit)
        if form.is_valid():
            # Save the form but don't commit to the database yet
            updated_unit = form.save(commit=False)

            # Check if the status is changing from 'Live' to 'Sold'
            if preSaveUnitStatus == 'Live' and updated_unit.status == 'Sold':
                updated_unit.datetime_removed = timezone.now()

            # Save the updated instance
            updated_unit.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@user_passes_test(is_user_staff)
@login_required
@csrf_exempt
def ajax_delete_unit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            unit_id = data.get('unit_id')
            unit = get_object_or_404(Unit, id=unit_id)
            unit.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@user_passes_test(is_user_staff)
@login_required
@csrf_exempt
def ajax_get_unit_details(request, unit_id):
    if request.method == 'GET':
        try:
            unit = Unit.objects.get(id=unit_id)
            return JsonResponse({
                'success': True,
                'unitId': unit_id,
                'status': unit.status,
                'neighborhood_id': unit.neighborhood.id,
                "unitType_id": unit.unitType.id,
                "listingLink": unit.listing_link,
                "price": unit.price,
                "category": unit.category,
                "qualityRating": unit.quality_rating,
                "note": unit.note
            })
        except Unit.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Unit not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


@user_passes_test(is_user_verified)
@require_POST
@login_required
@csrf_exempt
def ajax_save_note(request):
    try:
        # Parse JSON body
        data = json.loads(request.body)
        note = data.get('note', '').strip()
        saved_unit_id = data.get('saved_unit_id')  # Extract unit_id from the body

        # Fetch the Unit object
        savedUnitInst = SavedUnit.objects.get(pk=saved_unit_id, user=request.user)
        savedUnitInst.notes = note
        savedUnitInst.save()

        return JsonResponse({'success': True})
    except Unit.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Unit not found'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})