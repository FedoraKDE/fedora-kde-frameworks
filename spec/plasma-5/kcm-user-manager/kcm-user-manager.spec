%global modulename user-manager

Name:           kcm-user-manager
Epoch:          1
Version:        5.1.95
Release:        1.beta
Summary:        KDE System Settings module to manage system users

# KDE e.V. may determine that future GPL versions are accepted
License:        GPLv2
URL:            https://projects.kde.org/projects/kde/workspace/user-manager

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{modulename}-%{version}.tar.xz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kdelibs4support-devel

BuildRequires:  libpwquality-devel

Requires:       kf5-filesystem

%description
%{summary}.

%prep
%setup -q -n %{modulename}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd
make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# Upstream is a mess, let's force the kcm_ prefix to keep stuff tidy
mv %{buildroot}/%{_kf5_qtplugindir}/user_manager.so \
   %{buildroot}/%{_kf5_qtplugindir}/kcm_user_manager.so
mv %{buildroot}/%{_kf5_datadir}/kservices5/user_manager.desktop \
   %{buildroot}/%{_kf5_datadir}/kservices5/kcm_user_manager.desktop
sed -i 's/X-KDE-Library=user_manager/X-KDE-Library=kcm_user_manager/' \
   %{buildroot}/%{_kf5_datadir}/kservices5/kcm_user_manager.desktop

%files
%doc COPYING
%{_kf5_qtplugindir}/kcm_user_manager.so
%{_kf5_datadir}/kservices5/kcm_user_manager.desktop

%changelog
* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta
