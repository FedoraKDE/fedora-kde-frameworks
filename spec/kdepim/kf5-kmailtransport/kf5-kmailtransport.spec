%global framework kmailtransport
%global git_rev   4103dc

Name:           kf5-%{framework}
Version:        15.08.0
Release:        0.1.git%{git_rev}%{?dist}
Summary:        The KMailTransport Library

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/pim/%{framework}

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
#Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz
Source0:        %{framework}-%{git_rev}.tar.gz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  cyrus-sasl-devel

BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kwallet-devel

BuildRequires:  kf5-kmime-devel
BuildRequires:  kf5-akonadi-devel
BuildRequires:  kf5-akonadi-mime-devel

Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kwallet-devel
Requires:       kf5-kmime-devel
Requires:       kf5-akonadi-mime-devel
Obsoletes:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      kdepimlibs-devel%{?_isa} < 15.08.0
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


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_kf5_libdir}/libKF5MailTransport.so.*

%files devel
%{_kf5_includedir}/kmailtransport_version.h
%{_kf5_includedir}/KMailTransport
%{_kf5_libdir}/libKF5MailTransport.so
%{_kf5_libdir}/cmake/KF5MailTransport
%{_kf5_archdatadir}/mkspecs/modules/qt_KMailTransport.pri


%changelog
* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-0.1.git4103dc
- Initial snapshot
