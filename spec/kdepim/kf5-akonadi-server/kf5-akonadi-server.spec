%global framework akonadi-server
%global git_rev   f91c2b

# base pkg default to SQLITE now, install -mysql if you want that instead
%global database_backend SQLITE

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

%global mysql mysql
%if 0%{?rhel} > 6
# el7 mariadb pkgs don't have compat Provides: mysql (apparently?)
%global mysql mariadb
%endif

Name:           kf5-%{framework}
Summary:        PIM Storage Service
Version:        15.08.0
Release:        0.1.git%{git_rev}%{?dist}

License:        LGPLv2+
URL:            https://projects.kde.org/packages/kde/pim/akonadi

Source0:        akonadi-server-%{git_rev}.tar.gz
## mysql config
Source10:       akonadiserverrc.mysql

## upstreamable patches

## upstream patches

%define mysql_conf_timestamp 20140709

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel

# for xsltproc
BuildRequires:  libxslt
BuildRequires:  pkgconfig(shared-mime-info)
BuildRequires:  pkgconfig(sqlite3) >= 3.6.23

# backends, used at buildtime to query known locations of server binaries
# FIXME/TODO: set these via cmake directives, avoids needless buildroot items
BuildRequires:  mariadb-server
BuildRequires:  postgresql-server

Requires:       kf5-filesystem

Requires(postun): /sbin/ldconfig

Conflicts:      akonadi < 15.08.0

%description
%{summary}.

%package devel
Summary:        Developer files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Conflicts:      akonadi-devel < 15.08.0
%description devel
%{summary}.

%package mysql
Summary:        Akonadi MySQL backend support
# upgrade path
Obsoletes:      akonadi < 1.7.90-2
Obsoletes:      akonadi-mysql < 15.08.0
Conflicts:      akonadi-mysql < 15.08.0
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{mysql}-server
%if "%{?mysql}" != "mariadb" && 0%{?fedora} > 20
Recommends:     mariadb-server
%endif
Requires:       qt5-qtbase-mysql%{?_isa}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%description mysql
Configures akonadi to use mysql backend by default.

Requires an available instance of mysql server at runtime.
Akonadi can spawn a per-user one automatically if the mysql-server
package is installed on the machine.
See also: %{_sysconfdir}/akonadi/mysql-global.conf



%prep
%setup -q -n %{framework}-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. \
  %{?database_backend:-DDATABASE_BACKEND=%{database_backend}} \
  -DINSTALL_QSQLITE_IN_QT_PREFIX:BOOL=ON
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

install -p -m644 -D %{SOURCE10} %{buildroot}%{_sysconfdir}/xdg/akonadi/akonadiserverrc.mysql

mkdir -p %{buildroot}%{_datadir}/akonadi/agents

touch -d %{mysql_conf_timestamp} \
  %{buildroot}%{_sysconfdir}/xdg/akonadi/mysql-global*.conf \
  %{buildroot}%{_sysconfdir}/xdg/akonadi/mysql-local.conf

# create/own %{_kf5_libdir}/akonadi
mkdir -p %{buildroot}%{_kf5_libdir}/akonadi

# %%ghost'd global akonadiserverrc
touch akonadiserverrc
install -p -m644 -D akonadiserverrc %{buildroot}%{_sysconfdir}/xdg/akonadi/akonadiserverrc

## unpackaged files
# omit mysql-global-mobile.conf
rm -fv %{buildroot}%{_sysconfdir}/xdg/akonadi/mysql-global-mobile.conf

%post
/sbin/ldconfig
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%posttrans
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%postun
/sbin/ldconfig ||:
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/mime/packages &> /dev/null || :
  update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null ||:
fi

%files
%doc AUTHORS README
%license lgpl-license
%dir %{_sysconfdir}/xdg/akonadi/
%ghost %config(missingok,noreplace) %{_sysconfdir}/xdg/akonadi/akonadiserverrc
%{_sysconfdir}/xdg/akonadi.categories
%{_kf5_bindir}/akonadi_agent_launcher
%{_kf5_bindir}/akonadi_agent_server
%{_kf5_bindir}/akonadi_control
%{_kf5_bindir}/akonadi_rds
%{_kf5_bindir}/akonadictl
%{_kf5_bindir}/akonadiserver
%{_kf5_libdir}/akonadi/
%{_kf5_libdir}/libKF5AkonadiPrivate.so.*
%{_kf5_datadir}/dbus-1/interfaces/org.freedesktop.Akonadi.*.xml
%{_kf5_datadir}/dbus-1/services/org.freedesktop.Akonadi.*.service
%{_kf5_datadir}/mime/packages/akonadi-mime.xml
%{_kf5_datadir}/akonadi/
%{_kf5_qtplugindir}/sqldrivers/libqsqlite3.so

%files devel
%{_kf5_bindir}/asapcat
%{_kf5_includedir}/akonadi/
%{_kf5_libdir}/libKF5AkonadiPrivate.so
%{_kf5_libdir}/cmake/KF5AkonadiServer/

%post mysql
%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/xdg/akonadi/akonadiserverrc \
  akonadiserverrc \
  %{_sysconfdir}/xdg/akonadi/akonadiserverrc.mysql \
  10

%postun mysql
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives \
  --remove akonadiserverrc \
  %{_sysconfdir}/xdg/akonadi/akonadiserverrc.mysql
fi

%files mysql
%config(noreplace) %{_sysconfdir}/xdg/akonadi/akonadiserverrc.mysql
%config(noreplace) %{_sysconfdir}/xdg/akonadi/mysql-global.conf
%config(noreplace) %{_sysconfdir}/xdg/akonadi/mysql-local.conf


%changelog
* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-0.1.gitf91c2b
- Initial snapshot
