%global git_date 20150122
%global git_commit 0c2e1aa

Name:           kaccounts
Version:        1.0
Release:        2.%{git_date}git%{git_commit}%{?dist}
Summary:        Small system to administer web accounts for the sites and services across the KDE desktop,
License:        LGPLv2
URL:            https://projects.kde.org/projects/kdereview/kaccounts-integration

# git archive --format=tar.gz --remote=git://anongit.kde.org/kaccounts-integration.git \
#             --prefix=kaccounts-integration-%%{version}/ --output=kaccounts-integration-%%{git_commit}.tar.gz \
#             %%{git_commit}

Source0:        kaccounts-integration-%{git_commit}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kdbusaddons-devel

BuildRequires:  libaccounts-qt5-devel
BuildRequires:  signon-qt5-devel

#BuildRequires:  akonadi

%description
Framework to provide Accounts integration in KDE

%package        devel
Summary:        Development files for accounts-qt
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel%{?_isa}
Requires:       kf5-kcoreaddons-devel%{?_isa}
Requires:       libaccounts-qt5-devel%{?_isa}
Requires:       signon-qt5-devel%{?_isa}

%description    devel
Headers, development libraries and documentation for %{name}.

%prep
%setup -q -n kaccounts-integration-%{version}

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
%doc COPYING README
%{_kf5_qtplugindir}/kcm_kaccounts.so
%{_kf5_datadir}/kservices5/kcm_kaccounts.desktop
%{_kf5_qtplugindir}/kded_accounts.so
%{_kf5_datadir}/kservices5/kded/accounts.desktop
%{_libdir}/libkaccounts.so.*

%files devel
%{_libdir}/libkaccounts.so
%{_libdir}/cmake/KAccounts
%{_includedir}/KAccounts

%changelog
* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 1.0.0-2.20150122git0c2e1aa
- Fix -devel Requries

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 1.0.0-1.20150122git0c2e1aa
- Initial version
