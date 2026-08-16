#!/usr/bin/env python3
"""Build the VPM listing described by source.json.

Every .zip attached to a release of a repository in the source's githubRepos is
downloaded; the ones carrying a package.json become listing entries, tagged with
their download URL and the SHA-256 of the zip. The rest of source.json is copied
to the listing as-is.

Usage: build-listing.py [source.json] [publish/listing.json]
"""

import hashlib
import json
import os
import re
import sys
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path

GITHUB_API = "https://api.github.com"


def fetch(url, token=None):
    """The bytes at url, with a GitHub token attached when one is given."""
    # VRChat's WAF rejects requests whose agent lacks a name, version and
    # contact, and GitHub requires an agent at all. This satisfies both.
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "vpm-listing/1.0 (+https://github.com/CassidyPrather/vpm)"},
    )
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request) as response:
        return response.read()


def release_zip_urls(repo, token):
    """Every .zip asset attached to any release of the owner/name repo."""
    urls = []
    page = 1
    while True:
        releases = json.loads(
            fetch(f"{GITHUB_API}/repos/{repo}/releases?per_page=100&page={page}", token)
        )
        if not releases:
            return urls
        for release in releases:
            urls += [
                asset["browser_download_url"]
                for asset in release["assets"]
                if asset["name"].endswith(".zip")
            ]
        page += 1


def package_from_zip(url):
    """The package.json inside the zip at url, or None if it holds none.

    Deliberately unauthenticated: a release download redirects to a pre-signed
    URL that rejects requests still carrying an Authorization header.
    """
    zip_bytes = fetch(url)
    with zipfile.ZipFile(BytesIO(zip_bytes)) as archive:
        if "package.json" not in archive.namelist():
            return None
        package = json.loads(archive.read("package.json"))
    package["url"] = url
    package["zipSHA256"] = hashlib.sha256(zip_bytes).hexdigest()
    return package


def version_key(version):
    """Sort key ordering 1.10.0 above 1.9.0, without a semver dependency.

    Every element is the same shape, so mixed numeric and textual versions stay
    comparable instead of raising.
    """
    return [
        (0, int(part), "") if part.isdigit() else (1, 0, part)
        for part in re.split(r"[.+-]", version)
    ]


def main():
    source_path = Path(sys.argv[1] if len(sys.argv) > 1 else "source.json")
    output_path = Path(sys.argv[2] if len(sys.argv) > 2 else "publish/listing.json")
    source = json.loads(source_path.read_text())
    token = os.environ.get("GITHUB_TOKEN")

    packages = {}
    for repo in source.get("githubRepos", []):
        for url in release_zip_urls(repo, token):
            package = package_from_zip(url)
            if package is None:
                print(f"no package.json in {url}, skipping")
                continue
            print(f"found {package['name']} {package['version']} in {url}")
            packages.setdefault(package["name"], {})[package["version"]] = package

    listing = {key: value for key, value in source.items() if key != "githubRepos"}
    listing["packages"] = {
        name: {
            "versions": {
                version: versions[version]
                for version in sorted(versions, key=version_key, reverse=True)
            }
        }
        for name, versions in sorted(packages.items())
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(listing, indent=2) + "\n")
    print(f"wrote {sum(len(v) for v in packages.values())} versions to {output_path}")


if __name__ == "__main__":
    main()
