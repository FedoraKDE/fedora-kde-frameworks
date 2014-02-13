%global snapshot 20140213

Summary:        A Qt implementation of the DBusMenu protocol (Qt5 version)
Name:           dbusmenu-qt5
Version:        0.9.2
Release:        0.2.%{snapshot}bzr%{?dist}

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://launchpad.net/libdbusmenu-qt/

#Source0 :       https://launchpad.net/libdbusmenu-qt/trunk/%{version}/+download/libdbusmenu-qt-%{version}.tar.bz2
# bzr branch lp:libdbusmenu-qt && mv libdbusmenu-qt{,5-%{version}} && \
# tar -c libdbusmenu-qt5-0.9.2 | bzip2 -c > libdbusmenu-qt5-0.9.2-${snapshot}bzr.tar.bz2
Source0:        libdbusmenu-qt5-%{version}-%{snapshot}bzr.tar.bz2
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  qjson-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-filesystem

%description
This library provides a Qt implementation of the DBusMenu protocol.

The DBusMenu protocol makes it possible for applications to export and import
their menus over DBus.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
%{summary}.


%prep
%setup -q -n libdbusmenu-qt5-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} \
        -DUSE_QT4:BOOL=FALSE \
        -DUSE_QT5:BOOL=TRUE \
        -DWITH_DOC:BOOL=TRUE \
        ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# unpackaged files
rm -rf %{buildroot}%{_docdir}/dbusmenu-qt


%check
# verify pkg-config version
export PKG_CONFIG_PATH=%{buildroot}%{_kf5_datadir}/pkgconfig:%{buildroot}%{_kf5_libdir}/pkgconfig
test "$(pkg-config --modversion dbusmenu-qt5)" = "%{version}"
# test suite
xvfb-run dbus-launch make -C %{_target_platform} check ||:


%clean
rm -rf %{buildroot} 


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_kf5_libdir}/libdbusmenu-qt5.so.2*
%{_kf5_datadir}/doc/libdbusmenu-qt5-doc/

%files devel
%defattr(-,root,root,-)
%{_kf5_includedir}/dbusmenu-qt5/
%{_kf5_libdir}/libdbusmenu-qt5.so
%{_kf5_libdir}/pkgconfig/dbusmenu-qt5.pc
%{_kf5_libdir}/cmake/dbusmenu-qt5/


%changelog
* Thu Feb 13 2014 Daniel Vrátil <dvratil@redhat.com> - 0.9.2-0.2.20140213bzr
- Update to latest git snapshot, rebuild to install to /usr prefix

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> - 0.9.2-0.1.20140205bzr
- Update to latest git snapshot

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> - 0.9.2-1
- fork from dbusmenu-qt, built against Qt 5
