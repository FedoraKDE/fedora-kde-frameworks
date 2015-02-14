%define framework kpackage

Name:           kf5-%{framework}
Version:        5.7.0
Release:        3%{?dist}
Summary:        KDE Frameworks 5 Tier 2 library to load and install packages as plugins

License:        LGPLv2+
URL:            https://projects.kde.org/projects/frameworks/kpackage

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kdoctools-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 2 library to load and install non-binary packages as
if they were plugins.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kpackage5_qt --with-qt --with-man --all-name

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kpackage5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5Package.so.*
%{_kf5_bindir}/kpackagetool5
%{_kf5_datadir}/kservicetypes5/kpackage-packagestructure.desktop
%{_mandir}/man1/kpackagetool5.1.gz

%files devel
%{_kf5_includedir}/kpackage_version.h
%{_kf5_includedir}/KPackage
%{_kf5_libdir}/libKF5Package.so
%{_kf5_libdir}/cmake/KF5Package


%changelog
* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-1
- KDE Frameworks 5.7.0

* Tue Jan 06 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.0-1
- KDE Frameworks 5.6.0
