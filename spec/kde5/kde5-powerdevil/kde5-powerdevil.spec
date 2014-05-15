%define git_commit 6694e1d
%define base_name powerdevil

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        1.20140515git%{git_commit}%{?_dist}
Summary:        Manages the power consumption settings of a Plasma Shell

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{base_name}-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-umbrella
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kidletime-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-kdelibs4support-devel

BuildRequires:  kde5-plasma-workspace-devel

BuildRequires:  chrpath

Requires:       kde5-filesystem

Conflicts:      kde-runtime
Provides:       powerdevil = %{version}-%{release}

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

# FIXME: This is result of broken Cmake Config files from kde5-plasma-workspace-devel
chrpath --delete %{buildroot}/%{_kde5_plugindir}/kded_powerdevil.so
chrpath --delete %{buildroot}/%{_kde5_plugindir}/kcm_powerdevilglobalconfig.so
chrpath --delete %{buildroot}/%{_kde5_plugindir}/kcm_powerdevilprofilesconfig.so
chrpath --delete %{buildroot}/%{_kde5_libdir}/libpowerdevilcore.so.1.1.0
chrpath --delete %{buildroot}/%{_kde5_libdir}/libpowerdevilconfigcommonprivate.so.%{version}

# Don't bother with -devel
rm %{buildroot}/%{_kde5_libdir}/libpowerdevil{configcommonprivate,core,ui}.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_kde5_sysconfdir}/dbus-1/system.d/org.kde.powerdevil.backlighthelper.conf
%{_kde5_libdir}/libpowerdevilconfigcommonprivate.so.*
%{_kde5_libdir}/libpowerdevilcore.so.*
%{_kde5_libdir}/libpowerdevilui.so.*
%{_kde5_plugindir}/*.so
%{_kf5_libexecdir}/kauth/backlighthelper
%{_datadir}/dbus-1/system-services/org.kde.powerdevil.backlighthelper.service
%{_datadir}/knotifications5/powerdevil.notifyrc
%{_datadir}/kservices5/*.desktop
%{_datadir}/kservices5/kded/*.desktop
%{_datadir}/kservicetypes5/*.desktop
%{_datadir}/polkit-1/actions/org.kde.powerdevil.backlighthelper.policy


%changelog
* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515gitf7a2bbe
- Intial snapshot
