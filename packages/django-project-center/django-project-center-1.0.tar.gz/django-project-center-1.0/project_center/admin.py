import datetime

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin, UserChangeForm, GroupAdmin, Group
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.utils.text import Truncator
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.admin import RelatedOnlyFieldListFilter
from django.utils import timezone

from .models import User, Project, ProjectCategory, ProjectStatus, ProjectStage, ProjectActivity, Company

class ProjectCenterUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        labels = {
            "is_staff": "Can Login"
        }


class ProjectCenterUserAdmin(UserAdmin):

    form = ProjectCenterUserForm
    list_display = ['id', 'first_name', 'last_name', 'email', 'company', 'is_staff', 'email_notify']
    search_fields = ['last_name', 'email']
    readonly_fields = []
    list_filter = ['company', 'groups', 'is_staff', 'email_notify']
    fieldsets = (

        (_("Personal info"), {"fields": (("first_name", "last_name"), "email", "title", "company",
                                         "address_1",
                                         ("city", "state", "postal_code"), "primary_phone",
                                         ("email_notify",),
                                         )}),
        (_("Authentication"), {"fields": (("username", "password"),)}),
        (
            _("Permissions"),
            {
                "fields": (
                    ("is_active",
                    "is_staff",
                    "is_superuser"),
                    "groups",
                ),
            },
        ),
        (_("Important dates"), {"fields": (("last_login", "date_joined"),)}),
        (_("Other/Legacy"), {"fields": ("import_id",)}),
    )

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field)
        return obj

    # inlines = [ApplicationInline, AttachmentsInline]

