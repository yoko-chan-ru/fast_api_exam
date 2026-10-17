from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ==========================================
# ТЕСТЫ ДЛЯ ИСПОЛНИТЕЛЕЙ (ARTISTS)
# ==========================================

def test_create_artist():
    """Тест: Создание исполнителя"""
    response = client.post("/artists/", json={"name": "Linkin Park"})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "Linkin Park"

def test_get_artists():
    """Тест: Получение списка исполнителей"""
    response = client.get("/artists/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # Проверяем, что список не пустой

# ==========================================
# ТЕСТЫ ДЛЯ АЛЬБОМОВ (ALBUMS)
# ==========================================

def test_create_album():
    """Тест: Создание альбома для существующего исполнителя"""
    # Сначала создаем исполнителя, чтобы получить его ID
    artist_resp = client.post("/artists/", json={"name": "Nirvana"})
    artist_id = artist_resp.json()["id"]

    # Теперь создаем альбом
    response = client.post("/albums/", json={
        "title": "Nevermind",
        "year": 1991,
        "artist_id": artist_id
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Nevermind"
    assert data["artist_id"] == artist_id

def test_create_album_artist_not_found():
    """Тест: Попытка создать альбом для несуществующего исполнителя (404)"""
    response = client.post("/albums/", json={
        "title": "Фейковый альбом",
        "year": 2024,
        "artist_id": 9999  # Такого ID точно нет
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Исполнитель не найден"

def test_get_all_albums():
    """Тест: Получение всех альбомов"""
    response = client.get("/albums/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_album_by_id():
    """Тест: Получение одного альбома по ID"""
    # Создаем данные для теста
    artist_resp = client.post("/artists/", json={"name": "Metallica"})
    artist_id = artist_resp.json()["id"]
    
    album_resp = client.post("/albums/", json={
        "title": "Master of Puppets",
        "year": 1986,
        "artist_id": artist_id
    })
    album_id = album_resp.json()["id"]

    # Запрашиваем этот альбом
    response = client.get(f"/albums/{album_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Master of Puppets"

def test_get_album_not_found():
    """Тест: Запрос несуществующего альбома (404)"""
    response = client.get("/albums/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Альбом не найден"

def test_get_artist_with_albums():
    """Тест: Получение исполнителя вместе с его альбомами (вложенный ответ)"""
    # Создаем исполнителя и два его альбома
    artist_resp = client.post("/artists/", json={"name": "Queen"})
    artist_id = artist_resp.json()["id"]
    
    client.post("/albums/", json={"title": "A Night at the Opera", "year": 1975, "artist_id": artist_id})
    client.post("/albums/", json={"title": "News of the World", "year": 1977, "artist_id": artist_id})

    # Запрашиваем исполнителя
    response = client.get(f"/artists/{artist_id}/albums")
    assert response.status_code == 200
    data = response.json()
    
    # Проверяем, что вернулись данные исполнителя
    assert data["name"] == "Queen"
    # Проверяем, что альбомы вложились в ответ
    assert "albums" in data
    assert len(data["albums"]) == 2