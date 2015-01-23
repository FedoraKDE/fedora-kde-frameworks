%global         git_date    20150123
%global         git_commit  3860b3e

Name:           signon-plugin-oauth2
Version:        0.20
Release:        1.%{git_date}git%{git_commit}%{?dist}
Summary:        OAuth2 plugin for the Accounts framework

License:        LGPLv2
URL:            http://code.google.com/p/accounts-sso
#Source0:        http://accounts-sso.googlecode.com/files/signon-plugins-oauth2-%{version}.tar.bz2
Source0:        signon-plugin-oauth2-%{git_commit}.tar.gz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  signon-qt5-devel
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  libproxy-devel

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build
export PATH=%{_qt5_bindir}:$PATH
%{qmake_qt5} QMF_INSTALL_ROOT=%{_prefix} \
    CONFIG+=release signon-oauth2.pro

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

# Delete tests
rm -fv %{buildroot}/%{_bindir}/signon-oauth2plugin-tests
rm -rfv %{buildroot}/%{_datadir}/signon-oauth2plugin-tests

# Delete examples
rm -fv %{buildroot}/%{_bindir}/oauthclient
rm -rvf %{buildroot}/%{_sysconfdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/signon/liboauth2plugin.so

%files devel
%{_includedir}/signon-plugins/*.h
%{_libdir}/pkgconfig/signon-oauth2plugin.pc


%changelog
* Fri Jan 23 2015 Daniel Vrátil <dvratil@redhat.com> - 8.57-2.20150122git3ef0a6b
- Install dbus service files

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 8.57-1.20150122git3ef0a6b
- Update to latest git snapshot

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 8.56-1
- Initial version