class CompanyProjectsInline(admin.TabularInline):
    model = Project
    readonly_fields = ('last_activity', 'last_activity_date')
    fields = ('title', 'last_activity', 'last_activity_date', 'status', 'stage', 'category',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CompanyUsersInline(admin.TabularInline):
    model = User

    fields = ('first_name', 'last_name', 'email')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ['name', ]
    ordering = ['name']

    inlines = [CompanyProjectsInline, CompanyUsersInline]


admin.site.register(Company, CompanyAdmin)


class ProjectActivityInline(admin.TabularInline):
    model = ProjectActivity
    readonly_fields = ('name', 'date', 'user', 'get_download_link')
    fields = ('name', 'date', 'user', 'get_download_link')
    show_change_link = True
    ordering = ("-date",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProjectAdmin(admin.ModelAdmin):
    list_display_links = ['id', 'title']
    list_display = ('id', 'title', 'date', 'company', 'last_activity_name', 'last_activity_date', 'status', 'stage', 'category', 'internal')
    list_filter = ['company', 'category', 'status', 'stage', 'internal']
    list_editable = ['category', 'status', 'stage', 'internal']
    search_fields = ['title', 'code', ]
    filter_horizontal = ['users']
    ordering = ['-date']
    inlines = [ProjectActivityInline]
    fieldsets = (

        (_("Project info"), {"fields": ("title", ("company", "category"), ("status", "stage", "internal"), 'date',
                                         )}),
        (_("Project Users"), {"fields": ("users",)}),
    )

    def last_activity(self, obj):
        return obj.projectactivity_set.order_by('-date').first()

    def get_form(self, request, obj=None, **kwargs):
        self.instance = obj
        return super(ProjectAdmin, self).get_form(request, obj=obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Restrict the list of authors to Super Users and Staff only.
        """
        if db_field.name == 'users':
            try:
                if self.instance.company and request.user.is_superuser or request.user.groups.filter(name=settings.PROJECT_CENTER_ADMINISTRATOR_GROUP_NAME).exists():
                    """Do we filter for admins?"""
                    kwargs['queryset'] = User.objects.filter(company=self.instance.company)
                elif self.instance.company:
                    kwargs['queryset'] = User.objects.filter(is_active=True, is_staff=True, company=self.instance.company)
            except:
                kwargs['queryset'] = kwargs['queryset'] = User.objects.filter(is_active=True, is_staff=True, )

        return super(ProjectAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)




admin.site.register(Project, ProjectAdmin)



class ProjectActivityForm(ModelForm):
    model = ProjectActivity
class ProjectActivityAdmin(admin.ModelAdmin):
    form_class = ProjectActivityForm
    list_display_links = ['id','name']
    list_filter = (('project', RelatedOnlyFieldListFilter),)
    readonly_fields = ('project_link', 'user_link', 'get_download_link',"user_name", "project_name")
    list_display = ('id', 'name', 'project_link', 'user_link', 'date', 'get_download_link', 'notes_trunc')
    search_fields = ['name', 'file', ]
    ordering = ('-date',)
    fieldsets = (

        (_("Activity Info"), {"fields": ("name", ("user", "project"), "date", "file", "get_download_link", "notes" )}),)
    project_user_fieldsets = (

        (_("Activity Info"), {"fields": ("name", ("user_name", "project_name"), "date", "get_download_link", "notes", "reply", "reply_file" )}),)
    def get_queryset(self, request):
        """
            For non-superusers, restrict:
             1. For those in the "Project Center User" group, only see those activities and projects which they are directly assigned to
             2. For those in the "Project Center Company Administrator" group, only see project activities to those in the same company
             3. For those in the "Project Center Admininstrator" group - they see all projects and all activities.
            **** SuperUsers see all projects and activites as expected.
        """
        qs = super(ProjectActivityAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.is_project_center_administrator():
            return qs
        elif request.user.is_project_center_company_administrator():
            try:
                return qs.filter(project__company=request.user.company)
            except:
                return None
        elif request.user.is_project_center_user():
            try:
                return qs.filter(project__users__id=request.user.id)
            except:
                return None
        else:
            return None

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser or request.user.is_project_center_administrator():
            self.readonly_fields = (
            'project_link', 'user_link', 'get_download_link', "user_name", "project_name", )
            return self.fieldsets
        elif request.user.is_project_center_company_administrator():
            self.readonly_fields = (
            'name', 'date', 'project_link', 'user_link', 'get_download_link', "user_name", "project_name", 'notes')
            return self.project_user_fieldsets
        elif request.user.is_project_center_user():
            self.readonly_fields = ('name', 'date','project_link', 'user_link', 'get_download_link', "user_name", "project_name", 'notes')
            return self.project_user_fieldsets
        else:
            return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
            For non-superusers, restrict:
             1. For those in the "Project Center User" group, only see those activities and projects which they are directly assigned to
             2. For those in the "Project Center Company Administrator" group, only see project activities to those in the same company
             3. For those in the "Project Center Admininstrator" group - they see all projects and all activities.
            **** SuperUsers see all projects and activites as expected.
        """
        if db_field.name == 'project':
            if request.user.is_superuser or request.user.is_project_center_administrator():
                kwargs['queryset'] = Project.objects.all()
            elif request.user.is_project_center_company_administrator():
                kwargs['queryset'] = Project.objects.filter(company=request.user.company)
            elif request.user.is_project_center_user():
                kwargs['queryset'] = Project.objects.filter(users__id=request.user.id)
            else:
                return None

        return super(ProjectActivityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def notes_trunc(self, obj):
        return Truncator(obj.notes).words(5)

    notes_trunc.short_description = 'Notes'

    def project_name(self, obj):
        return obj.project.title

    project_name.short_description = 'Project'

    def user_name(self, obj):
        return obj.user

    user_name.short_description = 'User'

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_project_center_administrator():
            return True
        elif request.user.is_project_center_company_administrator():
            return False
        elif request.user.is_project_center_user():
            return False
        else:
            return None

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_project_center_administrator():
            return True
        elif request.user.is_project_center_company_administrator():
            return True
        elif request.user.is_project_center_user():
            return True
        else:
            return None

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_project_center_administrator():
            return True
        elif request.user.is_project_center_company_administrator():
            return False
        elif request.user.is_project_center_user():
            return False
        else:
            return None

    def project_link(self, obj):
        try:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:project_center_project_change", args=(obj.project.pk,)),
                obj.project.title
            ))
        except:
            return None

    project_link.short_description = 'Project'

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:project_center_user_change", args=(obj.user.pk,)),
            obj.user.get_full_name()
        )) if obj.user else ''

    user_link.short_description = 'User'

    def activity_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:project_center_activity_change", args=(obj.pk,)),
            obj.name()
        ))

    user_link.short_description = 'User'

    def save_model(self, request, obj, form, change):

        if (form.data.get('reply', None)) is not None or (form.data.get('reply_file', None)) is not None:

            new = ProjectActivity.objects.create(
                name='re: ' + obj.name,
                project=obj.project,
                user=request.user,
                date=timezone.now(),
                notes=form.data.get('reply', None),
                file=request.FILES.get('reply_file', None),
            )

            messages.success(request, 'The new Project Activity "' + new.name + '" was successfully added.')
            return obj
        else:
            super().save_model(request, obj, form, change)

admin.site.register(ProjectActivity, ProjectActivityAdmin)


class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display')


admin.site.register(ProjectCategory, ProjectCategoryAdmin)


class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display')


admin.site.register(ProjectStatus, ProjectStatusAdmin)


class ProjectStageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display')


admin.site.register(ProjectStage, ProjectStageAdmin)

admin.site.register(User, ProjectCenterUserAdmin)
