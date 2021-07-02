from django.shortcuts import render
# import models class
from store.models import Category, Product

# import Views class
from django.views.generic import ListView, DetailView

# import mixin for login required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class HomeListView(ListView):
    model = Product
    template_name = 'store/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.filter(parent=None)
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'store/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_obj = Category.objects.get(name=self.object.category)
        context['releted_product'] = Product.objects.filter(category=cat_obj).order_by('-created')
        return context


@login_required
def category_product(request, pk):
    category = Category.objects.get(id=pk)
    cat_products = Product.objects.filter(category=category)

    context = {
        'cat_products': cat_products
    }
    return render(request, 'store/category.html', context)


@login_required
def category_quickview(request, pk):
    quickview = Product.objects.get(id=pk)
    context = {
        'quickview_item': quickview
    }
    return render(request, 'store/quickView.html', context)
