Name:           kwrited
Version:        5.2.0
Release:        1%{?dist}
Summary:        KDE Write Daemon

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/kwrited

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

Patch0:         kwrited-call-setgroups.patch

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kpty-devel
BuildRequires:  kf5-kdelibs4support-devel

Requires:       kf5-filesystem

# Owns /usr/share/knotifications5
Requires:       kf5-knotifications

# TODO: Remove once kwrited is split from kde-workspace
Conflicts:      kde-workspace < 5.0.0-1

%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1 -b .setgroups

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%files
%doc COPYING
%{_bindir}/kwrited
%config %{_sysconfdir}/xdg/autostart/kwrited-autostart.desktop
%{_kf5_datadir}/knotifications5/kwrited.notifyrc


%changelog
* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Tue Jan 06 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-3
- missing %%config
- add patch to call setgroups(0, 0)
- deps fix

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Wed Jul 23 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- Rebuild

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515gitc11b832c
- Intial snapshot
