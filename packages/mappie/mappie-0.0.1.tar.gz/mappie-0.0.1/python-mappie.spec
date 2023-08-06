# SPDX-FileCopyrightText: 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# License text: https://spdx.org/licenses/MIT

Name:           python-mappie
Version:        0.0.1
Release:        1%{?dist}
Summary:        Python library with collections, frozen mappings, and more

License:        MIT
URL:            https://sr.ht/~gotmax23/mappie
%global furl    https://git.sr.ht/~gotmax23/mappie
Source0:        %{furl}/refs/download/v%{version}/mappie-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel

%global _description %{expand:
mappie is a python library with collections, frozen mappings, and more.}

%description %_description

%package -n python3-mappie
Summary:        %{summary}

%description -n python3-mappie %_description


%prep
%autosetup -p1 -n mappie-%{version}


%generate_buildrequires
%pyproject_buildrequires -x test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files mappie


%check
%pytest


%files -n python3-mappie -f %{pyproject_files}
%doc README.md
%license LICENSES/*


%changelog
* Tue Jun 13 2023 Maxwell G <maxwell@gtmx.me> - 0.0.1-1
- Release 0.0.1.
