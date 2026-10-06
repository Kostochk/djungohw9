from django.db import models

class Product(models.Model):
    """Модель Товару"""
    name = models.CharField(max_length=150, verbose_name="Назва товару")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна за одиницю")
    description = models.TextField(blank=True, null=True, verbose_name="Опис товару")

    def __str__(self):
        return self.name


class Buyer(models.Model):
    """Модель Покупця"""
    name = models.CharField(max_length=150, verbose_name="Повне ім'я / Компанія")
    phone = models.CharField(max_length=20, verbose_name="Контактний телефон")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")

    def __str__(self):
        return self.name


class Seller(models.Model):
    """Модель Продавця"""
    name = models.CharField(max_length=150, verbose_name="ПІБ Продавця")
    store_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Назва торгової точки")

    def __str__(self):
        return self.name


class Sale(models.Model):
    """Модель Продажу (Связующая таблица)"""
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name="Покупець")
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name="Продавець")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    
    quantity = models.PositiveIntegerField(verbose_name="Кількість")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Загальна сума")
    date = models.DateField(verbose_name="Дата продажу")

    def save(self, *args, **kwargs):
        """Автоматический пересчет общей суммы перед сохранением в базу"""
        if self.product and self.quantity:
            self.total_amount = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Продаж №{self.id} від {self.date}"