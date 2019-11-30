from django.shortcuts import render,redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
import requests
import json

# Create your views here.
def home(request):
    #pk_c2f90b5fc9ba44f2bdc0cb851270ab5c
    
    if request.method == "POST":
        stock=request.POST['stock']
        
        api_request=requests.get("https://cloud.iexapis.com/stable/stock/" + stock + "/quote?token=pk_c2f90b5fc9ba44f2bdc0cb851270ab5c")
        try:
            api=json.loads(api_request.content,encoding='utf-8')
            
        except Exception as e:
            api="error.."
        return render(request,'home.html',{'api':api})
    else:
        return render(request,'home.html',{'ticker':"enter Stock to see  today's price"})

def about(request):
    return render(request,'about.html') 

def stock(request): 
    if request.method == "POST":
        
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,('Stock has been added'))
            return redirect('stock')
    else:  
        stock=Stock.objects.all() 
        output=[]
        for stock_item in stock:
            api_request=requests.get("https://cloud.iexapis.com/stable/stock/" + str(stock_item) + "/quote?token=pk_c2f90b5fc9ba44f2bdc0cb851270ab5c")
            try:
                api=json.loads(api_request.content,encoding='utf-8') 
                output.append(api)
            except Exception as e:
                api="error.."
         
        return render(request,'stock.html',{'stock':stock ,'output':output}) 
    
def delete(request,stock_id):
    item=Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request,('deleted'))
    return redirect('stock')
    
def delete_stock(request):
    stock=Stock.objects.all() 
    return render(request,'delete_stock.html',{'stock':stock}) 

    
    