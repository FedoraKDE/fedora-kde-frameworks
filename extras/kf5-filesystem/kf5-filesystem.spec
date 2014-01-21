%define framework filesystem

Name:           kf5-%{framework}
Version:        4.95.0
Release:        4%{?dist}
Summary:        Filesystem and RPM macros for KDE Frameworks 5
BuildArch:      noarch

License:        BSD
URL:            http://www.kde.org

Source0:        macros.kf5

%description
Filesystem and RPM macros for KDE Frameworks 5

%install
mkdir -p %{buildroot}/opt/kf5/{,bin,share,doc,include,%{_lib},libexec,qt5/plugins,etc}
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d/
cp %{_sourcedir}/macros.kf5 %{buildroot}%{_rpmconfigdir}/macros.d

%files
%{_rpmconfigdir}/macros.d/macros.kf5
/opt/kf5

%changelog
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

