%global git_version 6b7ca63
%global git_date 20150114

Name:           kwalletmanager
Summary:        Manage KDE passwords
Version:        5.1.95
Release:        1.beta.%{git_date}git%{git_version}%{?dist}

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/kdeutils/kwalletmanager

# git archive --format=tar.gz --remote=git://anongit.kde.org/kwalletmanager.git \
#             --prefix=kwalletmanager-%{version}/ --output=kwalletmanager-%{git_version}.tar.gz \
#             %{git_version}

Source0:        kwalletmanager-%{git_version}.tar.gz

# when split occured
Conflicts:      kdeutils-common < 6:4.7.80

Obsoletes:      kdeutils-kwalletmanager < 6:4.7.80
Provides:       kdeutils-kwalletmanager = 6:%{version}-%{release}

# renamed 
Obsoletes:      kwallet < 4.12.3-10
Provides:       kwallet = %{version}-%{release}


BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kdbusaddons-devel

BuildRequires:  polkit-qt5-devel

Requires:       polkit-qt
Requires:       polkit-kde

Requires:       kf5-kwallet-runtime

%description
KDE Wallet Manager is a tool to manage the passwords on your KDE system.


%prep
%setup -q -n %{name}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:
fi

%files
%doc COPYING COPYING.LIB
%{_datadir}/applications/org.kde.kwalletmanager5.desktop
%{_datadir}/applications/kwalletmanager5-kwalletd.desktop
%{_datadir}/doc/HTML/*/kwallet
%{_datadir}/kwalletmanager5
%{_kf5_qtplugindir}/kcm_kwallet.so
%{_kf5_libexecdir}/kauth/kcm_kwallet_helper
%{_sysconfdir}/dbus-1/system.d/org.kde.kcontrol.kcmkwallet.conf
%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmkwallet.service
%{_polkit_qt_policydir}/org.kde.kcontrol.kcmkwallet.policy
%{_kf5_datadir}/kservices5/*.desktop
%{_bindir}/kwalletmanager5
%{_kf5_datadir}/kxmlgui5/kwalletmanager5
%{_datadir}/icons/hicolor/*/apps/*


%changelog
* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta.20140114git6b7ca63
- updated to latest git snapshot

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.92-3.20141107git9ef0d8c
- Plasma 5.1.1

* Mon Nov 03 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.92-2.20141023gitcb0f4c7
- Requires: kf5-kwallet-runtime

* Thu Oct 23 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.92-20141023gitcb0f4c7
- KF5 version
