%define git_commit 9afaa84
%define base_name kwalletmanager

Name:           kde5-%{base_name}
Version:        4.90.0
Release:        1.20140519git%{git_commit}%{?dist}
Summary:        KDE Wallet Manager is a tool to manage the passwords on your KDE system.

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
# Source0:        http://download.kde.org/unstable/kde-baseapps/%{version}/kde-baseapps-%{version}.tar.xz
Source0:        %{base_name}-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel

BuildRequires:  kde5-rpm-macros

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-umbrella
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

Requires:       kde5-filesystem

%description
%{summary}.

%prep
%setup -q -n %{base_name}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING COPYING.LIB
%{_kde5_bindir}/kwalletmanager
%{_kde5_sysconfdir}/dbus-1/system.d/org.kde.kcontrol.kcmkwallet.conf
%{_kde5_plugindir}/kcm_kwallet.so
%{_kde5_libexecdir}/kcm_kwallet_helper
%{_datadir}/applications/kwalletmanager-kwalletd.desktop
%{_datadir}/applications/kwalletmanager.desktop
%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmkwallet.service
%{_datadir}/doc/HTML/en/kwallet
%{_datadir}/icons/*/*/*/*.png
%{_kde5_datadir}/kwalletmanager
%{_datadir}/kservices5/kwalletconfig.desktop
%{_datadir}/kservices5/kwalletmanager_show.desktop
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmkwallet.policy

%changelog
* Tue May 20 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.0-1.20140520git9afaa84
- initial version
