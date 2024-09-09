# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Row, Column
from crispy_forms.bootstrap import Modal, PrependedText
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm

# class CustomUserLoginForm(forms.Form):
#     email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#     def clean(self):
#         email = self.cleaned_data.get('email')
#         password = self.cleaned_data.get('password')
#         if email and password:
#             self.user_cache = authenticate(email=email, password=password)
#             if self.user_cache is None:
#                 raise forms.ValidationError('Invalid email or password.')
#             elif not self.user_cache.is_active:
#                 raise forms.ValidationError('This account is inactive.')
#         return self.cleaned_data

#     def get_user(self):
#         return self.user_cache

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password1', 'password2']

class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        active_users = CustomUser.objects.filter(
            email__iexact=email,
            is_active=True,
        )
        return active_users

class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class UnitUpdateForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['status', 'neighborhood', 'unitType', 'listing_link', 'price', 'quality_rating', 'note']

# class SiteHelpFeedbackForm(forms.ModelForm):
#     class Meta:
#         model = SiteHelpFeedback
#         fields = ['user_email', 'help_type', 'help_message']
#         widgets = {
#             'help_type': forms.Select(attrs={'class': 'form-control'}),
#             'help_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'user_email': forms.EmailInput(attrs={'class': 'form-control'}),
#         }
#         labels = {
#             'user_email': 'Email'
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(SiteHelpFeedbackForm, self).__init__(*args, **kwargs)
        
#         if user and user.is_authenticated:
#             self.fields.pop('user_email')
#         else:
#             self.fields['user_email'].required = True

#         self.fields['help_type'].required = True
#         self.fields['help_message'].required = True

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

# class TicketListingForm(forms.ModelForm):
#     class Meta:
#         model = TicketListing
#         fields = '__all__'  # Or specify the fields you want to include in the form
#         widgets = {
#             'event_datetime': forms.TextInput(attrs={'type': 'datetime-local'}),
#             'tickets_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),    
#         }
#         labels = {
#             'original_qty_tickets_available': 'Ticket quantity'
#         }

