
%global bootstrap 1

%global qt_module qttools
%if 0%{?fedora} > 19 || 0%{?rhel} > 6
%global system_clucene 1
%endif

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
# only primary archs (for now), allow secondary to bootstrap
%if ! 0%{?bootstrap}
%ifarch %{arm} %{ix86} x86_64
%define docs 1
%endif
%endif

%define pre rc

Summary: Qt5 - QtTool components
Name:    qt5-qttools
Version: 5.5.0
Release: 0.2.rc%{?dist}

License: LGPLv3 or LGPLv2
Url:     http://www.qt.io
Source0: http://download.qt.io/development_releases/qt/5.5/%{version}%{?pre:-%{pre}}/submodules/%{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}.tar.xz

Patch1: qttools-opensource-src-5.3.2-system-clucene.patch

# help lrelease/lupdate use/prefer qmake-qt5
# https://bugzilla.redhat.com/show_bug.cgi?id=1009893
Patch2: qttools-opensource-src-5.2.0-qmake-qt5.patch

## upstream patches

Source20: assistant.desktop
Source21: designer.desktop
Source22: linguist.desktop
Source23: qdbusviewer.desktop

# %%check needs cmake (and don't want to mess with cmake28)
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires: cmake
%endif
BuildRequires: desktop-file-utils
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtbase-static >= %{version}
BuildRequires: qt5-qtdeclarative-static >= %{version}
BuildRequires: qt5-qtwebkit-devel

%if 0%{?system_clucene}
BuildRequires: clucene09-core-devel >= 0.9.21b-12
%endif

Requires: %{name}-common = %{version}-%{release}
%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

# when -libs were split out, for multilib upgrade path
Obsoletes: qt5-tools < 5.4.0-0.2

%description
%{summary}.

%package common
Summary: Common files for %{name}
BuildArch: noarch
%description common
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs-clucene%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-help%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Provides: qt5-designer = %{version}-%{release}
Provides: qt5-linguist = %{version}-%{release}
%description devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%package libs-clucene
Summary: Qt5 CLucene runtime library
Requires: %{name}-common = %{version}-%{release}
# when split happened
Conflicts: qt5-tools < 5.4.0-0.2
%description libs-clucene
%{summary}.

%package libs-designer
Summary: Qt5 Designer runtime library
Requires: %{name}-common = %{version}-%{release}
# when split happened
Conflicts: qt5-tools < 5.4.0-0.2
%description libs-designer
%{summary}.

%package libs-designercomponents
Summary: Qt5 Designer Components runtime library
Requires: %{name}-common = %{version}-%{release}
# when split happened
Conflicts: qt5-tools < 5.4.0-0.2
%description libs-designercomponents
%{summary}.

%package libs-help
Summary: Qt5 Help runtime library
Requires: %{name}-common = %{version}-%{release}
# when split happened
Conflicts: qt5-tools < 5.4.0-0.2
%description libs-help
%{summary}.

%package -n qt5-assistant
Summary: Documentation browser for Qt5
Requires: %{name}-common = %{version}-%{release}
%description -n qt5-assistant
%{summary}.

%package -n qt5-designer-plugin-webkit
Summary: Qt5 designer plugin for WebKit
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
%description -n qt5-designer-plugin-webkit
%{summary}.

%package -n qt5-qdbusviewer
Summary: D-Bus debugger and viewer
Requires: %{name}-common = %{version}-%{release}
%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}
%description -n qt5-qdbusviewer
QDbusviewer can be used to inspect D-Bus objects of running programs
and invoke methods on those objects.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
# for qhelpgenerator
BuildRequires: qt5-qttools-devel
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}-common = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}

%if 0%{?system_clucene}
%patch1 -p1 -b .system_clucene
# bundled libs
rm -rf src/assistant/3rdparty/clucene
%endif
%patch2 -p1 -b .qmake-qt5

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

# Add desktop files, --vendor=qt4 helps avoid possible conflicts with qt3/qt4
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --vendor="qt5" \
  %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23}

# icons
install -m644 -p -D src/assistant/assistant/images/assistant.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/assistant-qt5.png
install -m644 -p -D src/assistant/assistant/images/assistant-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/assistant-qt5.png
install -m644 -p -D src/designer/src/designer/images/designer.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/designer-qt5.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/qdbusviewer-qt5.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qdbusviewer-qt5.png
# linguist icons
for icon in src/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist-qt5.png
done

# hardlink files to %{_bindir}, add -qt5 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
  case "${i}" in
   assistant|designer|lconvert|linguist|lrelease|lupdate|pixeltool|qcollectiongenerator|qdbus|qdbusviewer|qhelpconverter|qhelpgenerator|qtplugininfo)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt5
      ln -sv ${i} ${i}-qt5
      ;;
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

