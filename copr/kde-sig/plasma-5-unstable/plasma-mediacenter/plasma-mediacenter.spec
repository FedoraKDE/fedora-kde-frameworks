Name:           plasma-mediacenter
Version: 5.5.95
Release: 1%{?dist}
Summary:        A mediacenter user interface written with the Plasma framework

License:        GPLv2
URL:            https://projects.kde.org/plasma-mediacenter
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-baloo-devel
BuildRequires:  kf5-kactivities-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  taglib-devel

Obsoletes: plasma-mediacenter-devel < 5.0.0

Requires:       qt5-qtmultimedia%{?_isa}

%description
Plasma Media Center is designed to provide an easy and comfortable
way to watch your videos, browse your photo collection and listen to
your music, all in one place. This release brings many refinements
and a host of new features, making consuming media even easier and
more fun.


%prep
%autosetup -n %{name}-%{version} -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd
make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast -C %{_target_platform} DESTDIR=%{buildroot}

%find_lang all --all-name


%check
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/plasma-mediacenter.desktop


%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f all.lang
%license COPYING COPYING.LIB
%doc README
%{_kf5_libdir}/libplasmamediacenter.so.*
%{_kf5_qtplugindir}/plasma/mediacenter/
%{_kf5_qmldir}/org/kde/plasma/mediacenter/
%{_kf5_datadir}/applications/plasma-mediacenter.desktop
%{_kf5_datadir}/kservices5/plasma-shell-org.kde.plasma.mediacenter.desktop
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_datadir}/plasma/shells/org.kde.plasma.mediacenter/
%{_datadir}/xsessions/plasma-mediacenter.desktop
%{_datadir}/icons/hicolor/*/*/*


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

* Fri Dec 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-2
- .spec cosmetics, Obsoletes: plasma-mediacenter-devel (#1290669)

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Update to Plasma 5.4.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.3.0-3
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 24 2014 Sinny Kumari<ksinny@gmail.com> - 1.3.0-1
- New release 1.3.0

* Sat Nov 23 2013 siddharth sharma<siddharth.kde@gmail.com> - 1.1.9-1
- New Release 1.1.9
- Patch include translations sub-directory

* Fri Sep 13 2013 siddharth <siddharth.kde@gmail.com> - 1.1.0a-2
- New Release 1.1.0a
- Add gettext for BuildRequires

* Mon Aug 12 2013 siddharth sharma <siddharth.kde@gmail.com> - 1.0.95-1
- new release plasma-mediacenter-1.0.95

* Thu Aug 01 2013 siddharth sharma <siddharth.kde@gmail.com> - 1.0.90-1
- new release plasma-mediacenter-1.0.90
- remove kdenetwork-fileshare-samba
- Adding youtube icon
- Changing Requires

* Wed Jul 31 2013 siddharth sharma <siddharth.kde@gmail.com> - 1.0.0-3
- remove plasma-mobile from buildrequires

* Wed Mar 20 2013 siddharth <siddharths@fedoraproject.org> - 1.0.0-2
- rebuilt, Fixing missing BuildRequires for new package

* Wed Mar 20 2013 siddharth sharma <siddharths@fedoraproject.org> -1.0.0-1
- new upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 24 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.8.90-6
- %%files cleanup
- remove deprecated .spec
- remove unneccessary hacks (in particular, move plugins back to where they belong)

* Wed Oct 24 2012 siddharth <siddharth.kde@gmail.com> - 0.8.90-5
- Removed unwanted Requires and BuildRequires
- Removed Hicolor icons

* Wed Sep 12 2012 siddharth <siddharth.kde@gmail.com> - 0.8.90-4
- Fix installing plugins path

* Thu Jun 14 2012 Siddharth Sharma <siddharth.kde@gmail.com> - 0.8.90-3
- Packaging Fixes
- Package update Beta Release

* Sun Jun 03 2012 siddharth <siddharth.kde@gmail.com> - 0.9-2
- rebuilt for devel package split

* Sat Jun 2 2012 siddharth Sharma <siddharths@fedoraproject.org> - 0.9-1
- Initial Release 1

