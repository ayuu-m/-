from django.urls import path
from . import views

urlpatterns = [
    # Основные маршруты
    path('', views.IndexView.as_view(), name='index'),
    path('cash-flow/create/', views.CashFlowCreateView.as_view(), name='cash_flow_create'),
    path('cash-flow/<int:pk>/update/', views.CashFlowUpdateView.as_view(), name='cash_flow_update'),
    path('cash-flow/<int:pk>/delete/', views.CashFlowDeleteView.as_view(), name='cash_flow_delete'),

    # Страница управления справочниками
    path('cash_flow_dictionaries/', views.DictionaryView.as_view(), name='dictionaries'),

    # API для динамической фильтрации
    path('api/categories-by-type/', views.get_categories_by_type, name='categories_by_type'),
    path('api/subcategories-by-category/', views.get_subcategories_by_category, name='subcategories_by_category'),

    # Управление статусами
    path('status/create/', views.StatusCreateView.as_view(), name='status_create'),
    path('status/<int:pk>/update/', views.StatusUpdateView.as_view(), name='status_update'),
    path('status/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),

    # Управление типами
    path('type/create/', views.TypeCreateView.as_view(), name='type_create'),
    path('type/<int:pk>/update/', views.TypeUpdateView.as_view(), name='type_update'),
    path('type/<int:pk>/delete/', views.TypeDeleteView.as_view(), name='type_delete'),

    # Управление категориями
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    # Управление подкатегориями
    path('subcategory/create/', views.SubcategoryCreateView.as_view(), name='subcategory_create'),
    path('subcategory/<int:pk>/update/', views.SubcategoryUpdateView.as_view(), name='subcategory_update'),
    path('subcategory/<int:pk>/delete/', views.SubcategoryDeleteView.as_view(), name='subcategory_delete'),
]
