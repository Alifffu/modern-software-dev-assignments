def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_action_items_pagination_and_sorting(client):
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


