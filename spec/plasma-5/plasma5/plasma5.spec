Name:           plasma5
Version:        5.1.0
Release:        1%{?dist}
Summary:        The next generation Plasma workspace from the KDE Community

License:        GPLv2+
URL:            http://www.kde.org

Requires:       plasma-breeze
Requires:       plasma-desktop
Requires:       plasma-workspace
Requires:       plasma-workspace-wallpapers
Requires:       plasma-oxygen
Requires:       plasma-milou
Requires:       plasma-nm
Requires:       plasma-systemsettings
Requires:       kwin
Requires:       kwrited
Requires:       powerdevil
Requires:       kio-extras
Requires:       kinfocenter
Requires:       kmenuedit
Requires:       kde-cli-tools
Requires:       khelpcenter
Requires:       kf5-baloo

%description
%{summary}.

%prep

%build

%install

%files


%changelog
* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Wed Aug 20 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-2
- Missed some requires

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Wed Jul 23 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0
