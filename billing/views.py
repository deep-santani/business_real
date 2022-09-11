from unicodedata import decimal
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.shortcuts import render
from .models import *
import json
import datetime
from decimal import Decimal
from django.http import HttpResponse
from django.db.models import Sum

# Create your views here.
def home(request):
    
    if Sale.objects.last() is not None:
        bill_no=str(Sale.objects.last().bill_no+1)
    else:
        bill_no="1"
    if request.method=="POST":
        cname=request.POST['cname']
        phoneno=request.POST['phno']
        email=request.POST['email']
        vehicle_number=request.POST['vehicle_no']
        address=request.POST['address']
        iname=request.POST.getlist('iname')
        iquantity=request.POST.getlist('iquantity')
        iprice=request.POST.getlist('iprice')
        igst=request.POST.getlist('igst')
        total=request.POST['tot']
        discount=request.POST['discount']
        amount=request.POST['paid']
        mode=request.POST['payment_mode']
        gateway=request.POST.get('payment_gateway')
        details=request.POST.get('payment_details')
        pay_later_paid=request.POST.get('pay_later_paid')
        pay_later_balance=request.POST.get('pay_later_balance')
        remark=request.POST.get('remark')
        d=Customer_detail.objects.filter(phoneno=phoneno).values()
        if pay_later_balance is None:
            pay_later_balance=0
            pay_later_paid=amount
        if len(d)==0:
            content={
                "phoneno":phoneno
            }
            if iname[0]!="":
                items_list=[]
                for i in range(len(iname)):
                    temp='"'+iname[i]+'":['+iquantity[i]+','+iprice[i]+','+igst[i]+']'
                    items_list.append(temp)
                items=","
                items=items.join(items_list)
                json_string='{'+items+'}'
                
                json_obj=json.loads(json_string)  
                customer=Customer_detail(name=cname,phoneno=phoneno,email=email,address=address)
                customer.save()
                sale=Sale(customer=customer,vehicle_number=vehicle_number,orders=json_obj,total=total,discount=discount,amount=amount)
                sale.save()
                payment=Payment(bill=sale,customer=customer,mode=mode,gateway=gateway,details=details,pay_later_paid=pay_later_paid,pay_later_balance=pay_later_balance,remark=remark)
                payment.save()
                for j in range(len(iname)):
                    item=Item.objects.filter(iname=iname[j]).values()
                    item.update(istock=Decimal(item[0].get('istock'))-Decimal(iquantity[j]))
                    item.update(isale=Decimal(item[0].get('isale'))+Decimal(iquantity[j]))
                return render(request,'home.html',{'bill_no':bill_no})
        else:
            if iname[0]!="":
                customer=Customer_detail.objects.get(phoneno=phoneno)
                items_list=[]
                for i in range(len(iname)):
                    temp='"'+iname[i]+'":['+iquantity[i]+','+iprice[i]+','+igst[i]+']'
                    items_list.append(temp)
                items=","
                items=items.join(items_list)
                json_string='{'+items+'}'
                json_obj=json.loads(json_string)
                sale=Sale(customer=customer,vehicle_number=vehicle_number,orders=json_obj,total=total,discount=discount,amount=amount)
                sale.save()
                payment=Payment(bill=sale,customer=customer,mode=mode,gateway=gateway,details=details,pay_later_paid=pay_later_paid,pay_later_balance=pay_later_balance,remark=remark)
                payment.save()
                for j in range(len(iname)):
                    item=Item.objects.filter(iname=iname[j]).values()
                    item.update(istock=(Decimal(item[0].get('istock'))-Decimal(iquantity[j])))
                    item.update(isale=Decimal(item[0].get('isale'))+Decimal(iquantity[j]))
                return render(request,'home.html')
            content={
                "name":d[0].get('name'),
                "address":d[0].get('address'),
                "email":d[0].get('email'),
                "phoneno":phoneno
            }
        
        return render(request,'home.html',{'details':content,'bill_no':bill_no})
    
    return render(request,'home.html')
    

def items(request):
    return HttpResponse(serializers.serialize('json',Item.objects.all()),content_type="text/json")
     

def bills(request):
    page=request.GET.get('page',1)
    paginator = Paginator(Payment.objects.all().order_by('-bill_id'), 10)
    totBill=Sale.objects.all().aggregate(Sum('total'))
    totDiscount=Sale.objects.all().aggregate(Sum('discount'))
    totAmt=Sale.objects.all().aggregate(Sum('amount'))
    totPayLaterPaid=Payment.objects.all().aggregate(Sum('pay_later_paid'))
    totPayLaterBal=Payment.objects.all().aggregate(Sum('pay_later_balance'))
    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)
    return render(request,'bills.html',{
        'data':payments,'totBill':totBill,'totDiscount':totDiscount,'totAmt':totAmt,'totPayLaterPaid':totPayLaterPaid,'totPayLaterBal':totPayLaterBal
        })

