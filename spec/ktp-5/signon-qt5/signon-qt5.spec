%global         git_date    20150122
%global         git_commit  3ef0a6b

Name:           signon-qt5
Version:        8.57
Release:        2.%{git_date}git%{git_commit}%{?dist}
Summary:        Accounts framework for Linux and POSIX based platforms

License:        LGPLv2
URL:            http://code.google.com/p/accounts-sso
#Source0:        http://accounts-sso.googlecode.com/files/signon-%{version}.tar.bz2
Source0:        signon-%{git_commit}.tar.gz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  libproxy-devel

%description
Single Sign-On is a framework for centrally storing authentication credentials
and handling authentication on behalf of applications as requested by
applications. It consists of a secure storage of login credentials (for example
usernames and passwords), plugins for different authentication systems and a
client library for applications to communicate with this system.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glib2-devel%{?_isa}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description doc
The %{name}-doc package contains documentation for %{name}.


%prep
%setup -q -n signon-%{version}

%build

sed -i "s/qdbusxml2cpp/qdbusxml2cpp-qt5/" src/signond/signond.pro

export PATH=%{_qt5_bindir}:$PATH
%{qmake_qt5} QMF_INSTALL_ROOT=%{_prefix} \
    CONFIG+=release signon.pro

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

# Remove static libraries
rm %{buildroot}/%{_libdir}/*.a


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc README TODO NOTES COPYING
%config(noreplace) %{_sysconfdir}/signond.conf
%{_bindir}/signond
%{_bindir}/signonpluginprocess
%{_libdir}/libsignon-extension.so.*
%{_libdir}/libsignon-plugins-common.so.*
%{_libdir}/libsignon-plugins.so.*
%{_libdir}/libsignon-qt5.so.*
%{_libdir}/signon
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/services/*.service

%files devel
%{_includedir}/signon-extension
%{_includedir}/signon-plugins
%{_includedir}/signon-qt5
%{_includedir}/signond
%{_libdir}/cmake/SignOnQt5
%{_libdir}/libsignon-extension.so
%{_libdir}/libsignon-plugins-common.so
%{_libdir}/libsignon-plugins.so
%{_libdir}/libsignon-qt5.so
%{_libdir}/pkgconfig/*.pc

%files doc
%{_docdir}/signon
%{_docdir}/libsignon-qt
%{_docdir}/signon-plugins
%{_docdir}/signon-plugins-dev


%changelog
* Fri Jan 23 2015 Daniel Vrátil <dvratil@redhat.com> - 8.57-2.20150122git3ef0a6b
- Install dbus service files

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 8.57-1.20150122git3ef0a6b
- Update to latest git snapshot

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 8.56-1
- Initial version
