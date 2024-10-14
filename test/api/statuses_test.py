from truthbrush.utils import as_datetime


def test_pull_statuses(user_timeline):

    assert len(user_timeline) > 25  # more than one page

    # the posts are in reverse chronological order:
    latest, earliest = user_timeline[0], user_timeline[-1]
    latest_at = as_datetime(latest["created_at"])
    earliest_at = as_datetime(earliest["created_at"])
    assert earliest_at < latest_at

    # POST INFO
    # contains status info
    assert list(latest.keys()) == [
        "id",
        "created_at",
        "in_reply_to_id",
        "quote_id",
        "in_reply_to_account_id",
        "sensitive",
        "spoiler_text",
        "visibility",
        "language",
        "uri",
        "url",
        "content",
        "account",
        "media_attachments",
        "mentions",
        "tags",
        "card",
        "group",
        "quote",
        "in_reply_to",
        "reblog",
        "sponsored",
        "replies_count",
        "reblogs_count",
        "favourites_count",
        "favourited",
        "reblogged",
        "muted",
        "pinned",
        "bookmarked",
        "poll",
        "emojis",
        "_pulled",
    ]
    assert isinstance(latest["id"], str)


def test_pull_statuses_recent(client, user_timeline):
    username = "truthsocial"

    # COMPLETE PULLS

    # it fetches a timeline of the user's posts:
    assert len(user_timeline) > 25  # more than one page

    # the posts are in reverse chronological order:
    latest, earliest = user_timeline[0], user_timeline[-1]
    latest_at = as_datetime(latest["created_at"])
    earliest_at = as_datetime(earliest["created_at"])
    assert earliest_at < latest_at

    # EMPTY PULLS

    # can use created_after param for filtering out posts:
    next_pull = list(
        client.pull_statuses(
            username=username, replies=False, created_after=latest_at, verbose=True
        )
    )
    assert not any(next_pull)

    # can use since_id param for filtering out posts:
    next_pull = list(
        client.pull_statuses(
            username=username, replies=False, since_id=latest["id"], verbose=True
        )
    )
    assert not any(next_pull)

    # PARTIAL PULLS

    n_posts = 50  # two and a half pages worth, to verify everything is ok
    recent = user_timeline[n_posts]
    recent_at = as_datetime(recent["created_at"])

    # can use created_after param for filtering out posts:
    partial_pull = list(
        client.pull_statuses(
            username=username, replies=False, created_after=recent_at, verbose=True
        )
    )
    assert len(partial_pull) == n_posts
    assert recent["id"] not in [post["id"] for post in partial_pull]

    # can use since_id param for filtering out posts:
    partial_pull = list(
        client.pull_statuses(
            username=username, replies=False, since_id=recent["id"], verbose=True
        )
    )
    assert len(partial_pull) == n_posts
    assert recent["id"] not in [post["id"] for post in partial_pull]
