%define framework kdoctools

Name:           kf5-%{framework}
Version:        4.95.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 2 addon for documentation

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  libxslt-devel
BuildRequires:  libxml2-devel
BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-karchive-devel

Requires:       docbook-dtds
Requires:       docbook-style-xsl

%description
Provides tools to generate documentation in various format from DocBook files.


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
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING.LIB README.md
%{_kf5_bindir}/checkXML
%{_kf5_bindir}/meinproc5
%{_kf5_libdir}/libKF5XsltKde.a
%{_kf5_datadir}/ksgmltools2/customization/*
%{_kf5_datadir}/man/*


%files devel
%{_kf5_includedir}/XsltKde/*
%{_kf5_libdir}/cmake/KF5DocTools

%changelog
* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Tue Jan  7 2014 Daniel Vrátil <dvratil@redhat.com>
- add docboox-style-xsl to Requires

* Tue Jan  7 2014 Daniel Vrátil <dvratil@redhat.com>
- add docbook-dtds to Requries, needed for meinproc to actually work

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
