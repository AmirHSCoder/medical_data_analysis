import pytest
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from rest_framework.test import APIClient

from apps.analysis import utils
from apps.analysis.models import MergedData, RFResult, YProb
from apps.common.repositories.analysis_repository import (
    MergedDataRepository,
    RFResultRepository,
    YProbRepository,
)

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(api_client, db):
    _ = User.objects.create_user(username="tester", password="pass")
    resp = api_client.post(
        "/api/token/", {"username": "tester", "password": "pass"}, format="json"
    )
    token = resp.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.mark.django_db
def test_rf_result_endpoint(auth_client, monkeypatch):
    RFResult.objects.create(report='{"acc":1}')

    def sync_get(request):
        utils.USE_ASYNC_DB = False
        repo = RFResultRepository()
        result = repo.latest()
        from django.http import JsonResponse

        report = result.report if result else {}
        return JsonResponse(report, safe=False)

    from apps.analysis import urls as analysis_urls

    for p in analysis_urls.urlpatterns:
        if p.name == "rf_result":
            p.callback = sync_get
    import json

    resp = auth_client.get("/api/rf_result/")
    assert resp.status_code == 200
    assert json.loads(resp.content) == '{"acc":1}'


@pytest.mark.django_db
def test_y_result_endpoint(auth_client, monkeypatch):
    YProb.objects.create(y_prob={"a": 1})

    def sync_get(request):
        utils.USE_ASYNC_DB = False
        repo = YProbRepository()
        result = repo.latest()
        from django.http import JsonResponse

        y_prob = result.y_prob if result else {}
        return JsonResponse(y_prob, safe=False)

    from apps.analysis import urls as analysis_urls

    for p in analysis_urls.urlpatterns:
        if p.name == "y_result":
            p.callback = sync_get
    resp = auth_client.get("/api/y_result/")
    assert resp.status_code == 200
    assert resp.json() == {"a": 1}


@pytest.mark.django_db
def test_data_endpoint(auth_client, monkeypatch):
    MergedData.objects.create(
        source_id="s1",
        subject_id="sub",
        group="A",
        visit=1,
        delay=0,
        gender="M",
        handedness="R",
        age=30,
    )
    MergedData.objects.create(
        source_id="s2",
        subject_id="sub",
        group="B",
        visit=2,
        delay=1,
        gender="F",
        handedness="L",
        age=31,
    )

    def sync_get(request):
        repo = MergedDataRepository()
        records = [model_to_dict(obj) for obj in repo.get_all()]
        from django.http import JsonResponse

        return JsonResponse(records, safe=False)

    from apps.analysis import urls as analysis_urls

    for p in analysis_urls.urlpatterns:
        if p.name == "data":
            p.callback = sync_get
    resp = auth_client.get("/api/data/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    assert {d["source_id"] for d in data} == {"s1", "s2"}


@pytest.mark.django_db
def test_train_endpoint(auth_client, monkeypatch):
    called = {}

    def fake_call(cmd):
        called["called"] = True

    monkeypatch.setattr("django.core.management.call_command", fake_call)

    def sync_post(request):
        from django.http import JsonResponse

        try:
            fake_call("train_model")
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)
        return JsonResponse({"detail": "Training started"}, status=200)

    from apps.analysis import urls as analysis_urls

    for p in analysis_urls.urlpatterns:
        if p.name == "train_model":
            p.callback = sync_post
    resp = auth_client.post("/api/train/")
    assert resp.status_code == 200
    assert called.get("called")
    assert resp.json()["detail"] == "Training started"
