Name:           kmenuedit
Version:        5.2.95
Release:        1%{?dist}
Summary:        KDE menu editor

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/kmenuedit

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kdoctools-devel

BuildRequires:  desktop-file-utils

Requires:       kf5-filesystem

# TODO: Remove once kmenuedit is split from kde-workspace
Conflicts:      kde-workspace < 5.0.0-1

%description
%{summary}.

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
%find_lang kmenuedit5 --with-qt --with-kde --all-name

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.kde.kmenuedit.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f kmenuedit5.lang
%doc COPYING COPYING.DOC
%{_bindir}/kmenuedit
%{_kf5_libdir}/libkdeinit5_kmenuedit.so
%{_datadir}/kmenuedit
%{_datadir}/applications/org.kde.kmenuedit.desktop
%{_datadir}/icons/hicolor/*/apps/kmenuedit.png
%{_kf5_datadir}/kxmlgui5/kmenuedit
%{_docdir}/HTML/*/kmenuedit


%changelog
* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Tue Jan 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-2.beta
- add icon scriptlets

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

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

* Tue Aug 05 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- Fix Obsoletes

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Sun May 18 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0.2-20140514git1b86b1a
- Rebuild due to build-id conflict with kf5-kded

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140514git1b86b1a
- Intial snapshot