## work-in-progress... -- rex
%if 0%{?fedora} || 0%{?rhel} > 6
%check
export CMAKE_PREFIX_PATH=%{buildroot}%{_qt5_prefix}:%{buildroot}%{_prefix}
export PATH=%{buildroot}%{_qt5_bindir}:%{_qt5_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt5_libdir}
mkdir tests/auto/cmake/%{_target_platform}
pushd tests/auto/cmake/%{_target_platform}
cmake ..
ctest --output-on-failure ||:
popd
%endif


%files
%{_bindir}/qdbus-qt5
%{_bindir}/qtpaths
%{_qt5_bindir}/qdbus
%{_qt5_bindir}/qdbus-qt5
%{_qt5_bindir}/qtpaths

%files common
%doc LICENSE.LGPL*

%post   libs-clucene -p /sbin/ldconfig
%postun libs-clucene -p /sbin/ldconfig
%files  libs-clucene
%{_qt5_libdir}/libQt5CLucene.so.5*

%post   libs-designer -p /sbin/ldconfig
%postun libs-designer -p /sbin/ldconfig
%files  libs-designer
%{_qt5_libdir}/libQt5Designer.so.5*
%dir %{_qt5_libdir}/cmake/Qt5Designer/

%post   libs-designercomponents -p /sbin/ldconfig
%postun libs-designercomponents -p /sbin/ldconfig
%files  libs-designercomponents
%{_qt5_libdir}/libQt5DesignerComponents.so.5*

%post   libs-help -p /sbin/ldconfig
%postun libs-help -p /sbin/ldconfig
%files  libs-help
%{_qt5_libdir}/libQt5Help.so.5*

%post -n qt5-assistant
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n qt5-assistant
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun -n qt5-assistant
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files -n qt5-assistant
%{_bindir}/assistant-qt5
%{_qt5_bindir}/assistant*
%{_datadir}/applications/*assistant.desktop
%{_datadir}/icons/hicolor/*/apps/assistant*.*

%files -n qt5-designer-plugin-webkit
%{_qt5_plugindir}/designer/libqwebview.so
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_QWebViewPlugin.cmake

%post -n qt5-qdbusviewer
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n qt5-qdbusviewer
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun -n qt5-qdbusviewer
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files -n qt5-qdbusviewer
%{_bindir}/qdbusviewer*
%{_qt5_bindir}/qdbusviewer*
%{_datadir}/applications/*qdbusviewer.desktop
%{_datadir}/icons/hicolor/*/apps/qdbusviewer*.*

