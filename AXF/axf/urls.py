from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import static

from axf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^regist/', include('axf_app.urls', namespace='regist')),
    url(r'^login/', include('axf_app.urls', namespace='login')),
    url(r'^logout/', include('axf_app.urls', namespace='logout')),

    url(r'^axf/', include('axf_app.urls', namespace='axf'))



]



# 配置这个才能显示正确的路径显示图片
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)