from django.db import models
from django.conf import  settings
from mainapp.models import Product


class Basket(models.Model):
    class Meta:
        verbose_name='Корзина'
        verbose_name_plural='Корзины'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=1)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @property
    def product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        "return total quantity for user"
        items = Basket.objects.filter(user=self.user)
        totalquantity = sum(list(map(lambda x: x.quantity, items)))
        return totalquantity

    @property
    def total_cost(self):
        "return total cost for user"
        items = Basket.objects.filter(user=self.user)
        totalcost = sum(list(map(lambda x: x.product_cost, items)))
        return totalcost

    def _str_(self):
        return self.user.name + '  ' +  self.product.name