%post devel
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans devel
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun devel
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files devel
%{_bindir}/designer*
%{_bindir}/lconvert*
%{_bindir}/linguist*
%{_bindir}/lrelease*
%{_bindir}/lupdate*
%{_bindir}/pixeltool*
%{_bindir}/qcollectiongenerator*
%{_bindir}/qhelpconverter*
%{_bindir}/qhelpgenerator*
%{_bindir}/qtdiag*
%{_bindir}/qtplugininfo*
%{_qt5_bindir}/designer*
%{_qt5_bindir}/lconvert*
%{_qt5_bindir}/linguist*
%{_qt5_bindir}/lrelease*
%{_qt5_bindir}/lupdate*
%{_qt5_bindir}/pixeltool*
%{_qt5_bindir}/qtdiag*
%{_qt5_bindir}/qcollectiongenerator*
%{_qt5_bindir}/qhelpconverter*
%{_qt5_bindir}/qhelpgenerator*
%{_qt5_bindir}/qtplugininfo*
%{_qt5_headerdir}/QtCLucene/
%{_qt5_headerdir}/QtDesigner/
%{_qt5_headerdir}/QtDesignerComponents/
%{_qt5_headerdir}/QtHelp/
%{_qt5_headerdir}/QtUiPlugin
# phrasebooks used by linguist
%{_qt5_datadir}/phrasebooks/
%{_qt5_libdir}/libQt5CLucene.prl
%{_qt5_libdir}/libQt5CLucene.so
%{_qt5_libdir}/libQt5Designer*.prl
%{_qt5_libdir}/libQt5Designer*.so
%{_qt5_libdir}/libQt5Help.prl
%{_qt5_libdir}/libQt5Help.so
%{_qt5_libdir}/cmake/Qt5Designer/Qt5DesignerConfig*.cmake
%dir %{_qt5_libdir}/cmake/Qt5Help/
%{_qt5_libdir}/cmake/Qt5Help/Qt5HelpConfig*.cmake
%dir %{_qt5_libdir}/cmake/Qt5LinguistTools/
%{_qt5_libdir}/cmake/Qt5LinguistTools/Qt5LinguistToolsConfig*.cmake
%{_qt5_libdir}/cmake/Qt5LinguistTools/Qt5LinguistToolsMacros.cmake
%{_qt5_libdir}/cmake/Qt5UiPlugin/
%{_qt5_libdir}/pkgconfig/Qt5CLucene.pc
%{_qt5_libdir}/pkgconfig/Qt5Designer.pc
%{_qt5_libdir}/pkgconfig/Qt5DesignerComponents.pc
%{_qt5_libdir}/pkgconfig/Qt5Help.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri
%{_datadir}/applications/*designer.desktop
%{_datadir}/applications/*linguist.desktop
%{_datadir}/icons/hicolor/*/apps/designer*.*
%{_datadir}/icons/hicolor/*/apps/linguist*.*

# example designer plugins
%{_qt5_plugindir}/designer/libcontainerextension.so
%{_qt5_plugindir}/designer/libcustomwidgetplugin.so
%{_qt5_plugindir}/designer/libtaskmenuextension.so
%{_qt5_plugindir}/designer/libworldtimeclockplugin.so
%{_qt5_plugindir}/designer/libqquickwidget.so
%dir %{_qt5_libdir}/cmake/Qt5Designer/
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_AnalogClockPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_MultiPageWidgetPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_QQuickWidgetPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_TicTacToePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_WorldTimeClockPlugin.cmake

%files static
%{_qt5_headerdir}/QtUiTools/
%{_qt5_libdir}/libQt5UiTools.*a
%{_qt5_libdir}/libQt5UiTools.prl
%{_qt5_libdir}/cmake/Qt5UiTools/
%{_qt5_libdir}/pkgconfig/Qt5UiTools.pc

%if 0%{?docs}
%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtassistant.qch
%{_qt5_docdir}/qtassistant/
%{_qt5_docdir}/qtdesigner.qch
%{_qt5_docdir}/qtdesigner/
%{_qt5_docdir}/qthelp.qch
%{_qt5_docdir}/qthelp/
%{_qt5_docdir}/qtlinguist.qch
%{_qt5_docdir}/qtlinguist/
%{_qt5_docdir}/qtuitools.qch
%{_qt5_docdir}/qtuitools/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Mon Jun 15 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.2-1
- 5.4.2

* Sat May 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-3
- rebuild (gcc5)

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-2
- rebuild (gcc5)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Thu Feb 19 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.0-2
- rebuild (gcc5)

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Tue Dec 09 2014 Daniel Vrátil <dvratil@redhat.com> 5.4.0-0.10.rc
- fix icon name in qdbusviewer-qt5.desktop

* Sun Nov 30 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.4.0-0.9.rc
- install Linguist icon as linguist-qt5.png, fixes file conflict (#1169127)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.8.rc
- 5.4.0-rc

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.7.beta
- out-of-tree build, use %%qmake_qt5

* Fri Oct 31 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.6.beta
- respin system-clucene.patch

* Sun Oct 26 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.4.0-0.5.beta
- system-clucene patch: create path recursively in QtCLucene, CLucene can't

* Sun Oct 26 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.4.0-0.4.beta
- disable bootstrap (reenable -doc)
- system-clucene patch: drop -fpermissive flag
- system-clucene patch: use toLocal8Bit instead of toStdString
- system_clucene: BR clucene09-core-devel >= 0.9.21b-12 (-11 was broken)

* Sat Oct 25 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.4.0-0.3.beta
- libQt5Designer should be in a subpackage (#1156685)
- -doc: disable(boostrap for new clucene), drop dep on main pkg

* Sat Oct 25 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.4.0-0.2.beta
- BR and rebuild against reference-counting-enabled clucene09 (#1128293)

* Sat Oct 18 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta
- 5.4.0-beta

* Fri Oct 17 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-2
- -devel: Requires: qt5-designer-plugin-webkit

* Tue Sep 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- 5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.3.0-2
- restore system-clucene patch, rm the bundled copy

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- -examples subpkg

* Tue Jan 14 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- epel7 bootstrapped

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.5.beta1
- enable -doc only on primary archs (allow secondary bootstrap)

* Sat Nov 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- bootstrap ppc

* Tue Oct 01 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-6
- lupdate can't find qmake configuration file default (#1009893)

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-4
- use upstream cmake fix(es) (QTBUG-32570, #1006254)

* Wed Sep 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-3
- wrong path to lrelease (#1006254)
- %%check: first try

* Tue Sep 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-2
- ExclusiveArch: %{ix86} x86_64 %{arm}
- epel-6 love

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- qttools-5.1.1
- qt5-assistant, qt5-qdbusviewer, qt5-designer-plugin-webkit subpkgs (to match qt4)

* Mon Aug 19 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-4
- use system clucene09-core

* Mon Apr 29 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-3
- drop deprecated Encoding= key from .desktop files
- add justification for desktop vendor usage

* Fri Apr 19 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- add .desktop/icons for assistant, designer, linguist, qdbusviewer

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Mon Feb 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-2
- BR: pkgconfig(zlib)
- -static subpkg

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

