"""PlacementPrediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PlacementPredictionApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('collegeLogin/', Login),
    path('Logout/', Logout),
    path('StudentManage/', StudentManage),
    path('SaveStudent/', SaveStudent),
    path('StudentLoginpage/', StudentLoginpage),
    path('StudentRegister/', StudentRegister),
    path('createaccount/', Createaccount),
    path('Studentlogin/', Studentlogin),
    path('UpdateButton/', UpdateButton),
    path('accountDetail/', StudentAccount),
    path('editAccount/', editAccount),
    path('updateAccount/', updateAccount),
    path('Performance/', Performances),
    path('SavePerformance/', SavePerformance),
    path('StudentPerformance/', StudentPerformance),
    path('PerformUpdateRequest/', PerformUpdateRequest),
    path('UpdatePerform/', UpdatePerform),
    path('UpdateRequests/', UpdateRequests),
    path('ApproveRequest/', ApproveRequest),
    path('importstudents/', importStudents),
    path('prediction/<int:id>', studentPrediction),

    path('improveskill/', improveSkill),
    path('preperation/one/', preperationOne),
    path('preperation/two/', preperationTwo),
    path('aboutcampus/', aboutCampus)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
