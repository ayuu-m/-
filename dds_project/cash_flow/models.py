# models.py
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Status(models.Model):
    """Модель для хранения статусов ДДС (Бизнес, Личное, Налог и т.д.)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название статуса")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class Type(models.Model):
    """Модель для хранения типов операций (Пополнение, Списание и т.д.)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название типа")

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для хранения категорий (Инфраструктура, Маркетинг и т.д.)"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories', verbose_name="Тип")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ['name', 'type']

    def __str__(self):
        return f"{self.name} ({self.type})"


class Subcategory(models.Model):
    """Модель для хранения подкатегорий (VPS, Proxy, Farpost, Avito и т.д.)"""
    name = models.CharField(max_length=100, verbose_name="Название подкатегории")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories',
                                 verbose_name="Категория")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ['name', 'category']

    def __str__(self):
        return f"{self.name} ({self.category})"


class CashFlow(models.Model):
    """Модель для хранения записей о движении денежных средств"""
    created_date = models.DateField(default=timezone.now, verbose_name="Дата создания")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)],
                                 verbose_name="Сумма (руб.)")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время записи в систему")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    class Meta:
        verbose_name = "Движение денежных средств"
        verbose_name_plural = "Движение денежных средств"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.created_date} - {self.type} - {self.category} - {self.amount} руб."
