def test_create_and_list_categories(client):
    payload = {"name": "Work"}
    r = client.post("/categories/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["name"] == "Work"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/categories/")
    assert r.status_code == 200
    categories = r.json()
    assert any(item["name"] == "Work" for item in categories)


def test_categories_pagination_and_sorting(client):
    for name in ["Beta", "Alpha", "Gamma"]:
        r = client.post("/categories/", json={"name": name})
        assert r.status_code == 201, r.text

    r = client.get("/categories/", params={"sort": "name"})
    assert r.status_code == 200
    assert [item["name"] for item in r.json()] == ["Alpha", "Beta", "Gamma"]

    r = client.get("/categories/", params={"sort": "-name"})
    assert r.status_code == 200
    assert [item["name"] for item in r.json()] == ["Gamma", "Beta", "Alpha"]

    r = client.get("/categories/", params={"sort": "name", "skip": 1, "limit": 1})
    assert r.status_code == 200
    assert [item["name"] for item in r.json()] == ["Beta"]


def test_create_note_with_category(client):
    category = client.post("/categories/", json={"name": "Personal"}).json()

    payload = {
        "title": "Category note",
        "content": "This note belongs to Personal",
        "category_id": category["id"],
    }
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    note = r.json()
    assert note["category_id"] == category["id"]
    assert note["category"]["name"] == "Personal"

    r = client.patch(f"/notes/{note['id']}", json={"category_id": category["id"]})
    assert r.status_code == 200
    patched = r.json()
    assert patched["category_id"] == category["id"]
    assert patched["category"]["name"] == "Personal"
