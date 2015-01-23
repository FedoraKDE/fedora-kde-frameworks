#%global git_version 7a8460a
#%global git_date 20150112

Name:           kscreen
Epoch:          1
Version:        5.2.0
Release:        1%{?dist}
Summary:        KDE Display Management software

# KDE e.V. may determine that future GPL versions are accepted
License:        GPLv2 or GPLv3
URL:            https://projects.kde.org/projects/playground/base/kscreen

Source0:        http://download.kde.org/stable/kscreen/%{version}/src/kscreen-%{version}.tar.xz
# git archive --format=tar.gz --prefix=kscreen-%{version}/ --remote=git://anongit.kde.org/kscreen \
#             --output=kscreen-%{git_version}.tar.gz %{git_version}
#Source0:        kscreen-%{git_version}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtdeclarative-devel

BuildRequires:  kf5-kscreen-devel

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kglobalaccel-devel

Requires:       kf5-filesystem

%description
KCM and KDED modules for managing displays in KDE.

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
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
fi

%files
%doc COPYING
%{_bindir}/kscreen-console
%{_kf5_qtplugindir}/kcm_kscreen.so
%{_kf5_qtplugindir}/kded_kscreen.so
%{_datadir}/kcm_kscreen/
%{_kf5_datadir}/kservices5/kcm_kscreen.desktop
%{_kf5_datadir}/kservices5/kded/kscreen.desktop
%{_datadir}/icons/hicolor/*/actions/*

%changelog
* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-2.beta.20150112git7a8460a
- BR kf5-kscreen-devel (renamed from libkscreen)

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta.20150112git7a8460a
- Update to latest git snapshot

* Thu Jan 08 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2.20150108git0d70c77
- Update to latest git snapshot

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Fri Nov 28 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1.20141128gitccf52c4
- Update to latest git snapshot

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1.20141107git88b2a3f
- Plasma 5.1.1

* Thu Oct 23 2014 Daniel Vrátil <dvratil@redhat.com> 1:5.0.92-20141023git
 - kscreen 5.0.92 (git)

* Fri Nov 22 2013 Dan Vrátil <dvratil@redhat.com> 1:1.0.2.1-1
 - kscreen 1:1.0.2.1-1

* Wed Nov 20 2013 Dan Vrátil <dvratil@redhat.com> 1:1.0.2-1
 - kscreen 1:1.0.2-1

* Thu Aug 01 2013 Dan Vrátil <dvratil@redhat.com> 1:1.0.1-1
 - kscreen 1:1.0.1-1

* Mon Jun 17 2013 Dan Vrátil <dvratil@redhat.com> 1:1.0-1
 - kscreen 1:1.0-1

* Thu May 02 2013 Dan Vrátil <dvratil@redhat.com> 1:0.0.92-1
 - update to 1:0.0.92-1
 
* Tue Apr 23 2013 Dan Vrátil <dvratil@redhat.com> 1:0.0.82.git20130424-1
 - dev git build

* Mon Apr 08 2013 Dan Vrátil <dvratil@redhat.com> 1:0.0.81-2
 - Explicitely depend on the same version of libkscreen

* Wed Mar 27 2013 Dan Vrátil <dvratil@redhat.com> 1:0.0.81-1
 - Update to 1:0.0.81-1

* Mon Jan 28 2013 Rex Dieter <rdieter@fedoraproject.org> 1:0.0.71-3
- drop Provides: kde-display-management, Conflicts: kded_randrmonitor

* Thu Jan 24 2013 Dan Vrátil <dvratil@redhat.com> 1:0.0.71-2
 - add Provides and Conflicts fields so make sure radrmonitor and
   kscreen never run side by side

* Sun Jan 20 2013 Dan Vrátil <dvratil@redhat.com> 1:0.0.71-1
 - update to 0.0.71 - first official release
 - install kscreen-console, which has been moved from libkscreen
 - the KCM is now called kcm_kscreen

* Wed Jan 09 2013 Dan Vrátil <dvratil@redhat.com> 0.9.0-5.20121228git
 - Update description, we don't ship the Plasma applet yet
 - Provides kde-display-management, a metapackage for KScreen and kded_randrmonitor
 - Conflicts with kded_randrmonitor

* Wed Jan 09 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-4.20121228git
- BR: qjson-devel >= 0.8.1
- License: GPLv2 or GPLv3
- tighten %%files

* Wed Jan 02 2013 Dan Vrátil <dvratil@redhat.com> 0.9.0-3.20121228git
 - Added qjson-devel to BuildRequires

* Fri Dec 28 2012 Dan Vrátil <dvratil@redhat.com> 0.9.0-2.20121228git
 - Fixed URL

* Fri Dec 28 2012 Dan Vrátil <dvratil@redhat.com> 0.9.0-1.20121228git
 - Fixed versioning
 - Added instructions how to obtain sources
 - Removed 'rm -rf $RPM_BUILD_ROOT'

* Wed Dec 26 2012 Dan Vrátil <dvratil@redhat.com> 20121226gitb31ab08-1
 - Initial SPEC
