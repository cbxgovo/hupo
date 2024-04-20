"""
URL configuration for hupo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

# 导入 跟下面的找函数的对应的
from app01 import views

urlpatterns = [

    path('admin/', admin.site.urls),
    # 去app01 访问网页index则取里面的views找这个index函数
    path('index/test', views.index_test),

    path('index/', views.upload_file),
    path('add/',views.files,name='add')












]





