from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User 
from django.contrib.auth import logout,authenticate,login
from home.models import Book,Package,Payment
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives
import razorpay
from django.views.decorators.csrf import csrf_exempt
# priynsh 0208 priy PRIY@0208

# Create your views here.
def index(request):
    print(request.user)
    packages = Package.objects.all()[:3]

    if request.user.is_anonymous:
    #     return redirect('/signup')
        messages.success(request,'Welcome Dear User, You have to login first for booking our packages')   
    else:
        messages.success(request,'Welcome User')
    return render(request, 'index.html', {'packages':packages})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        print(username,first_name,last_name,email,password,cpassword)

        # check if user has correct credential
        user = User.objects.create_user(username,email,password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('login')

    return render(request,"signup.html")

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        # check if user has correct credential
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            
            # Send Welcome mail
            subject= "Welcome to Shree Travels"
            msg=  f'Hi <b>{user.username}</b>,<br>You have successfully logged in to <b>Shree Travels</b>. <br><br><br>Regards, <br>Shree Travels.'
            from_email= settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            msg=EmailMultiAlternatives(subject,msg,from_email,recipient_list )
            msg.content_subtype='html'
            msg.send()
            print('mail send successfully')
            return redirect('home')
        else:
            print('User not login ')
            return redirect('login')

    return render(request, 'login1.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def about(request):
    return render(request,"about.html")

def package(request):
    packages = Package.objects.all()
    return render(request,"package.html",{'packages':packages})

def Gallery(request):
    return render(request,"gallery.html")

def detail(request):
    packages = Package.objects.all()
    context ={
        'packages':packages
        }
    return render(request,"detail.html",context)

def package_detail(request,id):
    package = Package.objects.filter(id=id)
    print(package)
    return render(request,"detail.html",{'package':package[0]})

def book(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobileno = request.POST.get('mobileno')
        address = request.POST.get('address')
        location = request.POST.get('location')
        guests = request.POST.get('guests')
        arrivals = request.POST.get('arrivals')
        leaving = request.POST.get('leaving')
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET)) 
        booking = Book(name=name,email=email,mobileno=mobileno,address=address,location=location,guests=guests,arrivals=arrivals,leaving=leaving)
        booking.save()
    packages = Package.objects.all()
    context ={
        'packages':packages,
    }
    return render(request,"book.html",context)

@csrf_exempt
def payment(request):
    if request.method == 'POST':
        payment_id=request.POST.get('razorpay_payment_id')
        print(request.POST)
        # a= request.POST
        # order_id:""
        # for key, val in a.items():
        #     if key == 'razorpay_order_id':
        #         order_id = val
        #         break
        # user = Payment.objects.filter(payment_id=order_id).first()
        # user.paid = True
        # user.save()
        book = Book.objects.all()
        context={
            'book':book
        }
    return render(request,"pay.html")
