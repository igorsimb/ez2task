from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.contrib.auth.decorators import login_required
from ckeditor_uploader import views
from django.urls import re_path
from django.views.decorators.cache import never_cache


urlpatterns = [
          path('admin/', admin.site.urls),
          path('', include('main_app.urls')),
          path('', include('users.urls')),

          # CKEditor
          re_path(r"^upload/", login_required(views.upload), name="ckeditor_upload"),
          re_path(r"^browse/", never_cache(login_required(views.browse)), name="ckeditor_browse", ),

          # Debug toolbar
          # path('__debug__/', include(debug_toolbar.urls)),
      ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'EZ2 Task'
