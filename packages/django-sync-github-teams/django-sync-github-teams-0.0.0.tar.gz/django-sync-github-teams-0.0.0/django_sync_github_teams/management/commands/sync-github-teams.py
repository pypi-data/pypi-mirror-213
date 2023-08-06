# Copyright (C) 2023 Linaro Limited
#
# Author: Antonio Terceiro <antonio.terceiro@linaro.org>
#
# SPDX-License-Identifier: GPL-2.0-or-later


from django.core.management.base import BaseCommand
from django_sync_github_teams.sync import sync_github_teams


class Command(BaseCommand):
    help = "Sync GitHub teams as Django groups"

    def handle(self, *args, **options):
        sync_github_teams()
