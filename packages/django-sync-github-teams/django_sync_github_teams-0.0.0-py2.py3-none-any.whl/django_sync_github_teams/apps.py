# Copyright (C) 2023 Linaro Limited
#
# Author: Antonio Terceiro <antonio.terceiro@linaro.org>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from django.apps import AppConfig


class DjangoSynGithubGroupsConfig(AppConfig):
    name = "django_sync_github_teams"
    verbose_name = "django_sync_github_teams"

    def ready(self):
        from . import sync

        sync
