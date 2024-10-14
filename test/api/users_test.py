def test_lookup_user(client):

    user = client.lookup(user_handle="realDonaldTrump")
    assert isinstance(user, dict)
    assert isinstance(user["id"], str)

    expected_attributes = [
        "accepting_messages",
        "acct",
        "avatar",
        "avatar_static",
        "bot",
        "chats_onboarded",
        "created_at",
        "discoverable",
        "display_name",
        "emojis",
        "feeds_onboarded",
        "fields",
        "followers_count",
        "following_count",
        "group",
        "header",
        "header_static",
        "id",
        "last_status_at",
        "location",
        "locked",
        "note",
        "pleroma",
        "receive_only_follow_mentions",
        "show_nonmember_group_statuses",
        "statuses_count",
        "tv_account",
        "tv_onboarded",
        "url",
        "username",
        "verified",
        "website",
    ]
    assert sorted(list(user.keys())) == expected_attributes
