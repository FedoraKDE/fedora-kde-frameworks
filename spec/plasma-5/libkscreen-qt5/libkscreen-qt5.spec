#%global git_version  4c5da6e
#%global git_date     20150112

%global base_name    libkscreen

Name:           libkscreen-qt5
Version:        5.2.95
Release:        1%{?dist}
Summary:        KDE display configuration library

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/libkscreen


# git archive --format=tar.gz --remote=git://anongit.kde.org/libkscreen.git \
#             --prefix=libkscreen-%%{version}/ --output=libkscreen-qt5-%%{git_version}.tar.gz %%{git_version}
#Source0:        libkscreen-%{git_version}.tar.gz

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{base_name}-%{version}.tar.xz

## upstreamable patches
## upstream patches

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXrandr-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

Requires:       kf5-filesystem

Provides:       kf5-kscreen%{?_isa} = %{version}-%{release}
Provides:       kf5-kscreen = %{version}-%{release}
Obsoletes:      kf5-kscreen% <= 1:5.1.95-2.beta


%description
LibKScreen is a library that provides access to current configuration
of connected displays and ways to change the configuration.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       kf5-kscreen-devel = %{version}-%{release}
Provides:       kf5-kscreen-devel%{?_isa} = %{version}-%{release}
Obsoletes:      kf5-kscreen-devel <= 1:5.1.95-2.beta

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{base_name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_kf5_libexecdir}/kscreen_backend_launcher
%{_kf5_libdir}/libKF5Screen.so.*
%{_kf5_plugindir}/kscreen/

%files devel
%{_kf5_includedir}/KScreen/
%{_kf5_includedir}/kscreen_version.h
%{_kf5_libdir}/libKF5Screen.so
%{_kf5_libdir}/cmake/KF5Screen/
%{_libdir}/pkgconfig/kscreen2.pc
%{_kf5_archdatadir}/mkspecs/modules/qt_KScreen.pri


%changelog
* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Wed Jan 28 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-2
- Fix Obsoletes

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0
  (new package, forked from libkscreen)
