%global framework akonadi-search
%global git_rev   2b42a3

Name:           kf5-%{framework}
Version:        15.08.0
Release:        0.1.git%{git_rev}%{?dist}
Summary:        The Akonadi Search Library

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

BuildRequires:  xapian-core-devel

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcrash-devel

BuildRequires:  kf5-akonadi-mime-devel
BuildRequires:  kf5-kcontacts-devel
BuildRequires:  kf5-kcalendarcore-devel
BuildRequires:  kf5-kmime-devel

Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel
Requires:       kf5-kcoreaddons-devel
Requires:       kf5-akonadi-devel
Requires:       kf5-akonadi-server-devel
Requires:       kf5-akonadi-mime-devel
Requires:       kf5-kcontacts-devel
Requires:       kf5-kmime-devel
Requires:       kf5-kcalendarcore-devel
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
%{_kf5_libdir}/libKF5AkonadiSearch.so.*

%files devel
%{_kf5_includedir}/akonadisearch_version.h
%{_kf5_includedir}/AkonadiSearch
%{_kf5_libdir}/libKF5AkonadiSearch.so
%{_kf5_libdir}/cmake/KF5AkonadiSearch
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiSearch.pri


%changelog
* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-0.1.git2b42a3
- Initial snapshot
