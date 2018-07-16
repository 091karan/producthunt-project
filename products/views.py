from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product,Comment
from django.utils import timezone

def home(request):
    products = Product.objects
    return render(request,'products/home.html',{'products':products})

@login_required(login_url = '/accounts/signup')
def create(request):
    if request.method == "POST":
        if(request.POST['title'] and request.POST['url'] and request.POST['body'] and request.FILES['icon'] and request.FILES['image']):
            product = Product()
            product.title = request.POST['title']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.body = request.POST['body']
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
    else:
        return render(request,'products/create.html')

def detail(request,product_id):
    product = get_object_or_404(Product,pk=product_id)
    comment = Comment.objects.filter(productid=product_id)
    return render(request,'products/detail.html',{"product":product,"comments":comment})

@login_required(login_url = '/accounts/signup')
def upvote(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product,pk=product_id)
        product.count += 1
        product.save()
        return redirect('/products/' + str(product.id))

@login_required(login_url = '/accounts/signup')
def comment(request,product_id):
    if request.method == "POST":
        comment = Comment()
        comment.commented_user = request.user
        comment.body = request.POST['body']
        comment.productid = product_id
        comment.save()
        return redirect('/products/' + str(product_id))
