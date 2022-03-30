from django.shortcuts import render
from .models import User # 新增的程式碼
from zipfile import ZipFile
from . import call
import json
import os
import uuid

# Create your views here.
def add(request):
    if request.method == "POST":
        upload_id = uuid.uuid4().hex
        context = {'upload_id': upload_id}
        zip_file = request.FILES.get('zip_file')
        image_num = request.POST.get('image_num')

        with ZipFile(zip_file, 'r') as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall()
        
        call.main(str(zip_file).split(".")[0], int(image_num), upload_id)
        # user = User(user_image=user_img)
        # user.save()
        return render(request, 'creator/download.html/', context)
    return render(request, 'creator/add.html', locals())

def download(request):
    # if request.method == "POST":
    #     import requests
    #     url = 'https://www.facebook.com/favicon.ico'
    #     r = requests.get(url, allow_redirects=True)
    #     open('facebook.ico', 'wb').write(r.content)
        # return render(request, 'creator/add.html', locals())
    # =====新增的程式碼=====#
    return render(request, 'creator/download.html', locals())

def detail(request):
    list_user = User.objects.all()
    return render(request, 'creator/detail.html', locals())