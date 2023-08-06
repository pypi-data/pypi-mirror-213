# Copyright (C) 2023 Linaro Limited
#
# Author: Antonio Terceiro <antonio.terceiro@linaro.org>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import re
from django.contrib.auth.models import Group
from django.conf import settings
from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
import requests


def sync_github_teams_on_login(sender, **kwargs):
    user = kwargs["user"]
    if not SocialAccount.objects.filter(provider="github", user=user).exists():
        return
    sync_github_teams()


if getattr(settings, "SYNC_GITHUB_TEAMS_ON_LOGIN", False):
    user_logged_in.connect(sync_github_teams_on_login)  # pragma: no cover


def sync_github_teams():
    teams = settings.SYNC_GITHUB_TEAMS
    if not teams:
        return
    token = settings.SYNC_GITHUB_TEAMS_TOKEN
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    for item in teams:
        org, team = item.split("/")
        group, _ = Group.objects.get_or_create(name=team)
        endpoint = f"https://api.github.com/orgs/{org}/teams/{team}/members"
        account_ids = []
        while True:
            res = requests.get(
                endpoint,
                headers=headers,
            )
            res.raise_for_status()
            for acct in res.json():
                account_ids.append(acct["id"])
            endpoint = get_next_link(res.headers.get("link"))
            if not endpoint:
                break

        accounts = SocialAccount.objects.filter(provider="github", uid__in=account_ids)
        users = [acct.user for acct in accounts]
        group.user_set.set(users)


def get_next_link(link_str):
    if not link_str:
        return None
    matches = re.findall('<([^>]+)>; rel="next"', link_str)
    if matches:
        return matches[0]
    return None
