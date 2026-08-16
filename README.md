# Cassidy's VPM Listing

A VRChat Creator Companion listing, published to <https://wirenook.net/vpm/listing.json>.

`source.json` is the whole configuration: its contents become the listing, minus
`githubRepos`, plus the packages found there. Add a repository to `githubRepos` and
every release zip in it that contains a `package.json` is picked up. Pushing that
change to `main` rebuilds and deploys; `listing.json` is the only file published.

`build-listing.py` does the build, and runs anywhere Python 3 does:

```sh
python3 build-listing.py            # writes publish/listing.json
```

Set `GITHUB_TOKEN` to raise the API rate limit or to read a private repository.

The listing currently ships no packages.

## Legal

Copyright 2024 Cassidy Prather <pratherea@gmail.com>

Everything in this repository henceforth is licensed under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) (See `COPYING`) unless otherwise specified.

## Credits

Descended from https://github.com/vrchat-community/template-package-listing ([VRCHAT DISTRO LICENSE FILE](https://github.com/vrchat-community/template-package/blob/d9cf13fe9f56867cbf7315a4dbbf1901bc1537ec/Packages/com.vrchat.core.bootstrap/License.md))
