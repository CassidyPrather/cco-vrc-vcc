# Cassidy's VPM Listing

A VRChat Creator Companion listing, published to <https://wirenook.net/vpm/listing.json>.

`source.json` is the whole configuration. Add a repository to `githubRepos` and every
release zip in it that contains a `package.json` is picked up. Pushing that change to
`main` rebuilds the listing and deploys it to GitHub Pages; `listing.json` is the only
file published.

The listing currently ships no packages.

## Legal

Copyright 2024 Cassidy Prather <pratherea@gmail.com>

Everything in this repository henceforth is licensed under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) (See `COPYING`) unless otherwise specified.

## Credits

Template files from https://github.com/vrchat-community/template-package-listing ([VRCHAT DISTRO LICENSE FILE](https://github.com/vrchat-community/template-package/blob/d9cf13fe9f56867cbf7315a4dbbf1901bc1537ec/Packages/com.vrchat.core.bootstrap/License.md))
