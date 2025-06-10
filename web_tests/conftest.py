# web_tests/conftest.py
import pytest

def pytest_addoption(parser):
    """Dodajemy opcje CLI do pytest dla integracji z Kiwi."""
    group = parser.getgroup("tcms")
    group.addoption(
        "--tcms-url",
        action="store",
        dest="tcms_url",
        help="URL do Kiwi TCMS (np. http://kiwi_web:8066)",
    )
    group.addoption(
        "--tcms-plan",
        action="store",
        dest="tcms_plan",
        help="ID planu testów w Kiwi TCMS",
    )
    group.addoption(
        "--tcms-build",
        action="store",
        dest="tcms_build",
        help="Numer bieżącego buildu (lub nazwa run) w Kiwi TCMS",
    )
    group.addoption(
        "--tcms-user",
        action="store",
        dest="tcms_user",
        help="Użytkownik Kiwi (np. tester)",
    )
    group.addoption(
        "--tcms-password",
        action="store",
        dest="tcms_password",
        help="Hasło do Kiwi",
    )
    group.addoption(
        "--tcms-insecure",
        action="store_true",
        dest="tcms_insecure",
        help="Wyłącz weryfikację SSL/TLS (jeśli używasz HTTPS z samopodpisanym cert.)",
    )

@pytest.fixture
def tcms_exec(request):
    """Inicjalizacja połączenia do Kiwi przez tcms_api."""
    from tcms_api import TCMS

    url = request.config.getoption("tcms_url")
    plan = request.config.getoption("tcms_plan")
    build = request.config.getoption("tcms_build")
    user = request.config.getoption("tcms_user")
    password = request.config.getoption("tcms_password")
    insecure = request.config.getoption("tcms_insecure")

    if insecure:
        import os
        os.environ["PYTHONHTTPSVERIFY"] = "0"

    rpc = TCMS(url, user, password).exec
    return {
        "rpc": rpc,
        "plan_id": plan,
        "build_id": build,
    }
