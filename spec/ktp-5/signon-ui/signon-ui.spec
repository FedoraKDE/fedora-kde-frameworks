Name:           signon-ui
Version:        0.15
Release:        2%{?dist}
Summary:        Online Accounts Sign-on Ui

License:        GPLv3
URL:            https://launchpad.net/signon-ui

Source0:        https://launchpad.net/signon-ui/trunk/%{version}/+download/signon-ui-%{version}.tar.bz2

Patch0:         signon-ui-0.15-fix-qt5-build.patch

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  libaccounts-qt5-devel
BuildRequires:  signon-qt5-devel
BuildRequires:  libproxy-devel
BuildRequires:  libnotify-devel

Requires:       dbus

%description
Sign-on UI is the component responsible for handling the user interactions which
can happen during the login process of an online account.
It can show password dialogs and dialogs with embedded web pages.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n signon-ui-%{version}

%patch0 -p1 -b .qt5


%build
export PATH=%{_qt5_bindir}:$PATH
%{qmake_qt5} QMF_INSTALL_ROOT=%{_prefix} \
    CONFIG+=release signon-ui.pro

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

# Remove installed tests
rm %{buildroot}/%{_bindir}/signon-ui-unittest
rm %{buildroot}/%{_bindir}/tst_inactivity_timer

# Own directory where others can install provider-specific configuration
mkdir -p %{buildroot}/%{_sysconfdir}/signon-ui/webkit-options.d

%files
%doc README TODO NOTES
%license COPYING
%{_bindir}/signon-ui
%{_datadir}/dbus-1/services/*.service
%{_sysconfdir}/signon-ui

%changelog
* Wed Mar 25 2015 Daniel Vrátil <dvratil@redhat.com> - 0.15-2
- fix license
- fix typo in mkdir arguments
- use %%license

* Tue Mar 17 2015 Daniel Vrátil <dvratil@redhat.com> - 0.15-1
- Initial version
