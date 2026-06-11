import pytest

from app.core.monitoring import reset_metrics
from app.modules.users.models import UserRole
from tests.users.helpers import AUTH_API, assert_detail_payload, auth_headers

MONITORING_API = "/api/v1/monitoring"


@pytest.mark.asyncio
async def test_metrics_endpoint_returns_prometheus_payload(client):
    reset_metrics()
    response = await client.get(f"{MONITORING_API}/metrics")

    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "app_users_total" in response.text
    assert "main_site_transitions_total" in response.text
    assert "/api/v1/monitoring/metrics" not in response.text


@pytest.mark.asyncio
async def test_metrics_ignore_service_monitors(client):
    reset_metrics()

    response = await client.get(
        f"{MONITORING_API}/grafana/login",
        headers={"User-Agent": "Zabbix"},
    )

    assert response.status_code == 200

    metrics_response = await client.get(f"{MONITORING_API}/metrics")

    assert metrics_response.status_code == 200
    assert "/api/v1/monitoring/grafana/login" not in metrics_response.text


@pytest.mark.asyncio
async def test_create_grafana_session_requires_admin(client):
    response = await client.post(f"{MONITORING_API}/grafana/session")

    assert response.status_code == 401
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_grafana_login_page_returns_html(client):
    response = await client.get(f"{MONITORING_API}/grafana/login")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Вход в Grafana" in response.text


@pytest.mark.asyncio
async def test_grafana_login_form_redirects_to_grafana(client, create_user):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )

    response = await client.post(
        f"{MONITORING_API}/grafana/login",
        data={
            "email": "admin@example.com",
            "password": "AdminPass123",
            "next_url": "/grafana/",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/grafana/"
    assert "grafana_session=" in response.headers.get("set-cookie", "")


@pytest.mark.asyncio
async def test_admin_can_create_and_clear_grafana_session(client, create_user):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    login_response = await client.post(
        f"{AUTH_API}/login",
        data={"username": "admin@example.com", "password": "AdminPass123"},
    )
    token = login_response.json()["access_token"]

    create_response = await client.post(
        f"{MONITORING_API}/grafana/session",
        headers=auth_headers(token),
    )

    assert create_response.status_code == 200
    assert create_response.json()["grafana_url"] == "/grafana/"
    cookie_header = create_response.headers.get("set-cookie", "")
    assert "grafana_session=" in cookie_header
    grafana_cookie = create_response.cookies.get("grafana_session")
    assert grafana_cookie

    auth_response = await client.get(
        f"{MONITORING_API}/grafana/auth",
        headers={"Cookie": f"grafana_session={grafana_cookie}"},
    )
    assert auth_response.status_code == 204
    assert auth_response.headers["x-grafana-user"]

    delete_response = await client.delete(f"{MONITORING_API}/grafana/session")
    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_metrics_include_business_counters(client, create_user):
    reset_metrics()
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    await create_user(
        email="superadmin@example.com",
        password="AdminPass123",
        role=UserRole.SUPERADMIN,
    )
    await client.post(
        "/api/v1/main-site-transitions",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    await client.post(
        "/api/v1/main-site-transitions",
        headers={
            "User-Agent": "Mozilla/5.0",
            "X-Forwarded-For": "203.0.113.10",
        },
    )

    response = await client.get(f"{MONITORING_API}/metrics")

    assert response.status_code == 200
    assert "app_users_total 2" in response.text
    assert "app_admin_users_total 1" in response.text
    assert "app_superadmin_users_total 1" in response.text
    assert "main_site_transitions_total 2" in response.text
    assert "main_site_transitions_unique_ip_total 2" in response.text


@pytest.mark.asyncio
async def test_metrics_include_subdistrict_view_metrics(client):
    reset_metrics()

    detail_response = await client.get("/api/v1/subdistricts/ШИННЫЙ")
    assert detail_response.status_code == 200

    metrics_response = await client.get(f"{MONITORING_API}/metrics")

    assert metrics_response.status_code == 200
    assert (
        'subdistrict_detail_views_total{subdistrict="ШИННЫЙ"} 1'
        in metrics_response.text
    )
    assert 'subdistrict_views_total{subdistrict="ШИННЫЙ"} 1' in metrics_response.text
