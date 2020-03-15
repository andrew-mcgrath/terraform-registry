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

from chalice import Blueprint

from .config import *

bp = Blueprint(__name__)


@bp.route("/")
def list_all():
    """
    Lists all modules in the registry
    ref: https://www.terraform.io/docs/registry/api.html#list-modules
    """
    bp.current_request.uri_params["q"] = "*"
    return search()


@bp.route("/{namespace}")
def list_namespace(namespace):
    """
    Lists all modules in the given namespace
    ref: https://www.terraform.io/docs/registry/api.html#list-modules
    
    """
    bp.current_request.uri_params["q"] = "*"
    bp.current_request.uri_params["namespace"] = namespace
    return search()


@bp.route("/search")
def search():
    """
    Search for modules in the registry
    ref: https://www.terraform.io/docs/registry/api.html#search-modules
    """
    q = bp.current_request.query_params["q"]

    # Optional
    offset = bp.current_request.query_params.get("offset", 0)
    limit = bp.current_request.query_params.get("limit", ZAE_TFR_LIMIT)
    provider = bp.current_request.query_params.get("provider", None)
    verified = bp.current_request.query_params.get("verified", None)
    namespace = bp.current_request.query_params.get("namespace", None)

    return {}


@bp.route("/{namespace}/{name}")
def list_latest_all_providers(namespace, name):
    """
    List Latest Version of Module for All Providers
    ref: https://www.terraform.io/docs/registry/api.html#list-latest-version-of-module-for-all-providers
    """
    # Optional
    offset = bp.current_request.uri_params.get("offset", 0)
    limit = bp.current_request.uri_params.get("limit", ZAE_TFR_LIMIT)
    return {}


@bp.route("/{namespace}/{name}/{provider}")
def list_latest(namespace, name, provider):
    """
    Latest Version for a Specific Module Provider
    ref: https://www.terraform.io/docs/registry/api.html#latest-version-for-a-specific-module-provider
    """
    return {}


@bp.route("/{namespace}/{name}/{provider}/versions")
def list_versions(namespace, name, provider):
    """
    List Available Versions for a Specific Module
    ref: https://www.terraform.io/docs/registry/api.html#list-available-versions-for-a-specific-module
    """
    return {}


@bp.route("/{namespace}/{name}/{provider}/{version}")
def get_module(namespace, name, provider, version):
    """
    Get a Specific Module
    ref: https://www.terraform.io/docs/registry/api.html#get-a-specific-module
    """

    return {}


@bp.route("/{namespace}/{name}/{provider}/download")
def download_latest(namespace, name, provider):
    """
    Download the Latest Version of a Module
    ref: https://www.terraform.io/docs/registry/api.html#download-the-latest-version-of-a-module

    :param namespace:
    :param name:
    :param provider:
    :return:
    """
    return {}


@bp.route("/{namespace}/{name}/{provider}/{version}/download")
def download(namespace, name, provider, version):
    """
    Download Source Code for a Specific Module Version
    ref: https://www.terraform.io/docs/registry/api.html#download-source-code-for-a-specific-module-version
    """
    return {}