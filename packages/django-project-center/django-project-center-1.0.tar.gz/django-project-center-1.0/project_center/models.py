import mimetypes
import os
import pathlib
from copy import deepcopy

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.timezone import datetime, make_aware, make_naive

from phonenumber_field.modelfields import PhoneNumberField


class State(models.Model):
    name = models.CharField(_('name'), max_length=100, blank=False)
    abbrev = models.CharField(_('abbrev'), max_length=2, blank=True)
    hash = models.CharField(_('hash'), max_length=40, blank=True, null=True)
    display = models.BooleanField(default=True)
    atsReference = models.IntegerField(_('atsReference'), blank=True, null=True, default=None,
                                       help_text='ATS Reference', )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "States"
        app_label = 'project_center'


class City(models.Model):
    name = models.CharField(_('name'), max_length=100, blank=False)
    state = models.ForeignKey(State, null=True, blank=False, on_delete=models.SET_NULL)
    hash = models.CharField(_('hash'), max_length=40, blank=False, null=False)
    display = models.BooleanField(default=True)

    def __str__(self):
        try:
            return '{city}, {state}'.format(
                city=self.name,
                state=self.state.abbrev)
        except AttributeError as e:
            return str(self.name)

    class Meta:
        verbose_name_plural = "Cities"
        app_label = 'project_center'

    def list_zips(self):
        return [x.zipcode for x in Zip.objects.filter(city=self).order_by('-population_count')]


class Zip(models.Model):
    zipcode = models.CharField(primary_key=True, unique=True, max_length=5)
    city = models.ForeignKey(City, null=True, default=None, related_name='zip', on_delete=models.SET_NULL)
    approximate_latitude = models.FloatField(blank=True, null=True, default=None)
    approximate_longitude = models.FloatField(blank=True, null=True, default=None)
    population_count = models.IntegerField(blank=True, null=True)
    display = models.BooleanField(default=True)

    def __str__(self):
        try:
            return '{zipcode} ({city}, {state})'.format(
                zipcode=self.zipcode,
                city=self.city,
                state=self.city.state.name)
        except AttributeError as e:
            return str(self.zipcode)

    def get_geocode(self):
        return (self.approximate_latitude, self.approximate_longitude)

    def get_geolocation(self):
        return self.get_geocode()

    def get_es_geocode(self):
        return [self.approximate_longitude, self.approximate_latitude]


class Company(models.Model):
    name = models.CharField(_('Company Name'), max_length=100, blank=False)

    class Meta:
        verbose_name = 'Project Company'
        verbose_name_plural = "Project Companies"
        app_label = 'project_center'

    def __str__(self):
        return self.name


