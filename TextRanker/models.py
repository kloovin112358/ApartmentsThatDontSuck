from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from djmoney.models.fields import MoneyField
from django.utils.text import slugify
from django.urls import reverse
import uuid

class DisposableEmailDomain(models.Model):
    domain = models.CharField(max_length=100)

    def __str__(self):
        return self.domain

def validate_not_disposable_email(email):
    domain = email.split('@')[1]
    if DisposableEmailDomain.objects.filter(domain=domain).exists():
        raise ValidationError(_('Error: our systems have detected that you are using a disposable email address. Please select a different email.'))

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):

    username = None
    email = models.EmailField(_('email address'), unique=True, validators=[validate_not_disposable_email])
    verified_account = models.BooleanField(default=False, verbose_name="Verified account?", help_text="Flipped to true when user clicks verification link sent to email address")
    account_under_review = models.BooleanField(default=False, verbose_name="Account under review?", help_text="This will be true when a ticket listing by this user has been reported")
    account_banned = models.BooleanField(default=False, verbose_name="Account banned?", help_text="If this is true, user has been banned for cause after review by admin")
    ban_datetime = models.DateTimeField(blank=True, null=True, verbose_name="Date and time of account ban")
    ban_removal_datetime = models.DateTimeField(blank=True, null=True, verbose_name="Date and time account ban to be removed")
    ban_reason = models.TextField(blank=True, null=True, verbose_name="Reason for account ban")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class EmailVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    verified_datetime = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        account = self.account
        if self.verified_datetime and not account.verified_account:
            account.verified_account = True
            account.save()
        super().save(*args, **kwargs)

class Neighborhood(models.Model):
    name = models.CharField(max_length=50)
    desirability = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# class Building(models.Model):
#     address = models.CharField(max_length=100, blank=True, null=True)
#     name = models.CharField(max_length=100, blank=True, null=True)  # Optional
#     neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
#     location_in_neighborhood_rating = models.PositiveSmallIntegerField()

#     def __str__(self):
#         return self.name if self.name else self.address

class ListingSite(models.Model):
    site_name = models.CharField(max_length=50)

    def __str__(self):
        return self.site_name

class UnitType(models.Model):
    unitType = models.CharField(max_length=20)

    def __str__(self):
        return self.unitType

class Unit(models.Model):
    STATUS_CHOICES = [
        ('Live', 'Live'),
        ('Sold', 'Sold'),
        ('Sucks', 'Sucks'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    datetime_added = models.DateTimeField()
    datetime_removed = models.DateTimeField(blank=True, null=True)  # Optional
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.RESTRICT)
    # building = models.ForeignKey(Building, on_delete=models.RESTRICT)
    # unit = models.CharField(max_length=10)
    unitType = models.ForeignKey(UnitType, on_delete=models.RESTRICT)
    listing_site = models.ForeignKey(ListingSite, on_delete=models.RESTRICT, blank=True, null=True)
    listing_link = models.CharField(unique=True, max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # availability_date = models.DateField()
    # square_footage = models.PositiveIntegerField()
    # view_natural_light_rating = models.PositiveSmallIntegerField()
    # has_dishwasher = models.BooleanField(default=False)
    # has_in_unit_washer_dryer = models.BooleanField(default=False)
    # has_air_conditioning = models.BooleanField(default=False)
    # is_bad_floor_of_building = models.BooleanField(default=False, help_text="If basement, ground floor looking out onto street, or second floor looking out onto busy street.")
    quality_rating = models.PositiveSmallIntegerField()
    value_rating = models.PositiveSmallIntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.listing_link

    def calculate_value_rating(self):
        try:
            quality_value = QualityValue.objects.get(
                unit_type=self.unitType,
                quality_rating=self.quality_rating,
                min_max=QualityValuePriceMinMax.objects.get(
                    unit_type=self.unitType,
                    price_min__lte=self.price,
                    price_max__gt=self.price
                )
            )
            return quality_value.value_rating
        except Exception as e:
            # Handle cases where no matching QualityValue exists
            return None

    def save(self, *args, **kwargs):
        # Calculate the value_rating before saving the Unit instance
        newValueRating = self.calculate_value_rating()
        if newValueRating is not None:
            if self.value_rating is not None and self.value_rating == newValueRating:
                pass
            else:
                self.value_rating = newValueRating
        super(Unit, self).save(*args, **kwargs)
    
REPORT_STATUS_CHOICES = [
    ('Open', 'Open'),
    ('Dismissed', 'Dismissed'),
    ('Actioned', 'Actioned'),
]

class UnitSucksReport(models.Model):
    status = models.CharField(max_length=10, choices=REPORT_STATUS_CHOICES, default="Open")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    description = models.TextField()
    datetime_submitted = models.DateTimeField()

    def __str__(self):
        return f"Report by {self.user} on {self.unit}"
    
class UnitNotAvailableReport(models.Model):
    status = models.CharField(max_length=10, choices=REPORT_STATUS_CHOICES, default="Open")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    datetime_submitted = models.DateTimeField()

    def __str__(self):
        return f"Report by {self.user} on {self.unit}"

class Search(models.Model):
    listing_site = models.ForeignKey(ListingSite, on_delete=models.CASCADE)
    search_url = models.CharField(max_length=1000)
    last_item_note = models.TextField(help_text="This will help you know when to stop browsing on the search. When you hit the item that says this, STOP.")
    unitType = models.ForeignKey(UnitType, on_delete=models.RESTRICT, related_name="searches")
    last_updated = models.DateTimeField()
    live_search = models.BooleanField(default=True)

    def __str__(self):
        return "Search for {0} {1}".format(str(self.unitType), str(self.listing_site))
    
class SavedUnit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Saved unit by {self.user}"

class ContactFormMessage(models.Model):
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.message

class QualityRating(models.Model):
    quality_rating = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return str(self.quality_rating)

class QualityValuePriceMinMax(models.Model):
    unit_type = models.ForeignKey(UnitType, on_delete=models.RESTRICT)
    price_min = models.DecimalField(max_digits=8, decimal_places=2)
    price_max = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        # Format the prices as integers if they have no decimal places
        price_min_str = "${:,.0f}".format(self.price_min)
        price_max_str = "${:,.0f}".format(self.price_max)
        
        return f"{price_min_str} - {price_max_str}"

    class Meta:
        unique_together = ('price_min', 'price_max', 'unit_type',)
        ordering = ['price_min']

class QualityValue(models.Model):
    unit_type = models.ForeignKey(UnitType, on_delete=models.RESTRICT)
    quality_rating = models.ForeignKey(QualityRating, on_delete=models.RESTRICT)
    min_max = models.ForeignKey(QualityValuePriceMinMax, on_delete=models.CASCADE)
    value_rating = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('quality_rating', 'min_max',)
    
    def __str__(self):
        return "{0}, {1}, {2} = {3}".format(str(self.unit_type), str(self.min_max), str(self.quality_rating), str(self.value_rating))