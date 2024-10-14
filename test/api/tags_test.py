def test_trending_tags(client):
    # it pulls a list of tags displayed on the topics tab of the search page:
    tags = client.tags()
    assert isinstance(tags, list)
    assert len(tags) == 20

    # each tag has a name and number of recent posts:
    tag = tags[0]
    assert isinstance(tag, dict)
    assert sorted(list(tag.keys())) == [
        "history",
        "name",
        "recent_history",
        "recent_statuses_count",
        "url",
    ]

    # the tag name is displayed on the trending page:
    assert isinstance(tag["name"], str)
    assert isinstance(tag["url"], str)
    assert tag["url"] == f"https://truthsocial.com/tags/{tag['name']}"

    # the number of recent statuses is displayed on the website:
    assert isinstance(tag["recent_statuses_count"], int)

    # a history of how the tag has trended day by day, over the past week:
    assert isinstance(tag["history"], list)  # of dict
    # >[
    # >{'accounts': '1453', 'day': '1721606400', 'days_ago': 0, 'uses': '4272'},
    # >{'accounts': '860', 'day': '1721520000', 'days_ago': 1, 'uses': '2277'},
    # >{'accounts': '981', 'day': '1721433600', 'days_ago': 2, 'uses': '2548'},
    # >{'accounts': '1255', 'day': '1721347200', 'days_ago': 3, 'uses': '3373'},
    # >{'accounts': '1058', 'day': '1721260800', 'days_ago': 4, 'uses': '2995'},
    # >{'accounts': '1039', 'day': '1721174400', 'days_ago': 5, 'uses': '2978'},
    # >{'accounts': '1489', 'day': '1721088000', 'days_ago': 6, 'uses': '3907'}
    # >]
    # looks like they are in reverse chronological order

    assert isinstance(tag["recent_history"], list)  # of int
    # [1489, 1039, 1058, 1255, 981, 860, 1453]
    # looks like they go in chronological order, starting with 6 days ago
