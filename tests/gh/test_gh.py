#  Copyright (c) 2020 Zero A.E., LLC
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
from http import HTTPStatus

import pytest
import requests
from pytest_chalice.handlers import RequestHandler

from chalicelib import gh


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture()
def gh_app_api() -> str:
    return "/gh"


def test_j2_can_find_template():
    from chalicelib.gh import j2

    assert j2.get_template("setup.html") is not None


def test_manifest(gh_app_api: str, client: RequestHandler):
    response = client.get(f"{gh_app_api}/")
    assert response.status_code == HTTPStatus.OK


def test_manifest_callback_invalid_nonce(gh_app_api: str, client: RequestHandler):
    response = client.get(f"{gh_app_api}/callback?state=xxx")
    assert response.status_code == HTTPStatus.EXPECTATION_FAILED


def test_manifest_callback(gh_app_api: str, client: RequestHandler, monkeypatch):
    class MockOKResponse:
        status_code = HTTPStatus.OK

        @staticmethod
        def json():
            # https://developer.github.com/apps/building-github-apps/creating-github-apps-from-a-manifest/#response
            import json

            return json.loads(
                """
                {
                    "id": 1,
                    "node_id": "MDM6QXBwNTk=",
                    "owner": {
                      "login": "octocat",
                      "id": 1,
                      "node_id": "MDQ6VXNlcjE=",
                      "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                      "gravatar_id": "",
                      "url": "https://api.github.com/users/octocat",
                      "html_url": "https://github.com/octocat",
                      "followers_url": "https://api.github.com/users/octocat/followers",
                      "following_url": "https://api.github.com/users/octocat/following{/other_user}",
                      "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
                      "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
                      "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
                      "organizations_url": "https://api.github.com/users/octocat/orgs",
                      "repos_url": "https://api.github.com/users/octocat/repos",
                      "events_url": "https://api.github.com/users/octocat/events{/privacy}",
                      "received_events_url": "https://api.github.com/users/octocat/received_events",
                      "type": "User",
                      "site_admin": false
                    },
                    "name": "octoapp",
                    "description": null,
                    "external_url": "https://www.example.com",
                    "html_url": "https://github.com/apps/octoapp",
                    "created_at": "2018-09-13T12:28:37Z",
                    "updated_at": "2018-09-13T12:28:37Z",
                    "client_id": "Iv1.8a61f9b3a7aba766",
                    "client_secret": "1726be1638095a19edd134c77bde3aa2ece1e5d8",
                    "webhook_secret": "e340154128314309424b7c8e90325147d99fdafa",
                    "pem": "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAuEPzOUE+kiEH1WLiMeBytTEF856j0hOVcSUSUkZxKvqczkWM\n9vo1gDyC7ZXhdH9fKh32aapba3RSsp4ke+giSmYTk2mGR538ShSDxh0OgpJmjiKP\nX0Bj4j5sFqfXuCtl9SkH4iueivv4R53ktqM+n6hk98l6hRwC39GVIblAh2lEM4L/\n6WvYwuQXPMM5OG2Ryh2tDZ1WS5RKfgq+9ksNJ5Q9UtqtqHkO+E63N5OK9sbzpUUm\noNaOl3udTlZD3A8iqwMPVxH4SxgATBPAc+bmjk6BMJ0qIzDcVGTrqrzUiywCTLma\nszdk8GjzXtPDmuBgNn+o6s02qVGpyydgEuqmTQIDAQABAoIBACL6AvkjQVVLn8kJ\ndBYznJJ4M8ECo+YEgaFwgAHODT0zRQCCgzd+Vxl4YwHmKV2Lr+y2s0drZt8GvYva\nKOK8NYYZyi15IlwFyRXmvvykF1UBpSXluYFDH7KaVroWMgRreHcIys5LqVSIb6Bo\ngDmK0yBLPp8qR29s2b7ScZRtLaqGJiX+j55rNzrZwxHkxFHyG9OG+u9IsBElcKCP\nkYCVE8ZdYexfnKOZbgn2kZB9qu0T/Mdvki8yk3I2bI6xYO24oQmhnT36qnqWoCBX\nNuCNsBQgpYZeZET8mEAUmo9d+ABmIHIvSs005agK8xRaP4+6jYgy6WwoejJRF5yd\nNBuF7aECgYEA50nZ4FiZYV0vcJDxFYeY3kYOvVuKn8OyW+2rg7JIQTremIjv8FkE\nZnwuF9ZRxgqLxUIfKKfzp/5l5LrycNoj2YKfHKnRejxRWXqG+ZETfxxlmlRns0QG\nJ4+BYL0CoanDSeA4fuyn4Bv7cy/03TDhfg/Uq0Aeg+hhcPE/vx3ebPsCgYEAy/Pv\neDLssOSdeyIxf0Brtocg6aPXIVaLdus+bXmLg77rJIFytAZmTTW8SkkSczWtucI3\nFI1I6sei/8FdPzAl62/JDdlf7Wd9K7JIotY4TzT7Tm7QU7xpfLLYIP1bOFjN81rk\n77oOD4LsXcosB/U6s1blPJMZ6AlO2EKs10UuR1cCgYBipzuJ2ADEaOz9RLWwi0AH\nPza2Sj+c2epQD9ZivD7Zo/Sid3ZwvGeGF13JyR7kLEdmAkgsHUdu1rI7mAolXMaB\n1pdrsHureeLxGbRM6za3tzMXWv1Il7FQWoPC8ZwXvMOR1VQDv4nzq7vbbA8z8c+c\n57+8tALQHOTDOgQIzwK61QKBgERGVc0EJy4Uag+VY8J4m1ZQKBluqo7TfP6DQ7O8\nM5MX73maB/7yAX8pVO39RjrhJlYACRZNMbK+v/ckEQYdJSSKmGCVe0JrGYDuPtic\nI9+IGfSorf7KHPoMmMN6bPYQ7Gjh7a++tgRFTMEc8956Hnt4xGahy9NcglNtBpVN\n6G8jAoGBAMCh028pdzJa/xeBHLLaVB2sc0Fe7993WlsPmnVE779dAz7qMscOtXJK\nfgtriltLSSD6rTA9hUAsL/X62rY0wdXuNdijjBb/qvrx7CAV6i37NK1CjABNjsfG\nZM372Ac6zc1EqSrid2IjET1YqyIW2KGLI1R2xbQc98UGlt48OdWu\n-----END RSA PRIVATE KEY-----\n"
                }
            """
            )

    monkeypatch.setattr(gh, "_verify_nonce", lambda x: True)
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: MockOKResponse())

    response = client.get(f"{gh_app_api}/callback?state=mocked")

    assert response.status_code == HTTPStatus.OK
