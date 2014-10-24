%global git_date    20141024
%global git_commit  8a1c3ad

Name:           kfind
Version:        4.97.0
Release:        1.%{git_date}git%{git_commit}%{?dist}
Summary:        KDE Find File Utility

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar.gz --remote=git://anongit.kde.org/kde-baseapps.git \
#             --output=kde-baseapps-%%{git_commit}.tar.gz \
#             --prefix=kde-baseapps-%%{git_commit}/ %%{git_commit}
Source0:        kde-baseapps-%{git_commit}.tar.gz

BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kdelibs4support-devel

# unstable
BuildRequires:  kf5-konq-devel

Requires:       kf5-filesystem

%description
KFind allows you to search for directories and files.

%prep
%setup -q -n kde-baseapps-%{git_commit}

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ../kfind
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%files
%doc COPYING COPYING.DOC COPYING.LIB
%{_bindir}/kfind
%{_datadir}/applications/org.kde.kfind.desktop
%{_datadir}/appdata/kfind.appdata.xml
%{_datadir}/icons/hicolor/*/apps/kfind.png
%{_datadir}/doc/HTML/*/kfind
%{_datadir}/man/man1/kfind.1.gz

%changelog
* Fri Oct 24 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-1.20141024git8a1c3ad
- Initial version
