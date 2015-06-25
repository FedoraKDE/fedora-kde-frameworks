
%global qt_module qtimageformats

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
%define docs 1

# where to enable webp support
%if 0%{?fedora} || 0%{?rhel} > 6
%global webp 1
%endif

%define pre rc

Summary: Qt5 - QtImageFormats component
Name:    qt5-%{qt_module}
Version: 5.5.0
Release: 0.2.rc%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
Source0: http://download.qt.io/development_releases/qt/5.5/%{version}%{?pre:-%{pre}}/submodules/%{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}.tar.xz

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: libmng-devel
BuildRequires: libtiff-devel
BuildRequires: jasper-devel
%if 0%{?webp}
BuildRequires: libwebp-devel
%else
Provides: bundled(libwebp)
%endif

# prior -devel subpkg contained only runtime cmake bits
Obsoletes: qt5-qtimageformats-devel < 5.4.0
Provides:  qt5-qtimageformats-devel = %{version}-%{release}

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The core Qt Gui library by default supports reading and writing image
files of the most common file formats: PNG, JPEG, BMP, GIF and a few more,
ref. Reading and Writing Image Files. The Qt Image Formats add-on module
provides optional support for other image file formats, including:
MNG, TGA, TIFF, WBMP.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
License: GFDL
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-devel
BuildArch: noarch
%description doc
%{summary}.
%endif


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}
%if 0%{?webp}
rm -rv src/3rdparty
%endif

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..

make %{?_smp_mflags}

%if 0%{?docs}
make %{?_smp_mflags} docs
%endif
popd


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%endif

%files
%doc LGPL_EXCEPTION.txt LICENSE.GPL* LICENSE.LGPL*
%{_qt5_plugindir}/imageformats/libqmng.so
%{_qt5_plugindir}/imageformats/libqtga.so
%{_qt5_plugindir}/imageformats/libqtiff.so
%{_qt5_plugindir}/imageformats/libqwbmp.so
%{_qt5_plugindir}/imageformats/libqdds.so
%{_qt5_plugindir}/imageformats/libqicns.so
%{_qt5_plugindir}/imageformats/libqjp2.so
%{_qt5_plugindir}/imageformats/libqwebp.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_*Plugin.cmake

%if 0%{?docs}
%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtimageformats.qch
%{_qt5_docdir}/qtimageformats/
%endif


%changelog
* Wed Jun 24 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Wed Jun 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> 5.4.2-1
- 5.4.2

* Sat May 23 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-4
- Provides: qt5-qtimageformat-devel

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-2
- rebuild (gcc5)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.3.rc
- 5.4.0-rc

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.beta
- out-of-tree build, use %%qmake_qt5

* Sun Oct 19 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta
- 5.4.0-beta, Obsoletes: qt5-qtimageformats-devel

* Wed Sep 17 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.3.2-1
- 5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.0-1
- 5.3.0

* Tue Mar 18 2014 Ville Skyttä <ville.skytta@iki.fi> - 5.2.1-2
- Fix libmng test, build with system one instead of bundled

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Sun Nov 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.beta1
- 5.2.0-beta1

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- ppc bootstrap

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -devel subpkg
- -doc subpkg

* Fri Aug 30 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- 5.1.1

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- update Source URL
- include license files
- improved description

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

