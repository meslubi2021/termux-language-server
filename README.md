# termux-language-server

[![readthedocs](https://shields.io/readthedocs/termux-language-server)](https://termux-language-server.readthedocs.io)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/termux/termux-language-server/main.svg)](https://results.pre-commit.ci/latest/github/termux/termux-language-server/main)
[![github/workflow](https://github.com/termux/termux-language-server/actions/workflows/main.yml/badge.svg)](https://github.com/termux/termux-language-server/actions)
[![codecov](https://codecov.io/gh/termux/termux-language-server/branch/main/graph/badge.svg)](https://codecov.io/gh/termux/termux-language-server)
[![DeepSource](https://deepsource.io/gh/termux/termux-language-server.svg/?show_trend=true)](https://deepsource.io/gh/termux/termux-language-server)

[![github/downloads](https://shields.io/github/downloads/termux/termux-language-server/total)](https://github.com/termux/termux-language-server/releases)
[![github/downloads/latest](https://shields.io/github/downloads/termux/termux-language-server/latest/total)](https://github.com/termux/termux-language-server/releases/latest)
[![github/issues](https://shields.io/github/issues/termux/termux-language-server)](https://github.com/termux/termux-language-server/issues)
[![github/issues-closed](https://shields.io/github/issues-closed/termux/termux-language-server)](https://github.com/termux/termux-language-server/issues?q=is%3Aissue+is%3Aclosed)
[![github/issues-pr](https://shields.io/github/issues-pr/termux/termux-language-server)](https://github.com/termux/termux-language-server/pulls)
[![github/issues-pr-closed](https://shields.io/github/issues-pr-closed/termux/termux-language-server)](https://github.com/termux/termux-language-server/pulls?q=is%3Apr+is%3Aclosed)
[![github/discussions](https://shields.io/github/discussions/termux/termux-language-server)](https://github.com/termux/termux-language-server/discussions)
[![github/milestones](https://shields.io/github/milestones/all/termux/termux-language-server)](https://github.com/termux/termux-language-server/milestones)
[![github/forks](https://shields.io/github/forks/termux/termux-language-server)](https://github.com/termux/termux-language-server/network/members)
[![github/stars](https://shields.io/github/stars/termux/termux-language-server)](https://github.com/termux/termux-language-server/stargazers)
[![github/watchers](https://shields.io/github/watchers/termux/termux-language-server)](https://github.com/termux/termux-language-server/watchers)
[![github/contributors](https://shields.io/github/contributors/termux/termux-language-server)](https://github.com/termux/termux-language-server/graphs/contributors)
[![github/commit-activity](https://shields.io/github/commit-activity/w/termux/termux-language-server)](https://github.com/termux/termux-language-server/graphs/commit-activity)
[![github/last-commit](https://shields.io/github/last-commit/termux/termux-language-server)](https://github.com/termux/termux-language-server/commits)
[![github/release-date](https://shields.io/github/release-date/termux/termux-language-server)](https://github.com/termux/termux-language-server/releases/latest)

[![github/license](https://shields.io/github/license/termux/termux-language-server)](https://github.com/termux/termux-language-server/blob/main/LICENSE)
[![github/languages](https://shields.io/github/languages/count/termux/termux-language-server)](https://github.com/termux/termux-language-server)
[![github/languages/top](https://shields.io/github/languages/top/termux/termux-language-server)](https://github.com/termux/termux-language-server)
[![github/directory-file-count](https://shields.io/github/directory-file-count/termux/termux-language-server)](https://github.com/termux/termux-language-server)
[![github/code-size](https://shields.io/github/languages/code-size/termux/termux-language-server)](https://github.com/termux/termux-language-server)
[![github/repo-size](https://shields.io/github/repo-size/termux/termux-language-server)](https://github.com/termux/termux-language-server)
[![github/v](https://shields.io/github/v/release/termux/termux-language-server)](https://github.com/termux/termux-language-server)

[![pypi/status](https://shields.io/pypi/status/termux-language-server)](https://pypi.org/project/termux-language-server/#description)
[![pypi/v](https://shields.io/pypi/v/termux-language-server)](https://pypi.org/project/termux-language-server/#history)
[![pypi/downloads](https://shields.io/pypi/dd/termux-language-server)](https://pypi.org/project/termux-language-server/#files)
[![pypi/format](https://shields.io/pypi/format/termux-language-server)](https://pypi.org/project/termux-language-server/#files)
[![pypi/implementation](https://shields.io/pypi/implementation/termux-language-server)](https://pypi.org/project/termux-language-server/#files)
[![pypi/pyversions](https://shields.io/pypi/pyversions/termux-language-server)](https://pypi.org/project/termux-language-server/#files)

Language server for
[termux](https://termux.dev)'s
[`build.sh`](https://github.com/termux/termux-packages/wiki/Creating-new-package)
and
[`*.subpackage.sh`](https://github.com/termux/termux-packages/wiki/Creating-new-package#writing-a-subpackage-script).

`build.sh` is a subtype of bash.
This language server only provides extra features for `build.sh` which
[bash-language-server](https://github.com/bash-lsp/bash-language-server)
doesn't support:

- [x] [Diagnostic](https://microsoft.github.io/language-server-protocol/specifications/specification-current#diagnostic):
  - [x] required variables. Such as: `TERMUX_PKG_VERSION`
  - [x] variable type. Such as: `TERMUX_PKG_DEPENDS` shouldn't be a function
  - [x] variable value. Such as: `TERMUX_PKG_AUTO_UPDATE` should be
  - [x] [variable order](https://github.com/termux/termux-packages/wiki/Creating-new-package#table-of-available-package-control-fields)
  - [x] unsorted comma separated value. Such as
    `TERMUX_PKG_RECOMMENDS="python-sentencepiece, python-numpy"`
    should be `TERMUX_PKG_RECOMMENDS="python-numpy, python-sentencepiece"`
    `true` or `false`
- [x] [Document Formatting](https://microsoft.github.io/language-server-protocol/specifications/specification-current#textDocument_formatting):
  - [x] sort some variables
  - [x] sort comma separated value
- [x] [Document Link](https://microsoft.github.io/language-server-protocol/specifications/specification-current#textDocument_documentLink):
  jump to
  <https://github.com/termux/termux-packages/tree/master/packages/package_name/build.sh>
- [x] [Hover](https://microsoft.github.io/language-server-protocol/specifications/specification-current#textDocument_hover)
- [x] [Completion](https://microsoft.github.io/language-server-protocol/specifications/specification-current#textDocument_completion):

Other features:

- [x] [pre-commit-hooks](https://pre-commit.com/)
  - [x] linter
  - [x] formatter

## Screenshots

### Diagnostic

![diagnostic](https://github.com/termux/termux-language-server/assets/32936898/598c371f-151d-442f-b782-e504a3d08872)

### Document Link

![document link](https://github.com/termux/termux-language-server/assets/32936898/9149386d-0e19-4f88-9931-dba8a3d960bc)

### Hover

![document hover](https://github.com/termux/termux-language-server/assets/32936898/5dfbe6d1-6bff-4ffd-bc8e-ad2c2895af52)

### Completion

![completion](https://github.com/termux/termux-language-server/assets/32936898/11f2bafc-cb3b-4559-9c3e-6df474e819bd)

Read
[![readthedocs](https://shields.io/readthedocs/termux-language-server)](https://termux-language-server.readthedocs.io)
to know more.

## Similar Projects

- [pkgbuild-language-server](https://github.com/Freed-Wu/pkgbuild-language-server):
  ArchLinux's `PKGBUILD`.
