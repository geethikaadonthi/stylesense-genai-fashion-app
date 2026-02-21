from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_healthcheck():
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_recommend():
    payload = {
        'style': 'casual',
        'occasion': 'Brunch',
        'weather': 'hot',
        'budget': 'mid-range'
    }
    response = client.post('/api/recommend', json=payload)
    assert response.status_code == 200
    body = response.json()
    assert 'styling_advice' in body
    assert len(body['outfit_recommendations']) >= 2
