%define framework karchive

Name:           kf5-%{framework}
Version:        4.95.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 1 addon with archive functions

License:        GPLv2+
URL:            http://www.kde.org

Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  lzma-devel

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

%description
KDE Frameworks 5 Tier 1 addon with archive functions


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

make %{?_smp_mflags} DESTDIR=%{buildroot} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING COPYING.LIB INSTALL README.md
%{_kf5_libdir}/libKF5Archive.so.*

%files devel
%{_kf5_includedir}/karchive_version.h
%{_kf5_includedir}/KArchive
%{_kf5_libdir}/libKF5Archive.so
%{_kf5_libdir}/cmake/KF5Archive
%{_kf5_archdatadir}/mkspecs/modules/*.pri

%changelog
* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
