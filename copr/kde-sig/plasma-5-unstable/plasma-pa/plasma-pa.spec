Name:           plasma-pa
Version: 5.5.95
Release: 1%{?dist}
Summary:        Plasma applet for audio volume management using PulseAudio
License:        LGPLv2+ and GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/plasma-na

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  glib2-devel
BuildRequires:  kde-filesystem
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kpackage-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel

Requires:       kf5-filesystem

%description
%{summary}.


%prep
%setup -q -n %{name}-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --all-name

## unpackaged files
rm -rfv %{buildroot}%{_kde4_appsdir}/kconf_update/


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%license COPYING COPYING.LIB
%{_kf5_datadir}/plasma/plasmoids/org.kde.plasma.volume
%{_kf5_qmldir}/org/kde/plasma/private/volume/
%{_kf5_qtplugindir}/kcms/kcm_pulseaudio.so
%{_kf5_datadir}/kservices5/plasma-applet-org.kde.plasma.volume.desktop
%{_kf5_datadir}/kconf_update/*
%{_kf5_libdir}/libQPulseAudioPrivate.so
%{_kf5_datadir}/kpackage/kcms/kcm_pulseaudio
%{_kf5_datadir}/kservices5/kcm_pulseaudio.desktop
%lang(en) %{_kf5_docdir}/HTML/en/plasma-pa/
%lang(uk) %{_kf5_docdir}/HTML/uk/plasma-pa/
%lang(ca) %{_kf5_docdir}/HTML/ca/plasma-pa/
%lang(pt_BR) %{_kf5_docdir}/HTML/pt_BR/plasma-pa/


%changelog
* Sat Mar 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-1
- Plasma 5.5.95

* Tue Mar 01 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.5-1
- Plasma 5.5.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.4-1
- Plasma 5.5.4

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-1
- 5.5.2

* Fri Dec 18 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.1-1
- Plasma 5.5.1

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.95-1
- Plasma 5.4.95

* Fri Nov 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.3-2
- .spec cosmetics, fix URL

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-1
- 5.4.1

* Tue Aug 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Upate to 5.4.0
- add %%license

* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Initial version
