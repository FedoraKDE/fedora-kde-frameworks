%global framework akonadi-search

Name:           kf5-%{framework}
Version:        15.11.80
Release:        1%{?dist}
Summary:        The Akonadi Search library and indexing agent

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/pim/%{framework}

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/applications/%{version}/src/%{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  xapian-core-devel

BuildRequires:  kf5-ki18n-devel >= 5.15
BuildRequires:  kf5-kconfig-devel >= 5.15
BuildRequires:  kf5-kcrash-devel >= 5.15
BuildRequires:  kf5-krunner-devel >= 5.15
BuildRequires:  kf5-kcmutils-devel >= 5.15

BuildRequires:  kf5-akonadi-mime-devel >= 15.11.80
BuildRequires:  kf5-kcontacts-devel >= 15.11.80
BuildRequires:  kf5-kcalendarcore-devel >= 15.11.80
BuildRequires:  kf5-kmime-devel >= 15.11.80

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
%license COPYING COPYING.LIB
%{_sysconfdir}/xdg/akonadi-search.categories
%{_kf5_libdir}/libKF5AkonadiSearchPIM.so.*
%{_kf5_libdir}/libKF5AkonadiSearchCore.so.*
%{_kf5_libdir}/libKF5AkonadiSearchXapian.so.*
%{_kf5_libdir}/libKF5AkonadiSearchDebug.so.*

%{_kf5_bindir}/akonadi_indexing_agent
%{_kf5_datadir}/akonadi/agents/akonadiindexingagent.desktop
%{_kf5_datadir}/kservices5/plasma-krunner-pimcontacts.desktop
%{_kf5_datadir}/kservices5/plasma-krunner-pimcontacts_config.desktop
%{_kf5_qtplugindir}/akonadi/*.so
%{_kf5_qtplugindir}/kcm_krunner_pimcontacts.so
%{_kf5_qtplugindir}/krunner_pimcontacts.so

%files devel
%{_kf5_libdir}/libKF5AkonadiSearchPIM.so
%{_kf5_libdir}/libKF5AkonadiSearchCore.so
%{_kf5_libdir}/libKF5AkonadiSearchXapian.so
%{_kf5_libdir}/libKF5AkonadiSearchDebug.so
%{_kf5_includedir}/akonadi_search_version.h
%{_kf5_includedir}/AkonadiSearch
%{_kf5_libdir}/cmake/KF5AkonadiSearch


%changelog
* Thu Dec 03 2015 Jan Grulich <jgrulich@redhat.com> - 15.11.80-1
- Update to 15.11.80

* Mon Aug 24 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-1
- Initial version
