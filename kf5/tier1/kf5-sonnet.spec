#%define snapshot 20140205
%define framework sonnet

Name:           kf5-%{framework}
Version:        4.96.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 1 solution for spell checking

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  libupnp-devel
BuildRequires:  systemd-devel
BuildRequires:  aspell-devel
BuildRequires:  hspell-devel
BuildRequires:  hunspell-devel
BuildRequires:  zlib-devel

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

Requires:       kf5-sonnet-core%{?_isa} = %{version}-%{release}
Requires:       kf5-sonnet-ui%{?_isa} = %{version}-%{release}

%description
KDE Frameworks 5 Tier 1 solution for spell checking


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        core
Summary:        Non-gui part of the Sonnet framework

%description    core
Non-gui part of the Sonnet framework provides low-level spell checking tools

%package        ui
Summary:        GUI part of the Sonnet framework
Requires:       kf5-sonnet-core%{?_isa} = %{version}-%{release}

%description    ui
GUI part of the Sonnet framework provides widgets with spell checking support.


%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING.LIB README.md

%files core
%{_kf5_libdir}/libKF5SonnetCore.so.*
%{_kf5_plugindir}/sonnet_clients
%{_kf5_datadir}/sonnet/trigrams.map

%files ui
%{_kf5_libdir}/libKF5SonnetUi.so.*

%files devel
%{_kf5_includedir}/sonnet_version.h
%{_kf5_includedir}/sonnet
%{_kf5_libdir}/libKF5SonnetCore.so
%{_kf5_libdir}/libKF5SonnetUi.so
%{_kf5_libdir}/cmake/KF5Sonnet
%{_kf5_archdatadir}/mkspecs/modules/qt_SonnetCore.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_SonnetUi.pri

%changelog
* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-release snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)
- split to -core and -ui subpackages

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
