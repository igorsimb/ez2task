from django.urls import path

from .views import (ItemListView,
                    ItemDetailView,
                    ItemCreateView,
                    ItemDeleteView,
                    MyTasksView,
                    ItemUpdateView,
                    IndexView,
                    CategoryCreateView,
                    CategoryDeleteView,
                    CategoryUpdateView,
                    CompanyCreateView,
                    CompanyUpdateView,
                    CommentDeleteView,
                    ManageUsersView,
                    )


urlpatterns = [
    path('', IndexView.as_view(), name='main'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),

    path('manage-tasks/', ItemListView.as_view(), name='manage_tasks'),
    path('manage_users/', ManageUsersView.as_view(), name='manage_users'),
    path('my-tasks/', MyTasksView.as_view(), name='my_tasks'),

    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),

    path('company/create/', CompanyCreateView.as_view(), name='company_create'),
    path('company/update/<int:pk>/', CompanyUpdateView.as_view(), name='company_update'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
]