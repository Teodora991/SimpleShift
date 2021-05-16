import notifications.urls
from django.contrib import admin
from django.urls import path, include
from shifts.views import (SignupView, ActivateAccount,
                          EmployeeCreateView,
                          EmployeeListView,
                          EmployeeDetailView,
                          EmployeeUpdateView,
                          EmployeeDeleteView,
                          activate_admin,
                          activate_employee,
                          JobListView,
                          JobDeleteView,
                          JobUpdateView,
                          JobCreateView,
                          JobDetailView,)
from .views import HomePageView
from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="SimpleShift API",
      default_version='v1',
      description="API for manipulating employee shifts.",
      license=openapi.License(name="NoName License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('shifts/', include('shifts.urls', namespace='shifts')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('reset_password/', PasswordResetView.as_view(), name='reset_password'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('<int:pk>/activate_admin/', activate_admin, name="activate_admin"),
    path('<int:pk>/activate_employee/', activate_employee, name="activate_employee"),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('jobs/create/', JobCreateView.as_view(), name='job_create'),
    path('jobs/', JobListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('jobs/<int:pk>/update/', JobUpdateView.as_view(), name='job_update'),
    path('jobs/<int:pk>/delete/', JobDeleteView.as_view(), name='job_delete'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

