%global         git_date    20150122
%global         git_commit  533aa91

Name:           libaccounts-qt5
Version:        1.13
Release:        1.%{git_date}git%{git_commit}%{?dist}
Summary:        Accounts framework Qt 5 bindings
Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://code.google.com/p/accounts-sso/

#Source0:        http://accounts-sso.googlecode.com/files/accounts-qt-%{version}.tar.bz2
# git archive --format=tar.gz --remote=git://code.google.com/p/accounts-sso.libaccounts-qt/ \
#             --prefix=libaccounts-qt-%%{version}/ --output=libaccounts-%%{git_commit}.tar.gz %%{git_commit}
Source0:        libaccounts-qt-%{git_commit}.tar.gz

Patch1:         libaccounts-qt-64bitarchs.patch

BuildRequires:  qt5-qtbase-devel
BuildRequires:  libaccounts-glib-devel
BuildRequires:  doxygen
BuildRequires:  graphviz

%description
Framework to provide accounts for Qt 5.

%package        devel
Summary:        Development files for accounts-qt
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel%{?_isa}

%description    devel
Headers, development libraries and documentation for accounts-qt.

%prep
%setup -q -n libaccounts-qt-%{version}
%patch1 -p1 -b .64bitarchs

%build
%{_qt5_qmake} QMF_INSTALL_ROOT=%{_prefix} \
    CONFIG+=release \
    accounts-qt.pro

make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}

rm -f %{buildroot}/%{_datadir}/doc/accounts-qt/html/installdox

#remove tests for now
rm -rf %{buildroot}%{_datadir}/libaccounts-qt-tests
rm -f %{buildroot}%{_bindir}/accountstest

# move installed docs to include them in subpackage via %%doc magic
rm -rf __tmp_doc ; mkdir __tmp_doc
mv %{buildroot}%{_docdir}/accounts-qt __tmp_doc

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
#%doc COPYING
%{_libdir}/libaccounts-qt5.so.*

%files devel
%{_libdir}/libaccounts-qt5.so
%{_includedir}/accounts-qt5/
%{_libdir}/pkgconfig/accounts-qt5.pc
%{_libdir}/cmake/AccountsQt5
#%doc __tmp_doc/accounts-qt/*

%changelog
* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 1.13-1
- Update to latest git snapshot

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 1.11-2
- Specify custom CMAKE_CONFIG_PATH

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 1.11-1
- Fork accounts-qt to Qt 5 version