def delete_bill(request,bill):
    payments=Payment.objects.get(bill_id=bill)
    sale=Sale.objects.get(bill_no=bill)
    items_lst=list(sale.orders.keys())
    print(items_lst)
    for i in range(len(items_lst)):
        item=Item.objects.get(iname=items_lst[i])
        item.istock=item.istock+int(sale.orders.get(item.iname)[0])
        print(item.isale)
        item.isale=item.isale-int(sale.orders.get(item.iname)[0])
        item.save()
    payments.delete()
    sale.delete()

    return HttpResponse("<h1>successfully delete</h1>")

def stock(request):

    items=Item.objects.all().values().order_by('id')
    if request.method=="POST":
        item_id=request.POST.get('item_id')
        item_name=request.POST.get('iname')
        item_price=request.POST.get('iprice')
        item_gst=request.POST.get('igst')
        item_stock=request.POST.get('istock')
        item_sale=request.POST.get('isale')
        new_name=request.POST.get('new_name')
        new_price=request.POST.get('new_price')
        new_gst=request.POST.get('new_gst')
        new_stock=request.POST.get('new_stock')
        
        if item_name is not None:
            Item.objects.filter(id=item_id).update(iname=item_name,iprice=item_price,igst=item_gst,istock=item_stock,isale=item_sale)
        else:
            Item(iname=new_name,iprice=new_price,igst=new_gst,istock=new_stock).save()
    return render(request,'items.html',{'items':items})

def stock_delete(request,id):
    item=Item.objects.get(id=id)
    item.delete()
    return HttpResponse("<h1>Item deleted</h1>")

