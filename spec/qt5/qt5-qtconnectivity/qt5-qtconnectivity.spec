
%global qt_module qtconnectivity
# define to build docs, need to undef this for bootstrapping
#%define docs 1

Summary: Qt5 - Connectivity components
Name:    qt5-%{qt_module}
Version: 5.5.0
Release: 0.1.rc%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://qt.io
Source0: http://download.qt.io/snapshots/qt/5.5/%{version}-rc/latest_src/qt-everywhere-opensource-src-%{version}-rc.tar.xz

## upstreamable patches
# bswap_16 apparently missing on el6/ppc64
Patch50: qtconnectivity-opensource-src-5.4.0-bswap_16.patch

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: pkgconfig(bluez)
BuildRequires: pkgconfig(Qt5Qml)
%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-devel
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.



%prep
%setup -q -n qt-everywhere-opensource-src-%{version}-rc

pushd %{qt_module}
%patch50 -p1 -b .bswap_16
popd


%build
pushd %{qt_module}
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..

make %{?_smp_mflags}

%if 0%{?docs}
make %{?_smp_mflags} docs
%endif
popd

# %{qt_module}
popd

%install
pushd %{qt_module}
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%endif

# hardlink files to %{_bindir}, add -qt5 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
  case "${i}" in
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

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

# %{qt_module}
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc %{qt_module}/LGPL_EXCEPTION.txt LICENSE.GPL* LICENSE.LGPL*
%{_bindir}/sdpscanner
%{_qt5_bindir}/sdpscanner
%{_qt5_libdir}/libQt5Bluetooth.so.5*
%{_qt5_archdatadir}/qml/QtBluetooth/
%{_qt5_libdir}/libQt5Nfc.so.5*
%{_qt5_archdatadir}/qml/QtNfc/

%files devel
%{_qt5_headerdir}/QtBluetooth/
%{_qt5_libdir}/libQt5Bluetooth.so
%{_qt5_libdir}/libQt5Bluetooth.prl
%dir %{_qt5_libdir}/cmake/Qt5Bluetooth/
%{_qt5_libdir}/cmake/Qt5Bluetooth/Qt5BluetoothConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Bluetooth.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_bluetooth*.pri
%{_qt5_headerdir}/QtNfc/
%{_qt5_libdir}/libQt5Nfc.so
%{_qt5_libdir}/libQt5Nfc.prl
%dir %{_qt5_libdir}/cmake/Qt5Nfc/
%{_qt5_libdir}/cmake/Qt5Nfc/Qt5NfcConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Nfc.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_nfc*.pri

%if 0%{?docs}
%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtbluetooth.qch
%{_qt5_docdir}/qtbluetooth/
%{_qt5_docdir}/qtnfc.qch
%{_qt5_docdir}/qtnfc/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Mon Jun 15 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> -5.4.2-1
- 5.4.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-2
- rebuild (gcc5)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Fri Jan 02 2015 Dan Horák <dan[at]danny.cz> 5.4.0-2
- include the bswap patch in F-20 and F-21 builds too

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.3.rc
- 5.4.0-rc

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.beta
- out-of-tree build, use %%qmake_qt5

* Sun Oct 19 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta
- 5.4.0-beta

* Tue Sep 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- 5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Mon May 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- sanitize .prl files

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Thu Jan 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- first try
