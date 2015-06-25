
%global qt_module qttranslations

%define pre rc

Summary: Qt5 - QtTranslations module
Name:    qt5-%{qt_module}
Version: 5.5.0
Release: 0.2.rc%{?dist}

License: LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
Url:     http://www.qt.io
Source0: http://download.qt.io/development_releases/qt/5.5/%{version}%{?pre:-%{pre}}/submodules/%{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}.tar.xz

BuildArch: noarch

BuildRequires: qt5-qttools-devel >= %{version}

# help system-config-language and dnf/yum langpacks pull these in
%if 0%{?_qt5:1}
Provides: %{_qt5}-ar = %{version}-%{release}
Provides: %{_qt5}-ca = %{version}-%{release}
Provides: %{_qt5}-cs = %{version}-%{release}
Provides: %{_qt5}-da = %{version}-%{release}
Provides: %{_qt5}-de = %{version}-%{release}
Provides: %{_qt5}-es = %{version}-%{release}
Provides: %{_qt5}-fa = %{version}-%{release}
Provides: %{_qt5}-fi = %{version}-%{release}
Provides: %{_qt5}-fr = %{version}-%{release}
Provides: %{_qt5}-gl = %{version}-%{release}
Provides: %{_qt5}-he = %{version}-%{release}
Provides: %{_qt5}-hu = %{version}-%{release}
Provides: %{_qt5}-it = %{version}-%{release}
Provides: %{_qt5}-ja = %{version}-%{release}
Provides: %{_qt5}-ko = %{version}-%{release}
Provides: %{_qt5}-lt = %{version}-%{release}
Provides: %{_qt5}-lv = %{version}-%{release}
Provides: %{_qt5}-pl = %{version}-%{release}
Provides: %{_qt5}-pt = %{version}-%{release}
Provides: %{_qt5}-ru = %{version}-%{release}
Provides: %{_qt5}-sk = %{version}-%{release}
Provides: %{_qt5}-sl = %{version}-%{release}
Provides: %{_qt5}-sv = %{version}-%{release}
Provides: %{_qt5}-uk = %{version}-%{release}
Provides: %{_qt5}-zh_CN = %{version}-%{release}
Provides: %{_qt5}-zn_TW = %{version}-%{release}
%endif

%description
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}

%build
qmake-qt5
make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

# not used currently, since we track locales manually to keep %files/Provides sync'd -- rex
%find_lang %{name} --all-name --with-qt --without-mo

%files
%doc LICENSE.LGPL* LGPL_EXCEPTION.txt
%lang(ar) %{_qt5_translationdir}/*_ar.qm
%lang(ca) %{_qt5_translationdir}/*_ca.qm
%lang(cs) %{_qt5_translationdir}/*_cs.qm
%lang(da) %{_qt5_translationdir}/*_da.qm
%lang(de) %{_qt5_translationdir}/*_de.qm
%lang(es) %{_qt5_translationdir}/*_es.qm
%lang(fa) %{_qt5_translationdir}/*_fa.qm
%lang(fi) %{_qt5_translationdir}/*_fi.qm
%lang(fr) %{_qt5_translationdir}/*_fr.qm
%lang(gl) %{_qt5_translationdir}/*_gl.qm
%lang(he) %{_qt5_translationdir}/*_he.qm
%lang(hu) %{_qt5_translationdir}/*_hu.qm
%lang(it) %{_qt5_translationdir}/*_it.qm
%lang(ja) %{_qt5_translationdir}/*_ja.qm
%lang(ko) %{_qt5_translationdir}/*_ko.qm
%lang(lt) %{_qt5_translationdir}/*_lt.qm
%lang(lt) %{_qt5_translationdir}/*_lv.qm
%lang(pl) %{_qt5_translationdir}/*_pl.qm
%lang(pt) %{_qt5_translationdir}/*_pt.qm
%lang(ru) %{_qt5_translationdir}/*_ru.qm
%lang(sk) %{_qt5_translationdir}/*_sk.qm
%lang(sl) %{_qt5_translationdir}/*_sl.qm
%lang(sv) %{_qt5_translationdir}/*_sv.qm
%lang(uk) %{_qt5_translationdir}/*_uk.qm
%lang(zh_CN) %{_qt5_translationdir}/*_zh_CN.qm
%lang(zh_TW) %{_qt5_translationdir}/*_zh_TW.qm


%changelog
* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Wed Jun 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1

* Thu Jun 04 2015 Jan Grulich <jgrulich@redhat.com> 5.4.2-1
- 5.4.2

* Thu Mar 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- Provides: qt5-qtbase-<locales> to aid dnf/yum langpacks plugin and system-config-language (#1170730)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.rc
- 5.4.0-rc

* Mon Oct 20 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta
- 5.4.0-beta

* Wed Sep 17 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.3.2-1
- 5.3.2

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.beta1
- 5.2.0-beta1

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha

* Sun Sep 22 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- Initial packaging
