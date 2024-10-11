from datetime import timezone
from dateutil import parser as date_parse

import pytest

from truthbrush.api import Api


@pytest.fixture(scope="module")
def client():
    return Api()


def as_datetime(date_str):
    """Datetime formatter function. Ensures timezone is UTC. Consider moving to Api class."""
    return date_parse.parse(date_str).replace(tzinfo=timezone.utc)


def test_lookup_user(client):
    user = client.lookup(user_handle="realDonaldTrump")
    assert isinstance(user, dict)
    assert list(user.keys()) == [
        'id',
        'username',
        'acct',
        'display_name',
        'locked',
        'bot',
        'discoverable',
        'group',
        'created_at',
        'note',
        'url',
        'avatar',
        'avatar_static',
        'header',
        'header_static',
        'followers_count',
        'following_count',
        'statuses_count',
        'last_status_at',
        'verified',
        'location',
        'website',
        'accepting_messages',
        'chats_onboarded',
        'feeds_onboarded',
        'tv_onboarded',
        'show_nonmember_group_statuses',
        'pleroma',
        'tv_account',
        'receive_only_follow_mentions',
        'emojis',
        'fields'
    ]
    assert isinstance(user["id"], str)


#
# PULL STATUSES
#

@pytest.fixture(scope="module")
def user_timeline(client):
    return list(
        client.pull_statuses(username="truthsocial", replies=False, verbose=True)
    )

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



#
# TAGS / TOPICS
#

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
        "url"
    ]

    # the tag name is displayed on the trending page:
    assert isinstance(tag["name"], str)
    assert isinstance(tag["url"], str)
    assert tag["url"] == f"https://truthsocial.com/tags/{tag['name']}"

    # the number of recent statuses is displayed on the website:
    assert isinstance(tag["recent_statuses_count"], int)

    # a history of how the tag has trended day by day, over the past week:
    assert isinstance(tag["history"], list) # of dict
    #>[
    #>{'accounts': '1453', 'day': '1721606400', 'days_ago': 0, 'uses': '4272'},
    #>{'accounts': '860', 'day': '1721520000', 'days_ago': 1, 'uses': '2277'},
    #>{'accounts': '981', 'day': '1721433600', 'days_ago': 2, 'uses': '2548'},
    #>{'accounts': '1255', 'day': '1721347200', 'days_ago': 3, 'uses': '3373'},
    #>{'accounts': '1058', 'day': '1721260800', 'days_ago': 4, 'uses': '2995'},
    #>{'accounts': '1039', 'day': '1721174400', 'days_ago': 5, 'uses': '2978'},
    #>{'accounts': '1489', 'day': '1721088000', 'days_ago': 6, 'uses': '3907'}
    #>]
    # looks like they are in reverse chronological order

    assert isinstance(tag["recent_history"], list) # of int
    # [1489, 1039, 1058, 1255, 981, 860, 1453]
    # looks like they go in chronological order, starting with 6 days ago
