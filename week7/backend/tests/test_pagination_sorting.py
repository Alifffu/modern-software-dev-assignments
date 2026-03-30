def test_notes_pagination_and_sorting_across_backend(client):
    titles = ["Zeta note", "Alpha note", "Delta note"]
    for title in titles:
        payload = {"title": title, "content": f"Content for {title}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201, r.text

    r = client.get("/notes/", params={"sort": "title"})
    assert r.status_code == 200
    assert [item["title"] for item in r.json()] == ["Alpha note", "Delta note", "Zeta note"]

    r = client.get("/notes/", params={"sort": "-title"})
    assert r.status_code == 200
    assert [item["title"] for item in r.json()] == ["Zeta note", "Delta note", "Alpha note"]

    r = client.get("/notes/", params={"sort": "title", "skip": 1, "limit": 1})
    assert r.status_code == 200
    assert [item["title"] for item in r.json()] == ["Delta note"]


def test_categories_pagination_and_sorting_across_backend(client):
    names = ["Zebra", "Alpha", "Kappa"]
    for name in names:
        r = client.post("/categories/", json={"name": name})
        assert r.status_code == 201, r.text

    r = client.get("/categories/", params={"sort": "name"})
    assert r.status_code == 200
    assert [item["name"] for item in r.json()] == ["Alpha", "Kappa", "Zebra"]

    r = client.get("/categories/", params={"sort": "-name"})
    assert r.status_code == 200
    assert [item["name"] for item in r.json()] == ["Zebra", "Kappa", "Alpha"]

    r = client.get("/categories/", params={"sort": "name", "skip": 1, "limit": 1})
    assert r.status_code == 200
    assert [item["name"] for item in r.json()] == ["Kappa"]


def test_action_items_pagination_and_sorting_across_backend(client):
    descriptions = ["Beta task", "Alpha task", "Gamma task"]
    for description in descriptions:
        r = client.post("/action-items/", json={"description": description})
        assert r.status_code == 201, r.text

    r = client.get("/action-items/", params={"sort": "description"})
    assert r.status_code == 200
    assert [item["description"] for item in r.json()] == ["Alpha task", "Beta task", "Gamma task"]

    r = client.get("/action-items/", params={"sort": "-description"})
    assert r.status_code == 200
    assert [item["description"] for item in r.json()] == ["Gamma task", "Beta task", "Alpha task"]

    r = client.get("/action-items/", params={"sort": "description", "skip": 1, "limit": 1})
    assert r.status_code == 200
    assert [item["description"] for item in r.json()] == ["Beta task"]
