from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Product, Shop, Category

class ProductPriceFilter(admin.SimpleListFilter):
    template = "filters/productprice.html"
    title = 'price'
    parameter_name = 'price'
    def lookups(self, request, model_admin):
        return (
            ('none',('none')),
        )
    def queryset(self, request, queryset):
        try:
            if str(self.value()).split(":")[1] != '' and str(self.value()).split(":")[0] != '':
                return queryset.filter(price__lt=str(self.value()).split(":")[1],price__gt=str(self.value()).split(":")[0])
            if str(self.value()).split(":")[1] != '' and str(self.value()).split(":")[0] == '':
                return queryset.filter(price__lt=str(self.value()).split(":")[1])
            if str(self.value()).split(":")[0] != '' and str(self.value()).split(":")[1] == '':
                return queryset.filter(price__gt=str(self.value()).split(":")[0])
            if str(self.value()).split(":")[1] == '' and str(self.value()).split(":")[0] == '':
                return queryset.all()
        except:
            return queryset.all()

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['id','title']
    list_filter = ('active', ProductPriceFilter)
    def get_ordering(self, request):
        return ['amount','price']

class ShopAdmin(admin.ModelAdmin):
    search_fields = ['title']

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    def get_search_results(self, request, queryset, search_term):   # for customize search_list
        queryset,use_distinct = super(CategoryAdmin, self).get_search_results(request,queryset,search_term)
        try:
            products = get_object_or_404(Product, id=int(search_term)).in_category.values_list('id')
            ids = []
            for i in products:
                ids.append(i[0])
            condition = Q(id__in=ids) | Q(title__icontains=search_term)
            queryset |= Category.objects.filter(condition)

        except:
            pass

        return queryset, use_distinct

admin.site.register(Product, ProductAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Category, CategoryAdmin)
