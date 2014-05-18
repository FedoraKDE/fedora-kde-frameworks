Name:           kde5
Version:        4.90.3
Release:        2%{?dist}
Summary:        Filesystem and RPM macros for KDE 5 and Plasma Workspaces 2
BuildArch:      noarch

License:        BSD
URL:            http://www.kde.org

Source0:        macros.kde5

%description
Filesystem and RPM macros for KDE 5 and Plasma Workspaces 2


%package        filesystem
Summary:        Filesystem for KDE 5 applications
%description    filesystem
Filesystem for KDE 5 applications.

%package        rpm-macros
Summary:        RPM macros for KDE 5 applications
%description    rpm-macros
RPM macros for building KDE 5 applications.


%install
mkdir -p %{buildroot}/usr/libexec/kde5
mkdir -p %{buildroot}/usr/%{_lib}/qt5/plugins/kde5

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d/
install -pm644 %{_sourcedir}/macros.kde5 %{buildroot}%{_rpmconfigdir}/macros.d

%files filesystem
/usr/libexec/kde5
/usr/%{_lib}/qt5/plugins/kde5

%files rpm-macros
%{_rpmconfigdir}/macros.d/macros.kde5


%changelog
* Sun May 18 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.3-2
- Add /usr/share to XDG_DATA_DIRS

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.3-1
- split to -filesystem and -rpm-macros

* Thu Feb 13 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.2
- initial version (forked from kf5-filesystem which now points to /usr)

