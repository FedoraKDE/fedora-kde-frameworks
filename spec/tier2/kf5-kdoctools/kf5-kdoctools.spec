# %define snapshot  20140315
%define framework kdoctools

Name:           kf5-%{framework}
Version:        4.100.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 2 addon for documentation

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  libxslt-devel
BuildRequires:  libxml2-devel
BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-karchive-devel

Requires:       docbook-dtds
Requires:       docbook-style-xsl
Requires:       kf5-filesystem

%description
Provides tools to generate documentation in various format from DocBook files.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-karchive-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        User documentation and help for %{name}
%description    doc
Documentation and user help for %{name}.


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
%{_kf5_bindir}/checkXML5
%{_kf5_bindir}/meinproc5
%{_kf5_datadir}/man/*
%{_kf5_datadir}/kf5/kdoctools/customization


%files devel
%{_kf5_includedir}/XsltKde/*
%{_kf5_libdir}/libKF5XsltKde.a
%{_kf5_libdir}/cmake/KF5DocTools


%files doc
%{_kf5_docdir}/HTML/*/kdoctools5-common

%changelog
* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-1
- KDE Frameworks 4.100.0

* Sun May 18 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-3
- Apply upstream patch to improve error reporting in meinproc

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-1
- KDE Frameworks 4.99.0

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Sat Mar 15 2014 Jan Grulich <jgrulich@redhat.com 4.97.0-2
- pickup upstream patches

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-relase snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Tue Jan  7 2014 Daniel Vrátil <dvratil@redhat.com>
- add docboox-style-xsl to Requires

* Tue Jan  7 2014 Daniel Vrátil <dvratil@redhat.com>
- add docbook-dtds to Requries, needed for meinproc to actually work

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
