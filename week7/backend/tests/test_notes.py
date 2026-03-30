def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_notes_pagination_and_sorting(client):
    titles = ["Zebra note", "Alpha note", "Middle note"]
    for title in titles:
        payload = {"title": title, "content": f"Content for {title}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201, r.text

    r = client.get("/notes/", params={"sort": "title"})
    assert r.status_code == 200
    assert [item["title"] for item in r.json()] == ["Alpha note", "Middle note", "Zebra note"]

    r = client.get("/notes/", params={"sort": "-title"})
    assert r.status_code == 200
    assert [item["title"] for item in r.json()] == ["Zebra note", "Middle note", "Alpha note"]

    r = client.get("/notes/", params={"sort": "title", "skip": 1, "limit": 1})
    assert r.status_code == 200
    assert [item["title"] for item in r.json()] == ["Middle note"]


