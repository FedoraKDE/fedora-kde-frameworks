Name:           kwrited
Version:        5.0.0
Release:        2%{?dist}
Summary:        KDE's kwrited daemon

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/stable/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kpty-devel
BuildRequires:  kf5-kdelibs4support-devel

Requires:       kf5-filesystem

%description
%{summary}.

%prep
%setup -q

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_bindir}/kwrited
%config %{_sysconfdir}/xdg/autostart/kwrited-autostart.desktop
%{_kf5_datadir}/knotifications5/kwrited.notifyrc


%changelog
* Wed Jul 23 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- Rebuild

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515gitc11b832c
- Intial snapshot