class User(AbstractUser):
    """A subclass of the user model for storing persistant candidate data as well as Admin Data."""

    import_id = models.IntegerField(_('Import ID'), blank=True, null=True, default=None, help_text='Import ID')
    title = models.CharField(_('Title'), max_length=64, blank=True, null=True, default='')
    address_1 = models.CharField(_('Address 1'), max_length=64, blank=True, null=True, default='')
    city = models.CharField(_('City'), max_length=64, blank=True, null=True, default='')
    state = models.ForeignKey(State, blank=True, null=True, default=None,
                              on_delete=models.SET_NULL)  # TODO: Add a validator
    postal_code = models.CharField(_('postal_code'), max_length=10, blank=True, null=True, default='',
                                   validators=[])  # TODO: Add a validator
    zip = models.CharField(_('postal_code'), max_length=10, blank=True, null=True, default='',
                           validators=[])  # TODO: Add a validator
    primary_phone = PhoneNumberField(_('primary_phone'), max_length=50, blank=True, null=True, default=None)
    company = models.ForeignKey(Company, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    email_notify = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name()

    class Meta(object):
        app_label = 'project_center'
        verbose_name = _('Project User')
        verbose_name_plural = _('Project Users')

    def _get_FIELD_display(self, field):
        field = super()._get_FIELD_display(field)
        return field

    def send_project_alert_email(self, subject=None, text=None, html=None, sender=None):

        subject, from_email, to = \
            subject if subject else 'Project Alert', \
            sender if sender else settings.EMAIL_DEFAULT_ADMIN_EMAIL_ADDRESS, \
                self.email
        text_content = text if text else 'A Project Activity Occured.'
        html_content = html if html else '<p>A Project Activity Occured.</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def is_project_center_administrator(self):
        if self.groups.filter(
            name=settings.PROJECT_CENTER_ADMINISTRATOR_GROUP_NAME).exists():
            return True
        else:
            return False
    def is_project_center_company_administrator(self):
        if self.groups.filter(
            name=settings.PROJECT_CENTER_COMPANY_ADMINISTRATOR_GROUP_NAME).exists():
            return True
        else:
            return False

    def is_project_center_user(self):
        if self.groups.filter(
            name=settings.PROJECT_CENTER_USER_GROUP_NAME).exists():
            return True
        else:
            return False


class ProjectCategory(models.Model):
    import_id = models.IntegerField(_('Import ID'), blank=True, null=True, default=None, help_text='Import ID')
    name = models.CharField(_('Category Name'), max_length=255, blank=False, help_text='Category Name')
    display = models.BooleanField(default=True)

    class Meta(object):
        app_label = 'project_center'
        verbose_name = _('Project Category')
        verbose_name_plural = _('Project Categories')

    def __str__(self):
        return self.name


class ProjectStatus(models.Model):
    import_id = models.IntegerField(_('Import ID'), blank=True, null=True, default=None, help_text='Import ID')
    name = models.CharField(_('Status Name'), max_length=255, blank=False, help_text='Status Name')
    display = models.BooleanField(default=True)

    class Meta(object):
        app_label = 'project_center'
        verbose_name = _('Project Status')
        verbose_name_plural = _('Project Statuses')

    def __str__(self):
        return self.name


class ProjectStage(models.Model):
    import_id = models.IntegerField(_('Import ID'), blank=True, null=True, default=None, help_text='Import ID')
    name = models.CharField(_('Stage Name'), max_length=255, blank=False, help_text='Stage Name')
    display = models.BooleanField(default=True)

    class Meta(object):
        app_label = 'project_center'
        verbose_name = _('Project Stage')
        verbose_name_plural = _('Project Stages')

    def __str__(self):
        return self.name


class Project(models.Model):
    import_id = models.IntegerField(_('Import ID'), blank=True, null=True, default=None, help_text='Import ID')
    slug = models.SlugField('Slug', max_length=255, blank=True, null=True, unique=True)
    title = models.CharField(_('Title'), max_length=255, blank=False, help_text='Project Title')
    date = models.DateTimeField(_('Start Date'), blank=True, null=True, help_text='Start Date')
    code = models.CharField(_('Code/ID'), max_length=30, null=True, default=None, blank=True, help_text='Project Code')
    category = models.ForeignKey(ProjectCategory, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    status = models.ForeignKey(ProjectStatus, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    stage = models.ForeignKey(ProjectStage, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    internal = models.BooleanField('Internal', blank=False, default=False, )
    description = models.TextField(_('Description'), blank=True, null=True, default=None,
                                   help_text='Project Description')
    company = models.ForeignKey(Company, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    users = models.ManyToManyField(User, blank=True, null=True, default=None, verbose_name='Project Users', help_text='Users from the Company that are '
                                                                                 'allowed to access the Project')
    last_activity_date = models.DateTimeField(_('Last Activity Date'), blank=True, null=True, help_text='Last Activity Date')
    last_activity_name = models.CharField(_('Last Activity Name'), max_length=255, null=True, default=None, blank=True, help_text='Last Activity Name')



    class Meta(object):
        app_label = 'project_center'
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        last = self.last_activity()
        if last:
            self.last_activity_date = last.date if last else None
            self.last_activity_name = last.name if last else None
        super().save(*args, **kwargs)

    def last_activity(self):
        try:
            return self.projectactivity_set.order_by('-date').first()
        except:
            return None

    def category_name(self):
        return self.category.name if self.category else None

    def get_absolute_url(self):
        return reverse('project-detail', args=[self.id])

    def send_group_alert(self, message=None):
        for user in self.users.all():
            print(user)


def activity_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    try:
        return 'project_activity_files/{0}/{1}'.format(instance.project.slug, os.path.basename(filename))
    except:
        return None


class ProjectActivity(models.Model):
    import_id = models.IntegerField(_('Import ID'), blank=True, null=True, default=None, help_text='Import ID')
    name = models.CharField(_('Activity Name'), max_length=255, blank=False, help_text='Activity Name')
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, blank=True, null=True, default=None, on_delete=models.CASCADE)
    date = models.DateTimeField(_('Activity Date'), blank=True, null=True, help_text='Activity Date')
    file = models.FileField(upload_to=activity_file_directory_path, blank=True, null=True, max_length=255)
    notes = models.TextField('Activity Notes', blank=True, null=True)
    reply = models.TextField('Comments/Reply', blank=True, null=True, help_text='*** Adding or changing Comments will '
                                                                                'add a new Activity Record to the '
                                                                                'Project History')
    reply_file = models.FileField('File Attachment', upload_to=activity_file_directory_path, blank=True, null=True,
                                  help_text='*** Attaching a new File will add a new Activity Record to the Project '
                                            'History')



    class Meta(object):
        app_label = 'project_center'
        verbose_name = _('Project Activity')
        verbose_name_plural = _('Project Activities')

    def __str__(self):
        return self.name

    def get_filename(self):
        return os.path.basename(self.file.name) if self.file else None

    def get_mimetype(self):
        return mimetypes.guess_type(self.get_filename())[0] if self.file else None

    def get_suffix(self):
        return pathlib.Path(self.get_filename()).suffix if self.file else None

    def get_download_link(self):
        if self.get_filename():
            return mark_safe(
                '<a href="' + reverse('activity-download', args=[self.id]) + '">' + self.get_filename() + '</a>')
        else:
            return None

    get_download_link.short_description = 'Download Link'

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)
