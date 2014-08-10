Name:           plasma5
Version:        5.0.1
Release:        1%{?dist}
Summary:        The next generation Plasma workspace from the KDE Community

License:        GPLv2+
URL:            http://www.kde.org

Requires:       plasma-breeze
Requires:       plasma-desktop
Requires:       plasma-workspace
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

%description
%{summary}.

%prep

%build

%install

%files


%changelog
* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Wed Jul 23 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0
