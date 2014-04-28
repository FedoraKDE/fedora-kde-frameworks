Name:           kf5
Version:        4.98.0
Release:        9
Summary:        Filesystem and RPM macros for KDE Frameworks 5
BuildArch:      noarch
License:        BSD
URL:            http://www.kde.org

Source0:        macros.kf5

%description
Filesystem and RPM macros for KDE Frameworks 5

%package        filesystem
Summary:        Filesystem for KDE Frameworks 5
%description    filesystem
Filesystem for KDE Frameworks 5.

%package        rpm-macros
Summary:        RPM macros for KDE Frameworks 5
%description    rpm-macros
RPM macros for building KDE Frameworks 5 packages.


%install
# See macros.kf5 where the directories are specified
mkdir -p %{buildroot}%{_libdir}/qt5/plugins/kf5
mkdir -p %{buildroot}%{_includedir}/KF5
mkdir -p %{buildroot}%{_libexecdir}/kf5

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d/
install -pm644 %{_sourcedir}/macros.kf5 %{buildroot}%{_rpmconfigdir}/macros.d


%files filesystem
%{_libdir}/qt5/plugins/kf5
%{_includedir}/KF5
%{_libexecdir}/kf5


%files rpm-macros
%{_rpmconfigdir}/macros.d/macros.kf5


%changelog
* Mon Apr 28 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-8
- Remove INCLUDE_INSTALL_DIR, since we use the default one

* Tue Apr 22 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-7
- Make DATA_INSTALL_DIR relative, so that CMake config files don't point to /usr/usr/share

* Tue Apr 22 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-6
- Explicitly set BIN_INSTALL_DIR to be absolute, otherwise CMake complains

* Mon Apr 21 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-5
- Fix _kf5_sysconfdir and set some install paths in cmake_kf5

* Wed Apr 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-4
- Rename base package to kf5
- Create -filesystem, -rpm-macros subpackges

* Fri Apr 11 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-3
- Fix build
- Use %%global instead of %%define
- Use install instead of cp

* Fri Apr 11 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-2
- Fix some installation dirs in the macros.kf5 file

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 2 (4.97.0)

* Thu Feb 13 2014 Daniel Vrátil <dvraitl@redhat.com> 4.96.0-2
- Remove unnecessary mkdirs

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-release snapshot of 4.96.0

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-4
- fix definition of QT_PLUGIN_INSTALL_DIR in RPM macros

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-2
- fix install dirs definitions in RPM macros

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Tue Jan  7 2014 Daniel Vrátil <dvratil@redhat.com>
- export XDG_DATA_DIRS

* Mon Jan  6 2014 Daniel Vrátil <dvratil@redhat.com>
- alter XDG_DATA_DIRS in cmake_kf5 RPM macro
- add _kf5_mandir RPM macro

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version

