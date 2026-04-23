import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app


class FakeCursor:
    def __init__(self):
        self.last_query = ""

    def execute(self, query, params=None):
        self.last_query = " ".join(query.split()).lower()

    def fetchone(self):
        return {"total": 3}

    def fetchall(self):
        if "from buses" in self.last_query and "join" not in self.last_query:
            return [{"bus_id": 1, "bus_number": "BUS-101", "capacity": 40}]
        if "from drivers" in self.last_query and "join" not in self.last_query:
            return [{"driver_id": 1, "name": "Ravi", "phone": "999", "license_no": "DL-1"}]
        if "from routes r" in self.last_query:
            return [{"route_id": 1, "route_name": "Route-A", "start_point": "A", "end_point": "B", "bus_number": "BUS-101", "driver_name": "Ravi"}]
        if "select route_id, route_name from routes" in self.last_query:
            return [{"route_id": 1, "route_name": "Route-A"}]
        if "from stops s join routes" in self.last_query:
            return [{"stop_id": 1, "stop_name": "Central", "area": "Zone 1", "route_name": "Route-A"}]
        if "select s.stop_id, s.stop_name, r.route_name" in self.last_query:
            return [{"stop_id": 1, "stop_name": "Central", "route_name": "Route-A"}]
        if "from students st" in self.last_query:
            return [{"student_id": 1, "student_name": "Ananya", "grade": "6", "phone": "999", "stop_name": "Central", "route_name": "Route-A", "bus_number": "BUS-101", "driver_name": "Ravi"}]
        if "count(st.student_id)" in self.last_query:
            return [{"route_name": "Route-A", "student_count": 1}]
        return []

    def close(self):
        return None


class FakeConnection:
    def cursor(self, dictionary=False):
        return FakeCursor()

    def commit(self):
        return None

    def close(self):
        return None


def _mock_conn():
    return FakeConnection()


def test_dashboard_page(monkeypatch):
    monkeypatch.setattr("app.get_connection", _mock_conn)
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_reports_page(monkeypatch):
    monkeypatch.setattr("app.get_connection", _mock_conn)
    client = app.test_client()
    response = client.get("/reports")
    assert response.status_code == 200
    assert b"Transport Reports" in response.data


def test_delete_requires_post(monkeypatch):
    monkeypatch.setattr("app.get_connection", _mock_conn)
    client = app.test_client()
    response = client.get("/delete/buses/1")
    assert response.status_code == 405
