Name:           signon-plugin-oauth2
Version:        0.21
Release:        1%{?dist}
Summary:        OAuth2 plugin for the Accounts framework

License:        LGPLv2
URL:            http://code.google.com/p/accounts-sso

# Source available from https://drive.google.com/drive/#folders/0B8fX9XOwH_g4alFsYV8tZTI4VjQ
# as per https://groups.google.com/forum/#!topic/accounts-sso-announce/YBfS0ACmFl0
Source0:        signon-oauth2-%{version}.tar.bz2

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
%setup -q -n signon-oauth2-%{version}

%build
export PATH=%{_qt5_bindir}:$PATH
%{qmake_qt5} QMF_INSTALL_ROOT=%{_prefix} \
    CONFIG+=release \
    LIBDIR=%{_libdir} \
    signon-oauth2.pro

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
* Wed Apr 29 2015 Daniel Vrátil <dvratil@redhat.com> - 0.21-2
- Set correct libdir for installation

* Tue Mar 17 2015 Daniel Vrátil <dvratil@redhat.com> - 0.21-1
- Initial version
