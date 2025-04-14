from django import forms
from django.utils import timezone

from .models import Status, Type, Category, Subcategory, CashFlow


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'})
        }


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполняем queryset для поля category всеми доступными категориями
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = 'Выберите категорию'


class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = ['created_date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'created_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_created_date'}),
            'status': forms.Select(attrs={'class': 'form-control', 'id': 'id_status'}),
            'type': forms.Select(attrs={'class': 'form-control', 'id': 'id_type', 'onchange': 'loadCategories()'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'id_category',
                                            'onchange': 'loadSubcategories()'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'id_subcategory'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01',
                                               'id': 'id_amount'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'id_comment'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # сделаем поле необязательным в форме
        self.fields['created_date'].required = False

        # если значение не задано — подставим сегодняшнее
        if not self.initial.get('created_date'):
            self.initial['created_date'] = timezone.now().date()

        type_id = self.data.get('type') or (self.instance.type.id if self.instance.pk else None)
        category_id = self.data.get('category') or (self.instance.category.id if self.instance.pk else None)

        if type_id:
            self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
        else:
            self.fields['category'].queryset = Category.objects.none()

        if category_id:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
        else:
            self.fields['subcategory'].queryset = Subcategory.objects.none()

        self.fields['category'].empty_label = '---------'
        self.fields['subcategory'].empty_label = '---------'

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        type_obj = cleaned_data.get('type')

        # если дата не указана — ставим текущую
        if not cleaned_data.get('created_date'):
            cleaned_data['created_date'] = timezone.now().date()

        if category and type_obj and category.type != type_obj:
            self.add_error('category', 'Выбранная категория не соответствует выбранному типу операции')

        if subcategory and category and subcategory.category != category:
            self.add_error('subcategory', 'Выбранная подкатегория не соответствует выбранной категории')

        return cleaned_data