def bills_filter(request,filter):
    payments_list=[]
    customer_filter=False
    payment_filter=False
    date=request.GET.getlist('date')
    time=request.GET.getlist('time')
    bill_no=request.GET.get('bill_no')
    customer_name=request.GET.get('cname')
    phoneno=request.GET.get('phoneno')
    payment_mode=request.GET.get('payment_mode')
    payment_gateway=request.GET.get('payment_gateway')
    vehicle_number=request.GET.get('vehicle_number')
    billAmt=request.GET.getlist('billAmt')
    address=request.GET.get('address')
    discount=request.GET.getlist('discount')
    totAmt=request.GET.getlist('totAmt')
    amtPaid=request.GET.getlist('amtPaid')
    amtBal=request.GET.getlist('amtBal')
    item_name=request.GET.get('item_name')
    totalAmt=0
    totDiscount=0
    totBill=0
    pay_later_paid=0
    pay_later_balance=0
    if filter=="date":
        sales=Sale.objects.filter(date__range=date).order_by('date')
        totBill=Sale.objects.filter(date__range=date).aggregate(Sum('total'))
        totDiscount=Sale.objects.filter(date__range=date).aggregate(Sum('discount'))
        totalAmt=Sale.objects.filter(date__range=date).aggregate(Sum('amount'))
        
        for i in range(len(sales)):
            payments=Payment.objects.filter(bill=sales[i])
            pay_later_paid+=payments.values()[0].get('pay_later_paid')
            pay_later_balance+=payments.values()[0].get('pay_later_balance')
            payments_list.append(payments)
        
    elif filter=="time":
        sales=Sale.objects.filter(time__range=time).order_by('time')
        totBill=Sale.objects.filter(time__range=time).aggregate(Sum('total'))
        totDiscount=Sale.objects.filter(time__range=time).aggregate(Sum('discount'))
        totalAmt=Sale.objects.filter(time__range=time).aggregate(Sum('amount'))
        for i in range(len(sales)):
            payments=Payment.objects.filter(bill=sales[i])
            pay_later_paid+=payments.values()[0].get('pay_later_paid')
            pay_later_balance+=payments.values()[0].get('pay_later_balance')
            payments_list.append(payments)
    
    elif filter=="bill_no":
        payments=Payment.objects.filter(bill=bill_no)
        payments_list.append(payments)
       
    elif filter=="customer":
        customer=Customer_detail.objects.filter(name=customer_name)
        totBill=Sale.objects.filter(customer=customer[0]).aggregate(Sum('total'))
        totDiscount=Sale.objects.filter(customer=customer[0]).aggregate(Sum('discount'))
        totalAmt=Sale.objects.filter(customer=customer[0]).aggregate(Sum('amount'))
        pay_later_paid=Payment.objects.filter(customer=customer[0]).aggregate(Sum('pay_later_paid'))
        pay_later_paid=pay_later_paid.get('pay_later_paid__sum')
        pay_later_balance=Payment.objects.filter(customer=customer[0]).aggregate(Sum('pay_later_balance'))
        pay_later_balance=pay_later_balance.get('pay_later_balance__sum')
        customer_filter=True
        payments_list=Payment.objects.filter(customer=customer[0])
          
    elif filter=="phoneno":
        customer=Customer_detail.objects.filter(phoneno=phoneno)
        totBill=Sale.objects.filter(customer=customer[0]).aggregate(Sum('total'))
        totDiscount=Sale.objects.filter(customer=customer[0]).aggregate(Sum('discount'))
        totalAmt=Sale.objects.filter(customer=customer[0]).aggregate(Sum('amount'))
        pay_later_paid=Payment.objects.filter(customer=customer[0]).aggregate(Sum('pay_later_paid'))
        pay_later_paid=pay_later_paid.get('pay_later_paid__sum')
        pay_later_balance=Payment.objects.filter(customer=customer[0]).aggregate(Sum('pay_later_balance'))
        pay_later_balance=pay_later_balance.get('pay_later_balance__sum')
        customer_filter=True
        payments_list=Payment.objects.filter(customer=customer[0])
        
    elif filter=="payment_mode":
        payment_filter=True
        pay_later_paid=Payment.objects.filter(mode=payment_mode).aggregate(Sum('pay_later_paid'))
        pay_later_paid=pay_later_paid.get('pay_later_paid__sum')
        pay_later_balance=Payment.objects.filter(mode=payment_mode).aggregate(Sum('pay_later_balance'))
        pay_later_balance=pay_later_balance.get('pay_later_balance__sum')
        payments_list=Payment.objects.filter(mode=payment_mode)
       
        
    
    elif filter=="payment_gateway":
        payment_filter=True
        pay_later_paid=Payment.objects.filter(gateway=payment_gateway).aggregate(Sum('pay_later_paid'))
        pay_later_paid=pay_later_paid.get('pay_later_paid__sum')
        pay_later_balance=Payment.objects.filter(gateway=payment_gateway).aggregate(Sum('pay_later_balance'))
        pay_later_balance=pay_later_balance.get('pay_later_balance__sum')
        payments_list=Payment.objects.filter(gateway=payment_gateway)
        

    elif filter=="vehicle_number":
        sales=Sale.objects.filter(vehicle_number=vehicle_number).order_by('-date')
        for i in range(len(sales)):
            payments=Payment.objects.filter(bill=sales[i])
            payments_list.append(payments)

    elif filter=="address":
        customer=Customer_detail.objects.filter(address__icontains=address)
        customer_filter=True
        for i in range(len(customer)):
            payments=Payment.objects.filter(customer=customer[i])
            for j in range(len(payments)):
                payments_list.append(payments[j])
        
    elif filter=="billAmt":
        sales=Sale.objects.filter(total__range=billAmt).order_by('date')
        for i in range(len(sales)):
            payments=Payment.objects.filter(bill=sales[i])
            payments_list.append(payments)

    elif filter=="discount":
        sales=Sale.objects.filter(discount__range=discount).order_by('date')
        for i in range(len(sales)):
            payments=Payment.objects.filter(bill=sales[i])
            payments_list.append(payments)

    elif filter=="totAmt":
        sales=Sale.objects.filter(amount__range=totAmt).order_by('date')
        for i in range(len(sales)):
            payments=Payment.objects.filter(bill=sales[i])
            payments_list.append(payments)

    elif filter=="amtPaid":
        payment_filter=True
        payments_list=Payment.objects.filter(pay_later_paid__range=amtPaid)

    elif filter=="amtBal":
        payment_filter=True
        payments_list=Payment.objects.filter(pay_later_balance__range=amtBal)

    elif filter=="item":
        
        sales=Sale.objects.filter(orders__has_key=item_name)
        for i in range(len(sales)):
            payments=Payment.objects.filter(bill=sales[i])
            payments_list.append(payments)
        print(sales)

    return render(request,'bills_filter.html',{
        'data':payments_list,'customer_filter':customer_filter,'payment_filter':payment_filter,
        'totBill':totBill,'totDiscount':totDiscount,'totAmt':totalAmt,'pay_later_paid':pay_later_paid,'pay_later_balance':pay_later_balance
        })

def Customers(request):
    return HttpResponse(serializers.serialize('json',Customer_detail.objects.all()),content_type="text/json")