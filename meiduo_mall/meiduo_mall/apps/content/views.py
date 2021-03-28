from django.shortcuts import render

# Create your views here.
from django.views import View
class ContentView(View):
    #提供广告页面
    def get(self,request):
        return render(request,'index.html')