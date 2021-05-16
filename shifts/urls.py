from django.urls import path
from .views import (ShiftCreateView,
                    ShiftListView,
                    ShiftDetailView,
                    ShiftDeleteView,
                    ShiftUpdateView,
                    apply_for_shift,
                    replace_request,
                    make_replacement,
                    assign_to_shift,
                    remove_shift_employee,
                    create_shift_evaluation,
                    ShiftEvaluationDetailView,
                    ShiftEvaluationUpdateView,
                    ShiftEvaluationDeleteView,
                    NotificationListView,
                    absence_report,
                    LiveShiftListView)


app_name = 'shifts'

urlpatterns = [
    path('create/', ShiftCreateView.as_view(), name='shift_create'),
    path('', ShiftListView.as_view(), name='shift_list'),
    path('<int:pk>/', ShiftDetailView.as_view(), name='shift_detail'),
    path('<int:pk>/delete', ShiftDeleteView.as_view(), name='shift_delete'),
    path('<int:pk>/update', ShiftUpdateView.as_view(), name='shift_update'),
    path('<int:pk>/apply', apply_for_shift, name='apply'),
    path('<int:pk>/assign/<int:employee_pk>', assign_to_shift, name='assign'),
    path('<int:pk>/<int:employee_pk>/remove', remove_shift_employee, name='remove_shift_employee'),
    path('<int:pk>/replace_request', replace_request, name='replace_request'),
    path('<int:pk>/<int:to_replace_pk>/make_replacement', make_replacement, name='make_replacement'),
    path('<int:pk>/absence_report', absence_report, name='absence_report'),
    path('<int:pk>/evaluation_create/', create_shift_evaluation, name='evaluation_create'),
    path('evaluation/<pk>/', ShiftEvaluationDetailView.as_view(), name='evaluation_detail'),
    path('evaluation/<pk>/update/', ShiftEvaluationUpdateView.as_view(), name='evaluation_update'),
    path('evaluation/<pk>/delete/', ShiftEvaluationDeleteView.as_view(), name='evaluation_delete'),
    path('notice/', NotificationListView.as_view(), name='notice'),
    path('live/', LiveShiftListView.as_view(), name='live_shifts'),
]
