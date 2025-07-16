from django.urls import path
from .views import RFResultView, YProbView, DataView

urlpatterns = [
    path('rf_result/', RFResultView.as_view(), name='rf_result'),
    path('y_result/', YProbView.as_view(), name='y_result'),
    path('data/', DataView.as_view(), name='data'),
]
