#%define snapshot 20140205
%define framework sonnet

Name:           kf5-%{framework}
Version:        4.98.0
Release:        2.20140505gitc88e9e1b%{?dist}
Summary:        KDE Frameworks 5 Tier 1 solution for spell checking

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-sonnet-c88e9e1b.tar

BuildRequires:  libupnp-devel
BuildRequires:  systemd-devel
BuildRequires:  aspell-devel
BuildRequires:  hspell-devel
BuildRequires:  hunspell-devel
BuildRequires:  zlib-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-devel

Requires:       kf5-filesystem
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
%{_kf5_datadir}/kf5/sonnet/trigrams.map

%files ui
%{_kf5_libdir}/libKF5SonnetUi.so.*

%files devel
%{_kf5_includedir}/sonnet_version.h
%{_kf5_includedir}/SonnetCore
%{_kf5_includedir}/SonnetUi
%{_kf5_libdir}/libKF5SonnetCore.so
%{_kf5_libdir}/libKF5SonnetUi.so
%{_kf5_libdir}/cmake/KF5Sonnet
%{_kf5_archdatadir}/mkspecs/modules/qt_SonnetCore.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_SonnetUi.pri

%changelog
* Mon May 05 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140505gitc88e9e1b
- Update to git: c88e9e1b

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140428gitc4511767
- Update to git: c4511767

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428gitc4511767
- Update to git: c4511767

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422git8a2f8f77
- Update to git: 8a2f8f77

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git47dc1d66
- Update to git: 47dc1d66

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-release snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)
- split to -core and -ui subpackages

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