#     confirm_resale = forms.BooleanField(
#         required=False, 
#         label="I confirm that these tickets can be resold*"
#     )
#     original_purchase_location_other = forms.CharField(
#         required=False, 
#         label="Please specify the Ticket Vendor*"
#     )
#     general_admission = forms.BooleanField(
#         required=False, 
#         label="Are the ticket(s) General Admission (no assigned seats)?"
#     )
#     standing_room_only = forms.BooleanField(
#         required=False, 
#         label="Are the ticket(s) standing-room only?",
#     )
#     physical_or_digital = forms.BooleanField(
#         required=False, 
#         label="Are the ticket(s) digital? (that is, they are NOT physical, paper tickets)",
#         initial=True
#     )
#     region_name = forms.ChoiceField(
#         required=True, 
#         label="Event region",
#         widget=forms.Select(attrs={
#             'class': 'form-control form-control-sm'
#         }),
#         help_text='In what region is the event? <span class="tooltip-text text-primary text-decoration-underline" data-bs-toggle="tooltip" title="TicketBites is only active in select cities. If your event is not in one of the listed regions, unfortunately you will not be able to sell your tickets on this site.">(What if my event region is not shown here?)</span>'
#     )
#     max_price = forms.DecimalField(
#         required=True,
#         label="Starting (maximum) ticket price",
#         help_text="What is the price you would like a SINGLE TICKET to start at?",
#         max_digits=5,
#         decimal_places=2,
#         min_value=0.01,
#         max_value=100.00,
#         widget=forms.NumberInput(attrs={
#             'step': '0.01',
#             'min': '0.01',
#             'max': '100.00',
#         }),
#         validators=[
#             MinValueValidator(0.01),
#             MaxValueValidator(100.00)
#         ],
#     )
#     min_price = forms.DecimalField(
#         required=True,
#         label="Ending (minimum) ticket price",
#         help_text="What is the SINGLE TICKET price you would like to move towards as time goes on?",
#         max_digits=5,
#         decimal_places=2,
#         min_value=0.01,
#         max_value=100.00,
#         widget=forms.NumberInput(attrs={
#             'step': '0.01',
#             'min': '0.01',
#             'max': '100.00',
#         }),
#         validators=[
#             MinValueValidator(0.01),
#             MaxValueValidator(100.00)
#         ],
#     )
#     images = MultipleFileField(label='Ticket images', required=False, help_text="Provide peace of mind for potential buyers with proof that you own the tickets. Also, your assigned seat listing may sell better if you provide an image of where your ticket(s) fall on the seat map.")

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         original_purchase_location_choices = list(self.fields['original_purchase_location'].choices)
#         original_purchase_location_choices.append(('Other', 'Other'))
#         self.fields['original_purchase_location'].choices = original_purchase_location_choices
#         self.fields['region_name'].choices = [(region.id, region.region_name) for region in EventRegion.objects.all()]
#         venue_choices = list(self.fields['venue'].choices)
#         venue_choices.append(('Other', 'Other'))
#         self.fields['venue'].choices = venue_choices
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.layout = Layout(
#             HTML('''
#                  <h2>Sell Tickets on TicketBites</h2>
#                  <div class="mb-3 mt-4">
#                  <i>Note: in order to list tickets, you MUST VERIFY that your tickets are transferrable. 
#                  Selling a ticket and failing to transfer it to the buyer will result in the following actions: 
#                  first offense = 30-day ban, second offense = 6-month ban, third offense = permanent ban.
#                  </i></div><hr><h3 class="mb-3">Event Information</h3>
#             '''),
#             Field('region_name'),
#             Field('physical_or_digital'),
#             Field('original_purchase_location', css_class='original-purchase-location'),
#             Row(
#                 Column('original_purchase_location_other', css_class='original-purchase-location-other'),
#                 css_class="hiddenPurchaseLocationDetails d-none"
#             ),
#             Row(
#                 Column('confirm_resale', css_class='confirm-resale'),
#                 css_class="confirmResale d-none"
#             ),
#             Row(
#                 Column('event_name'),
#                 Column('venue', css_class='venue-field')
#             ),
#             Field('event_datetime'),
#             HTML("<h3 class='mb-3 mt-4'>Ticket Information</h3>"),
#             Field('images'),
#             Field('tickets_description', placeholder="Anything you want the buyer to know about your tickets."),
#             Row(
#                 Column('original_qty_tickets_available'),
#                 Column('age_restriction'),
#             ),
#             Field('general_admission'),
#             Field('standing_room_only'),
#             HTML('''
#                  <h3 class='mb-3 mt-4'>Pricing Information</h3>
#                  <div class="mb-3">
#                     TicketBites uses Smart Pricing, which is designed to help you sell your tickets before the event date.
#                     This works by continually dropping the price of your tickets as the event date approaches.
#                     Below, you are able to set the maximum ticket price (at which the listing will start), and the minimum price (which
#                     the listing will approach as time goes on). For the best chance of a sale, enter $1 as the minimum price. If you do
#                     not want the price to drop at all, set the minimum price to the same amount as the maximum price.
#                  </div>
#             '''),
#             Row(
#                 Column(PrependedText('max_price', '$')),
#                 Column(PrependedText('min_price', '$')),
#             ),
#             HTML('''
#                 <div id="TicketGrid" class="d-flex flex-wrap">
#                     <div class="p-2 ticketGridItem" style="border: 1px solid #ddd; margin: 0.5rem; border-radius: 5px;">
#                         <div class="mb-2">
#                             <label class="form-check-label">
#                                 <span class="fw-bold">Ticket 1</span> - <span class="text-success">$XX.XX</span><br>
#                                 <span class="text-muted small">
#                                     <input class="form-control seatDetails" placeholder="Enter seat number">
#                                     <div class="seatType">Assigned Seat</div>
#                                     <div class="ticketType">Digital Ticket</div>
#                                 </span>
#                             </label>
#                         </div>
#                     </div>
#                 </div>
#             '''),
#             Submit('submit', 'Submit', css_class='btn btn-primary mt-3')
#         )

#         # JavaScript for handling dynamic fields
#         self.helper.layout.append(HTML('''
            


#         '''))

#         # Modal for adding new venue
#         self.helper.layout.append(HTML('''
#             <div class="modal fade" id="addVenueModal" tabindex="-1" aria-labelledby="addVenueModalLabel" aria-hidden="true">
#                 <div class="modal-dialog">
#                     <div class="modal-content">
#                         <div class="modal-header">
#                             <h5 class="modal-title" id="addVenueModalLabel">Add New Venue</h5>
#                             <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
#                         </div>
#                         <div class="modal-body">
#                             <form id="venueForm">
#                                 <div class="mb-3">
#                                     <label for="venue_region" class="form-label">Event region*</label>
#                                     <input type="text" class="form-control" id="venue_region" disabled>
#                                 </div>
#                                 <div class="mb-3">
#                                     <label for="venue_city" class="form-label">City*</label>
#                                     <input type="text" class="form-control" id="venue_city" required aria-describedby="venue_cityhelp">
#                                     <div id="venue_cityhelp" class="form-text">In case the venue is actually in a suburb, and the city name is different than the region listed above.</div>
#                                 </div>
#                                 <div class="mb-3">
#                                     <label for="venue_name" class="form-label">Venue name*</label>
#                                     <input type="text" class="form-control" id="venue_name" required maxlength=50>
#                                 </div>
#                                 <div class="mb-3">
#                                     <label for="venue_type" class="form-label">Venue type*</label>
#                                     <select id="venue_type" class="form-control" required>
#                                        <option value="">---------</option>
#                                        {% for venue_type in venue_types %}
#                                         <option value="venue_type.id">{{venue_type.type}}</option>
#                                        {% endfor %}
#                                     </select>
#                                 </div>
#                             </form>
#                         </div>
#                         <div class="modal-footer">
#                             <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
#                             <button type="button" class="btn btn-primary" id="saveVenueBtn">Save Venue</button>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#         '''))