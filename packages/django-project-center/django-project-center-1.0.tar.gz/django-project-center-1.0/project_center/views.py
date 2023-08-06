from django.http import HttpResponse, FileResponse, HttpResponseForbidden
from django.views.generic import UpdateView, View, FormView, TemplateView, ListView
from .models import ProjectActivity

class AttachmentDownloadView(View):
    def get(self, request, *args, **kwargs):
        try:
            obj = ProjectActivity.objects.get(id=kwargs['activity_id'])
            if request.user.is_superuser or request.user.is_project_center_administrator():
                return FileResponse(obj.file)
            elif request.user.is_project_center_company_administrator():
                return FileResponse(obj.file)
            elif request.user.is_project_center_user():
                return FileResponse(obj.file)
            else:
                return HttpResponseForbidden()

            # if self.request.user.is_superuser or self.request.user.id == obj.user.id:
            #     return FileResponse(obj.file)
            # else:
            #     return HttpResponseForbidden()
        except:
            return HttpResponseForbidden()