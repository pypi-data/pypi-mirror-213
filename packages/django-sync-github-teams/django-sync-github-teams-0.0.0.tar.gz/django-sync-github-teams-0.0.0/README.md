# django-sync-github-teams

django-sync-github-teams adds the ability to sync between Github teams and
groups in a Django application. It assumes and requires having users logging in
to the Django application using their GitHub accounts via [django-allauth][].
Check the django-allauth documentation for details on how to set it up.

[django-allauth]: https://django-allauth.readthedocs.io/en/latest/

## Installing and configuring

Install the package

```
pip install django-sync-github-teams
```

The in Django settings:

```python
INSTALLED_APPS = [
   ...
   "django_sync_github_teams",
   "allauth",
   "allauth.account",
   "allauth.socialaccount",
   ...
]

AUTH_SOCIALACCOUNT = {
	...
	"github": {
		"SCOPE": ["user"]
	},
	...
}

SYNC_GITHUB_TEAMS = ["myorg/myteam"]
SYNC_GITHUB_TEAMS_TOKEN = "*********************"
SYNC_GITHUB_TEAMS_ON_LOGIN = False
```

The follwing settings can be used:

* `SYNC_GITHUB_TEAMS`: list of strings containing the GitHub teams in the
  format `ORGANIZATION/TEAM` to be synced from GitHub. Each team listed will be
  synced to a local Django group with same name. Only users who have logged in
  locally using their GitHub accounts get added to the group.
* `SYNC_GITHUB_TEAMS_TOKEN`: string containing a GitHub API Personal access
  token to be used to read the team members. This token must have permissions
  to read the members of all of the teams listed in `SYNC_GITHUB_TEAMS`. See
  the [GitHub API documentation][] for more details about this.
* `SYNC_GITHUB_TEAMS_ON_LOGIN`: boolean; if set to True, a user's group will be
  populated when they login. This list of group is retrieved using the user's
  own credentials.

[GitHub API documentation]: https://docs.github.com/en/rest/teams/members?apiVersion=2022-11-28#list-team-members

## Usage

There's a management command to trigger the sync, which can be used in cronjobs
and the like:

```
./manage.py sync-github-teams
```

You can also trigger this in some other way from your application somehow:

```python
from django_sync_github_teams.sync import sync_github_teams

sync_github_teams()
```

This needs to run as often as your application requires. Note that even if you
enable syncing teams on login, you still need to sync them offline like this
from time to time, because users might leave the teams there where members of
when they first logged in.

## Contributing

Send merge requests at <https://gitlab.com/Linaro/django-sync-github-teams>.
Follow the existing coding conventions in the code (PEP-8, black), and make
sure the all the tests pass and that any new code is covered by tests. Just
running `make` will run all relevant tests.
