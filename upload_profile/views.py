from django.shortcuts import render
from .models import User # 新增的程式碼
from zipfile import ZipFile
from . import call
import json
import os

# Create your views here.
def add(request):
    # print(os.getcwd())
    # with open('data.json') as f:
    #     data = json.load(f)
    # print(data['name'])

    if request.method == "POST":

        zip_file = request.FILES.get('zip_file')
        total_images = request.POST.get('total_images')

        with ZipFile(zip_file, 'r') as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall()
        call.main(str(zip_file).split(".")[0], int(total_images))
        # user = User(user_image=user_img)
        # user.save()
        return render(request, 'upload_profile/download.html', locals())
    return render(request, 'upload_profile/add.html', locals())

def download(request):
    # if request.method == "POST":
    #     import requests
    #     url = 'https://www.facebook.com/favicon.ico'
    #     r = requests.get(url, allow_redirects=True)
    #     open('facebook.ico', 'wb').write(r.content)
        # return render(request, 'upload_profile/add.html', locals())
    # =====新增的程式碼=====#
    return render(request, 'upload_profile/download.html', locals())

def detail(request):
    list_user = User.objects.all()
    return render(request, 'upload_profile/detail.html', locals())