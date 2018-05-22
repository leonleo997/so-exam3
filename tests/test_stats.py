import pytest
from op_stats.app import app
from op_stats.stats import Stats

@pytest.fixture
def client():
  client = app.test_client()
  return client

def test_get_cpu_percent(mocker, client):
  mocker.patch.object(Stats, 'get_cpu_percent', return_value=100)
  response = client.get('/CPU')
  assert response.data.decode('utf-8') == '{"Consumo de CPU: ": 100}'
  assert response.status_code == 200

def test_get_ram(mocker, client):
  mocker.patch.object(Stats, 'get_ram', return_value=10)
  response = client.get('/RAM')
  assert response.data.decode('utf-8') == '{"RAM disponible: ": 10}'
  assert response.status_code == 200

def test_get_disk(mocker, client):
  mocker.patch.object(Stats, 'get_disk', return_value=40)
  response = client.get('/DISK')
  assert response.data.decode('utf-8') == '{"Disco disponible: ": 40}'
  assert response.status_code == 200

