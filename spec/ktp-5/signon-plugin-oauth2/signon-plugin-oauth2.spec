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
BuildRequires:  signon-qt5-devel
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  libproxy-devel

%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build

#sed -i "s/qdbusxml2cpp/qdbusxml2cpp-qt5/" src/signond/signond.pro

export PATH=%{_qt5_bindir}:$PATH
%{qmake_qt5} QMF_INSTALL_ROOT=%{_prefix} \
    CONFIG+=release signon-oauth2.pro

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

# Remove static libraries
rm %{buildroot}/%{_libdir}/*.a


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files



%changelog
* Fri Jan 23 2015 Daniel Vrátil <dvratil@redhat.com> - 8.57-2.20150122git3ef0a6b
- Install dbus service files

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 8.57-1.20150122git3ef0a6b
- Update to latest git snapshot

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 8.56-1
- Initial version
