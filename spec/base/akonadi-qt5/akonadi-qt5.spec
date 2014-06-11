##base pkg default to SQLITE now, install -mysql if you want that instead
# FIXME: Go back to SQLITE once it's available in Qt 5 build
%global database_backend MYSQL
%global snap f36fad6

Summary: PIM Storage Service (Qt 5 version)
Name:    akonadi-qt5
Version: 1.76.47
Release: 1%{?dist}

License: LGPLv2+
URL:     http://community.kde.org/KDE_PIM/Akonadi 
# git clone git://git.kde.org/akonadi
# git archive --prefix=akonadi-%{version}/ master | bzip2 > akonadi-%{version}-%{snap}.tar.bz2
Source0: akonadi-qt5-%{version}-%{snap}.tar.xz

## mysql config
Source10: akonadiserverrc.mysql

Patch0:   akonadi-qt5-coinstallable-libs.patch

## upstreamable patches

## upstream patches

%define mysql_conf_timestamp 20140514

BuildRequires: automoc4
BuildRequires: boost-devel
BuildRequires: cmake >= 2.8.8
# for xsltproc
BuildRequires: libxslt
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtbase-mysql
BuildRequires: qt5-qtbase-postgresql
BuildRequires: qt5-qtbase-odbc
BuildRequires: pkgconfig(shared-mime-info)
BuildRequires: pkgconfig(sqlite3) >= 3.6.23
# %%check
BuildRequires: dbus-x11 xorg-x11-server-Xvfb
# backends, used at buildtime to query known locations of server binaries
# FIXME/TODO: set these via cmake directives, avoids needless buildroot items
BuildRequires: mysql-server
BuildRequires: postgresql-server

Requires(postun): /sbin/ldconfig

# FIXME: Remove once we preffer SQLITE again
Requires:       akonadi-qt5-mysql
Provides:       akonadi = %{version}-%{release}
Provides:       akonadi%{?_isa} = %{version}-%{release}
Conflicts:      akonadi

%description
%{summary}.

%package devel
Summary: Developer files for %{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Conflicts: akonadi-devel
%description devel
%{summary}.

%package mysql
Summary: Akonadi MySQL backend support
# upgrade path
Obsoletes: akonadi < 1.7.90-2
Conflicts: akonadi-mysql
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: mysql-server
Requires: qt5-qtbase-mysql%{?_isa}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%description mysql
Configures Akonadi to use MySQL backend by default.

Requires an available instance of mysql server at runtime.
Akonadi can spawn a per-user one automatically if the mysql-server
package is installed on the machine.
See also: %{_sysconfdir}/akonadi/mysql-global.conf

%package libs
Summary: Shared Akonadi libraries
%description libs
Shared libraries used by both Akonadi Server and client libraries.



%prep
%setup -q -n akonadi-qt5-%{version}

%patch0 -p1 -b .coinstall

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{?cmake28}%{!?cmake28:%{?cmake}} \
  -DCONFIG_INSTALL_DIR=%{_sysconfdir} \
  %{?database_backend:-DDATABASE_BACKEND=%{database_backend}} \
  -DQT5_BUILD:BOOL=ON \
  -DINSTALL_QSQLITE_IN_QT_PREFIX:BOOL=ON \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

install -p -m644 -D %{SOURCE10} %{buildroot}%{_sysconfdir}/xdg/akonadi/akonadiserverrc.mysql

mkdir -p %{buildroot}%{_datadir}/akonadi/agents

touch -d %{mysql_conf_timestamp} \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-global*.conf \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-local.conf

# create/own %{_libdir}/akondi
mkdir -p %{buildroot}%{_libdir}/akonadi

# %%ghost'd global akonadiserverrc 
touch akonadiserverrc 
install -p -m644 -D akonadiserverrc %{buildroot}%{_sysconfdir}/xdg/akonadi/akonadiserverrc

## unpackaged files
# omit mysql-global-mobile.conf
rm -fv %{buildroot}%{_sysconfdir}/akonadi/mysql-global-mobile.conf


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion akonadi)" = "%{version}"

# FIXME: Don't run tests with Qt 5
# this one (still) fails in mock (local build ok):
# 14/14 Test #14: akonadi-dbconfigtest
#xvfb-run -a dbus-launch --exit-with-session make test -C %{_target_platform}  ||:


%post -p /sbin/ldconfig

%posttrans
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
/sbin/ldconfig ||:
if [ $1 -eq 0 ] ; then
  update-mime-database %{_datadir}/mime &> /dev/null ||:
fi

%files
%doc AUTHORS lgpl-license
%dir %{_sysconfdir}/xdg/akonadi/
%ghost %config(missingok,noreplace) %{_sysconfdir}/xdg/akonadi/akonadiserverrc
%dir %{_sysconfdir}/akonadi/
%{_bindir}/akonadi_agent_launcher
%{_bindir}/akonadi_agent_server
%{_bindir}/akonadi_control
%{_bindir}/akonadi_rds
%{_bindir}/akonadictl
%{_bindir}/akonadiserver
%{_libdir}/akonadi/
%{_datadir}/dbus-1/interfaces/org.freedesktop.Akonadi.*.xml
%{_datadir}/dbus-1/services/org.freedesktop.Akonadi.*.service
%{_datadir}/mime/packages/akonadi-mime.xml
%{_datadir}/akonadi/

%files libs
%{_libdir}/libakonadiprotocolinternalsqt5.so.1*

%files devel
%{_bindir}/asapcat
%{_includedir}/akonadi/
%{_libdir}/pkgconfig/akonadi.pc
%{_libdir}/libakonadiprotocolinternalsqt5.so
%{_libdir}/cmake/Akonadi/

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
%config(noreplace) %{_sysconfdir}/akonadi/mysql-global.conf
%config(noreplace) %{_sysconfdir}/akonadi/mysql-local.conf


%changelog
* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 1.76.47-1
- Update to latest upstream

* Sun May 18 2014 Daniel Vrátil <dvratil@redhat.com> - 1.73.44-2
- Fix deps

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 1.73.44-1
- Fork a Qt 5 version from Akonadi
