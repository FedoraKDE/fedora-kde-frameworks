%global framework filesystem

Name:           kf5-%{framework}
Version:        4.98.0
Release:        3
Summary:        Filesystem and RPM macros for KDE Frameworks 5
BuildArch:      noarch

License:        BSD
URL:            http://www.kde.org

Source0:        macros.kf5

%description
Filesystem and RPM macros for KDE Frameworks 5

%install
# See macros.kf5 where the directories are specified
mkdir -p %{buildroot}%{_includedir}/kf5
mkdir -p %{buildroot}%{_libdir}/kf5/plugins
mkdir -p %{buildroot}%{_datadir}/kf5

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d/
install -pm644 %{_sourcedir}/macros.kf5 %{buildroot}%{_rpmconfigdir}/macros.d

%files
%{_rpmconfigdir}/macros.d/macros.kf5
%{_includedir}/kf5
%{_libdir}/kf5/plugins
%{_datadir}/kf5

%changelog
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

