from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count, Q
from .models import Buyer, Seller, Product, Sale
from .forms import ProductForm  

def product_edit(request, pk):
    """Редагування товару (Завдання 1)"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('reports_dashboard')  # або на список товарів
    else:
        form = ProductForm(instance=product)
    return render(request, 'sales/edit_form.html', {'form': form, 'title': f'Редагувати {product.name}'})

def product_delete(request, pk):
    """Видалення товару (Завдання 2)"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('reports_dashboard')
    return render(request, 'sales/confirm_delete.html', {'obj': product})


def reports_dashboard(request):
    context = {}

    seller_id = request.GET.get('seller_for_buyers')
    if seller_id:
        context['buyers_by_seller'] = Buyer.objects.filter(sale__seller_id=seller_id).distinct()
        context['selected_seller'] = get_object_or_404(Seller, pk=seller_id)

    specific_date = request.GET.get('specific_date')
    if specific_date:
        sales_on_date = Sale.objects.filter(date=specific_date)
        context['sales_on_date'] = sales_on_date
        context['total_sum_on_date'] = sales_on_date.aggregate(total=Sum('total_amount'))['total'] or 0

    product_id = request.GET.get('product_filter')
    if product_id:
        context['sellers_by_product'] = Seller.objects.filter(sale__product_id=product_id).distinct()
        context['buyers_by_product'] = Buyer.objects.filter(sale__product_id=product_id).distinct()
        context['selected_product'] = get_object_or_404(Product, pk=product_id)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    date_filter = Q()
    if start_date and end_date:
        date_filter = Q(sale__date__range=[start_date, end_date])
        context['time_period'] = f"з {start_date} по {end_date}"

    context['top_product_global'] = Product.objects.annotate(sales_count=Count('sale')).order_by('-sales_count').first()
    if start_date and end_date:
        context['top_product_period'] = Product.objects.filter(sale__date__range=[start_date, end_date]).annotate(
            sales_count=Count('sale')
        ).order_by('-sales_count').first()

    context['top_seller_global'] = Seller.objects.annotate(total_sales=Sum('sale__total_amount')).order_by('-total_sales').first()
    if start_date and end_date:
        context['top_seller_period'] = Seller.objects.filter(sale__date__range=[start_date, end_date]).annotate(
            total_sales=Sum('sale__total_amount')
        ).order_by('-total_sales').first()

    context['top_buyer_global'] = Buyer.objects.annotate(total_spent=Sum('sale__total_amount')).order_by('-total_spent').first()
    # За проміжок часу:
    if start_date and end_date:
        context['top_buyer_period'] = Buyer.objects.filter(sale__date__range=[start_date, end_date]).annotate(
            total_spent=Sum('sale__total_amount')
        ).order_by('-total_spent').first()

    context['all_sellers'] = Seller.objects.all()
    context['all_products'] = Product.objects.all()

    return render(request, 'sales/dashboard.html', context)