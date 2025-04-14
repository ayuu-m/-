from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from .models import Status, Type, Category, Subcategory, CashFlow
from .forms import CashFlowForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm


class IndexView(View):
    """Главная страница с таблицей записей и фильтрами"""

    def get(self, request):
        # Получение параметров фильтрации из запроса
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        status_id = request.GET.get('status')
        type_id = request.GET.get('type')
        category_id = request.GET.get('category')
        subcategory_id = request.GET.get('subcategory')

        # Формирование запроса с учетом фильтров
        cash_flows = CashFlow.objects.all()

        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                cash_flows = cash_flows.filter(created_date__gte=date_from_obj)
            except ValueError:
                pass

        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                cash_flows = cash_flows.filter(created_date__lte=date_to_obj)
            except ValueError:
                pass

        if status_id:
            cash_flows = cash_flows.filter(status_id=status_id)

        if type_id:
            cash_flows = cash_flows.filter(type_id=type_id)

        if category_id:
            cash_flows = cash_flows.filter(category_id=category_id)

        if subcategory_id:
            cash_flows = cash_flows.filter(subcategory_id=subcategory_id)

        # Расчет суммарных значений для отображения статистики
        income_sum = cash_flows.filter(type__name='Пополнение').aggregate(Sum('amount'))['amount__sum'] or 0
        expense_sum = cash_flows.filter(type__name='Списание').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = income_sum - expense_sum

        # Данные для фильтров
        statuses = Status.objects.all()
        types = Type.objects.all()
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()

        context = {
            'cash_flows': cash_flows,
            'statuses': statuses,
            'types': types,
            'categories': categories,
            'subcategories': subcategories,
            'income_sum': income_sum,
            'expense_sum': expense_sum,
            'balance': balance,
            'filters': {
                'date_from': date_from,
                'date_to': date_to,
                'status_id': int(status_id) if status_id and status_id.isdigit() else None,
                'type_id': int(type_id) if type_id and type_id.isdigit() else None,
                'category_id': int(category_id) if category_id and category_id.isdigit() else None,
                'subcategory_id': int(subcategory_id) if subcategory_id and subcategory_id.isdigit() else None,
            }
        }

        return render(request, 'cash_flow/index.html', context)


class CashFlowCreateView(View):
    """Представление для создания новой записи"""

    def get(self, request):
        form = CashFlowForm(initial={'created_date': timezone.now().date()})
        return render(request, 'cash_flow/cash_flow_form.html', {'form': form})

    def post(self, request):
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно создана')
            return redirect('index')
        return render(request, 'cash_flow/cash_flow_form.html', {'form': form})


class CashFlowUpdateView(View):
    """Представление для редактирования записи"""

    def get(self, request, pk):
        cash_flow = get_object_or_404(CashFlow, pk=pk)
        form = CashFlowForm(instance=cash_flow)
        return render(request, 'cash_flow/cash_flow_form.html', {'form': form, 'cash_flow': cash_flow})

    def post(self, request, pk):
        cash_flow = get_object_or_404(CashFlow, pk=pk)
        form = CashFlowForm(request.POST, instance=cash_flow)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно обновлена')
            return redirect('index')
        return render(request, 'cash_flow/cash_flow_form.html', {'form': form, 'cash_flow': cash_flow})


class CashFlowDeleteView(View):
    """Представление для удаления записи"""

    def get(self, request, pk):

        cash_flow = get_object_or_404(CashFlow, pk=pk)
        return render(request, 'cash_flow/cash_flow_confirm_delete.html', {'cash_flow': cash_flow})

    def post(self, request, pk):

        cash_flow = get_object_or_404(CashFlow, pk=pk)
        cash_flow.delete()
        messages.success(request, 'Запись успешно удалена')
        return redirect('index')


class DictionaryView(View):
    """Представление для управления справочниками"""

    def get(self, request):
        statuses = Status.objects.all()
        types = Type.objects.all()
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()

        subcategory_form = SubcategoryForm()
        # Явно установим queryset для поля категорий
        subcategory_form.fields['category'].queryset = categories

        context = {
            'statuses': statuses,
            'types': types,
            'categories': categories,
            'subcategories': subcategories,
            'status_form': StatusForm(),
            'type_form': TypeForm(),
            'category_form': CategoryForm(),
            'subcategory_form': subcategory_form,  # Используем модифицированную форму
        }

        return render(request, 'cash_flow/dictionaries.html', context)


# Представления для управления статусами
class StatusCreateView(View):
    def post(self, request):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно добавлен')
        else:
            messages.error(request, 'Ошибка при добавлении статуса')
        return redirect('dictionaries')


class StatusUpdateView(View):
    def post(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно обновлен')
        else:
            messages.error(request, 'Ошибка при обновлении статуса')
        return redirect('dictionaries')


class StatusDeleteView(View):
    def post(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        try:
            status.delete()
            messages.success(request, 'Статус успешно удален')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении статуса: {str(e)}')
        return redirect('dictionaries')


# Представления для управления типами
class TypeCreateView(View):
    def post(self, request):
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип успешно добавлен')
        else:
            messages.error(request, 'Ошибка при добавлении типа')
        return redirect('dictionaries')


class TypeUpdateView(View):
    def post(self, request, pk):
        type_obj = get_object_or_404(Type, pk=pk)
        form = TypeForm(request.POST, instance=type_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип успешно обновлен')
        else:
            messages.error(request, 'Ошибка при обновлении типа')
        return redirect('dictionaries')


class TypeDeleteView(View):
    def post(self, request, pk):
        type_obj = get_object_or_404(Type, pk=pk)
        try:
            type_obj.delete()
            messages.success(request, 'Тип успешно удален')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении типа: {str(e)}')
        return redirect('dictionaries')


# Представления для управления категориями
class CategoryCreateView(View):
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно добавлена')
        else:
            messages.error(request, 'Ошибка при добавлении категории')
        return redirect('dictionaries')


class CategoryUpdateView(View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно обновлена')
        else:
            messages.error(request, 'Ошибка при обновлении категории')
        return redirect('dictionaries')


class CategoryDeleteView(View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        try:
            category.delete()
            messages.success(request, 'Категория успешно удалена')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении категории: {str(e)}')
        return redirect('dictionaries')


# Представления для управления подкатегориями
class SubcategoryCreateView(View):
    def post(self, request):
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подкатегория успешно добавлена')
        else:
            messages.error(request, 'Ошибка при добавлении подкатегории')
        return redirect('dictionaries')


class SubcategoryUpdateView(View):
    def post(self, request, pk):
        subcategory = get_object_or_404(Subcategory, pk=pk)
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подкатегория успешно обновлена')
        else:
            messages.error(request, 'Ошибка при обновлении подкатегории')
        return redirect('dictionaries')


class SubcategoryDeleteView(View):
    def post(self, request, pk):
        subcategory = get_object_or_404(Subcategory, pk=pk)
        try:
            subcategory.delete()
            messages.success(request, 'Подкатегория успешно удалена')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении подкатегории: {str(e)}')
        return redirect('dictionaries')


# API для динамической фильтрации категорий и подкатегорий
def get_categories_by_type(request):
    type_id = request.GET.get('type_id')
    categories = []

    if type_id:
        categories = Category.objects.filter(type_id=type_id).values('id', 'name')

    return JsonResponse(list(categories), safe=False)


def get_subcategories_by_category(request):
    category_id = request.GET.get('category_id')
    subcategories = []

    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')

    return JsonResponse(list(subcategories), safe=False)
