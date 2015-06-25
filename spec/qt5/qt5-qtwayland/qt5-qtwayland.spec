
%global qt_module qtwayland

# build support for non-egl platforms
%define nogl 1

%define prerelease rc

Summary:        Qt5 - Wayland platform support and QtCompositor module
Name:           qt5-%{qt_module}
Version:        5.5.0
Release:        0.2.rc%{?dist}
License:        LGPLv2 with exceptions or LGPLv3 with exceptions
Url:            http://www.qt.io
Source0: http://download.qt.io/development_releases/qt/5.5/%{version}%{?prerelease:-%{prerelease}}/submodules/%{qt_module}-opensource-src-%{version}%{?prerelease:-%{prerelease}}.tar.xz

BuildRequires:  qt5-qtbase-devel >= %{version} 
BuildRequires:  qt5-qtbase-static
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libinput)

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
%{summary}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary:        Examples for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?prerelease:-%{prerelease}}

%build
%if 0%{?nogl}
# build support for non-egl platforms
mkdir nogl
pushd nogl
%{qmake_qt5} QT_WAYLAND_GL_CONFIG=nogl ..
popd
make %{?_smp_mflags} -C nogl
%endif

%{_qt5_qmake} CONFIG+=wayland-compositor
make %{?_smp_mflags}

%install
%if 0%{?nogl}
make install INSTALL_ROOT=%{buildroot} -C nogl/
%endif
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


# install private headers... needed by hawaii shell 
install -pm644 \
  include/QtCompositor/%{version}/QtCompositor/private/{wayland-wayland-server-protocol.h,qwayland-server-wayland.h} \
  %{buildroot}%{_qt5_headerdir}/QtCompositor/%{version}/QtCompositor/private/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%doc LICENSE.LGPL* LGPL_EXCEPTION.txt
%{_qt5_libdir}/libQt5Compositor.so.5*
%{_qt5_libdir}/libQt5WaylandClient.so.5*
%dir %{_qt5_plugindir}/wayland-decoration-client/
%{_qt5_plugindir}/wayland-decoration-client/libbradient.so
%{_qt5_plugindir}/wayland-graphics-integration-server
%{_qt5_plugindir}/wayland-graphics-integration-client
%{_qt5_plugindir}/platforms/libqwayland-egl.so
%{_qt5_plugindir}/platforms/libqwayland-generic.so
%{_qt5_plugindir}/platforms/libqwayland-xcomposite-egl.so
%{_qt5_plugindir}/platforms/libqwayland-xcomposite-glx.so
%dir %{_qt5_libdir}/cmake/Qt5Compositor/
%{_qt5_libdir}/cmake/Qt5Compositor/Qt5Compositor_*.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_*.cmake
%dir %{_qt5_libdir}/cmake/Qt5WaylandClient/
%{_qt5_libdir}/cmake/Qt5WaylandClient/Qt5WaylandClient_*.cmake

%files devel
%{_qt5_bindir}/qtwaylandscanner
%{_qt5_headerdir}/QtCompositor/
%{_qt5_headerdir}/QtWaylandClient/
%{_qt5_libdir}/libQt5Compositor.so
%{_qt5_libdir}/libQt5WaylandClient.so
%{_qt5_libdir}/libQt5Compositor.prl
%{_qt5_libdir}/libQt5WaylandClient.prl
%{_qt5_libdir}/cmake/Qt5Compositor/Qt5CompositorConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Compositor.pc
%{_qt5_libdir}/pkgconfig/Qt5WaylandClient.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_compositor*.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_waylandclient*.pri

%files examples
%{_qt5_examplesdir}/wayland/


%changelog
* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Wed Jun 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt5 5.5.0 RC1

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.2-1
- 5.4.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-2
- Rebuilt for GCC 5 C++11 ABI change

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-1
- 5.4.1

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.3.rc
- 5.4.0-rc

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.beta
- use %%qmake_qt5 macro

* Mon Oct 20 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta 
- 5.4.0-beta

* Wed Sep 24 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.4.0-0.alpha1
- Switch from a Git snapshot to a pre-release tarball

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-0.3.20140723git02c499c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.3.0-0.2.20140723git02c499c
- Update

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-0.2.20140529git98dca3b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.3.0-0.1.20140529git98dca3b
- Update and rebuild for Qt 5.3

* Fri Feb 14 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.6.20140202git6d038fb
- A more recent snapshot
- Disable xcomposite compositor until it builds

* Sat Jan 04 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.6.20131203git6b20dfe
- Enable QtQuick compositor

* Sat Jan 04 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.5.20131203git6b20dfe
- A newer snapshot

* Mon Nov 25 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.5.20131125git4f5985c
- Rebase to a later snapshot, drop our patches
- Add license texts

* Sat Nov 23 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.5.20131120git8cd1a77
- Rebuild with EGL backend

* Fri Nov 22 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.4.20131120git8cd1a77
- Rebase to a later snapshot, drop 5.2 ABI patch
- Enable nogl backend

* Sun Nov 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.0-0.4.20130826git3b0b90b
- rebuild (arm/qreal)

* Thu Oct 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.3.20130826git3b0b90b
- Bulk sad and useless attempt at consistent SPEC file formatting

* Sun Oct 06 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.2.20130826git3b0b90b
- Bump platform plugin ABI to 5.2 for Qt 5.2 aplha

* Wed Sep 11 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.1.20130826git3b0b90b
- Initial packaging
- Adjustments from review (Rex Dieter, #1008529)
