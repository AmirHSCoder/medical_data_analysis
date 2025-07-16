from django.urls import path

from .views import DataView, RFResultView, TrainModelView, YProbView

urlpatterns = [
    path("rf_result/", RFResultView.as_view(), name="rf_result"),
    path("y_result/", YProbView.as_view(), name="y_result"),
    path("data/", DataView.as_view(), name="data"),
    path("train/", TrainModelView.as_view(), name="train_model"),
]
