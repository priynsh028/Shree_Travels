from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User 
from django.contrib.auth import logout,authenticate,login
from home.models import Book,Package
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
import razorpay

# priynsh 0208 priy PRIY@0208
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
# Create your views here.
def index(request):
    print(request.user)
    packages = Package.objects.all()[:3]

    if request.user.is_anonymous:
        messages.success(request,'Welcome Dear User, You have to login first for booking our packages')   
    else:
        messages.success(request,'Welcome to our travel portal! Book your package now and get ready for an unforgettable trip!')
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
    return render(request,"detail.html",{'package':package[0]})

def book(request,id):
    packages = Package.objects.all()
    package = Package.objects.filter(id=id)

    context ={
        'packages':packages,
        'package':package[0],
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobileno = request.POST.get('mobileno')
        address = request.POST.get('address')
        location = request.POST.get('location')
        guests = request.POST.get('guests')
        arrivals = request.POST.get('arrivals')
        leaving = request.POST.get('leaving')
        pprice = request.POST.get('pprice')
        # save
        booking = Book(name=name,email=email,mobileno=mobileno,address=address,location=location,guests=guests,arrivals=arrivals,leaving=leaving,pprice=pprice,user=request.user)
        booking.save()

        return redirect('pay')
    return render(request,"book.html",context)


def pay(request):
    book = Book.objects.filter(user=request.user).last() 
    amount = int(book.pprice) 
    print('package price is:',amount)
    payment = client.order.create({
        "amount": amount * 100,
        "currency":"INR",
        "payment_capture":"1"
        })
    print(payment)
    order_id = payment['id']
    print(order_id)
    book.order_id = order_id
    book.save()
    booking = Book(order_id=order_id)
    context = {
        'book':book,
        'payment':payment,
        'order_id': order_id 
    }
    return render(request,"pay.html",context)

@csrf_exempt
def success(request):
    book_details = Book.objects.filter(user=request.user).last()  
    book = Book.objects.filter(user=request.user).last()  
    context = {
        'book':book_details,
    }
    if request.method == "POST":
        a = request.POST
        print(a)
        order_id = ''
        for key , val in a.items():
            if key == 'order_id':
                order_id = val
                break
        # book = Book.objects.filter(order_id=order_id).first()
        book_details.paid = True
        book_details.save()

        user = request.user
        # Send Welcome mail
        subject = "Package Payment Successful"
        from_email = settings.EMAIL_HOST_USER
        msg = f"""
            Thank You <b>{user.username}</b>,
            <br>
            <h2>Payment Successful</h2>
            <p>
                Name: {book.name}<br>
                Email Id: {book.email}<br>
                Mobile no: {book.mobileno}<br>
                Address: {book.address}<br>
                Package: {book.location}<br>
                Guests: {book.guests}<br>
                Arrivals Date: {book.arrivals}<br>
                Leaving Date: {book.leaving}<br>
                Package Amount: {book.pprice}<br>
                Payment Id: {book.order_id}<br>
            </p>
            <br>
            Regards,<br>
            Shree Travels.
        """
        recipient_list = [user.email]
        msg = EmailMultiAlternatives(subject,msg,from_email,recipient_list)
        msg.content_subtype='html'
        msg.send()
        print('Payment mail sent')
    return render(request,"success.html",context)