from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, CategoryViewSet, CategoryExpenseView, DashboardView

router = DefaultRouter()
router.register("transactions", TransactionViewSet, basename="transactions")
router.register("categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("analytics/category-expenses/", CategoryExpenseView.as_view()),
    path("dashboard/", DashboardView.as_view()),
]



