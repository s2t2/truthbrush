

#def test_group_search(client):
#
#    group_name = "Make America Great Again"
#
#    results = list(client.search(searchtype="groups", query=group_name))
#
#    # are these different pages?
#    # should we return as a single list?
#    assert len(results) == 4 # why four pages?
#    # why do these have 20 (80 total) if the default limit is 40?
#    assert len(results[0]["groups"]) == 20
#    assert len(results[1]["groups"]) == 20
#    assert len(results[2]["groups"]) == 20
#    assert len(results[3]["groups"]) == 20
#
#    assert results[0]["groups"][0]["display_name"] == group_name
#


def test_group_search_simplified(client):
    group_name = "Make America Great Again"

    groups = client.search_simpler(resource_type="groups", query=group_name)
    matching_groups = [group for group in groups if group["display_name"] == group_name]
    assert len(matching_groups) == 1


def test_group_posts(client):
    group_id = "110228354005031735" # "Make America Great Again"

    timeline = client.group_posts(group_id)
    assert len(timeline) == 20
