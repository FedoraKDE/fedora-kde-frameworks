%global git_date    20141024
%global git_commit  8a1c3ad

Name:           dolphin
Version:        4.97.0
Release:        1.%{git_date}git%{git_commit}%{?dist}
Summary:        KDE File Manager

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar.gz --remote=git://anongit.kde.org/kde-baseapps.git \
#             --output=kde-baseapps-%%{git_commit}.tar.gz \
#             --prefix=kde-baseapps-%%{git_commit}/ %%{git_commit}
Source0:        kde-baseapps-%{git_commit}.tar.gz

BuildRequires:  qt5-qtbase-devel

BuildRequires:  phonon-qt5-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kactivities-devel

# unstable
BuildRequires:  kf5-konq-devel
BuildRequires:  kf5-baloo-widgets-devel

# plasma-5
BuildRequires:  kf5-baloo-devel
BuildRequires:  kf5-kmetadata-devel

Requires:       kf5-filesystem
Requires:       kio-extras

%description
This package contains the default file manager of KDE.

%package        libs
Summary:        Dolphin runtime libraries
%description    libs
%{summary}.

%prep
%setup -q -n kde-baseapps-%{git_commit}

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ../dolphin
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

# Avoid -devel package
rm %{buildroot}/%{_libdir}/libdolphinprivate.so

%files
%doc COPYING COPYING.DOC COPYING.LIB
%{_bindir}/dolphin
%{_bindir}/servicemenuinstallation
%{_bindir}/servicemenudeinstallation
%{_kf5_qtplugindir}/dolphinpart.so
%{_kf5_qtplugindir}/kcm_*.so
%{_datadir}/dolphinpart/dolphinpart.rc
%{_datadir}/dolphin
%{_datadir}/applications/org.kde.dolphin.desktop
%{_datadir}/appdata/dolphin.appdata.xml
%{_datadir}/config.kcfg/*.kcfg
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_sysconfdir}/xdg/servicemenu.knsrc
%{_datadir}/doc/HTML/*/dolphin

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_libdir}/libdolphinprivate.so.*
%{_libdir}/libkdeinit5_dolphin.so


%changelog
* Tue Oct 07 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-20141024git8a1c3ad
- Initial version
