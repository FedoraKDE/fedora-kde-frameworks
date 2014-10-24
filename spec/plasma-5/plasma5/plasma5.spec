Name:           plasma5
Version:        5.1.0.1
Release:        4%{?dist}
Summary:        The next generation Plasma workspace from the KDE Community

License:        GPLv2+
URL:            http://www.kde.org

# Nicer name
Provides:       plasma-5 = %{version}-%{release}

Requires:       plasma-breeze
Requires:       plasma-breeze-kde4
Requires:       plasma-desktop
Requires:       plasma-workspace
Requires:       plasma-workspace-wallpapers
Requires:       plasma-oxygen
Requires:       plasma-oxygen-kde4
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
Requires:       khotkeys
Requires:       ksysguard

Requires:       kmix
Requires:       kwalletmanager
Requires:       kscreen

%description
%{summary}.

%prep

%build

%install

%files


%changelog
* Thu Oct 23 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-4
- Requires: kmix, kwalletmanager, kscreen

* Thu Oct 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-3
- Requires: ksysguard

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

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
