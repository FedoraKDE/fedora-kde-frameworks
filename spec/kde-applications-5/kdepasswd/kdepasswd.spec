%global git_date    20141024
%global git_commit  8a1c3ad

Name:           kdepasswd
Version:        4.97.0
Release:        1.%{git_date}git%{git_commit}%{?dist}
Summary:        Changes your UNIX password

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
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-ki18n-devel

# unstable
BuildRequires:  kf5-konq-devel

Requires:       kf5-filesystem
Requires:       kio-extras

%description
This application allows you to change your UNIX password.

%prep
%setup -q -n kde-baseapps-%{git_commit}

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ../kdepasswd
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%files
%doc COPYING COPYING.DOC COPYING.LIB
%{_bindir}/kdepasswd
%{_datadir}/applications/org.kde.kdepasswd.desktop
%{_datadir}/doc/HTML/*/kdepasswd

%changelog
* Fri Oct 24 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-1.20141024git8a1c3ad
- Initial version
