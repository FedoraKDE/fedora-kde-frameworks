Name:           plasma5
Version:        5.2.0
Release:        2%{?dist}
Summary:        The next generation Plasma workspace from the KDE Community

License:        GPLv2+
URL:            http://www.kde.org

BuildArch:      noarch

# Nicer name
Provides:       plasma-5 = %{version}-%{release}


# Shell
Requires:       plasma-desktop
Requires:       plasma-workspace
Requires:       plasma-workspace-wallpapers
Requires:       plasma-oxygen
Requires:       plasma-breeze
Requires:       breeze-icon-theme
Requires:       plasma-milou
Requires:       plasma-nm
Requires:       kdeplasma-addons

# Configuration
Requires:       plasma-systemsettings
#Requires:       kcm-gtk
Requires:       sddm-kcm
#Requires:       kcm-user-manager

# Daemons
Requires:       powerdevil
Requires:       kwrited
Requires:       kf5-baloo
Requires:       kio-extras
Requires:       khotkeys
Requires:       kscreen
Requires:       ksshaskpass
Requires:       polkit-kde

# Apps & utils
Requires:       kwin
Requires:       khelpcenter
Requires:       kinfocenter
Requires:       kmenuedit
Requires:       kde-cli-tools
Requires:       ksysguard

# KDE4 compat
Requires:       kde-style-breeze


# Unstable/unreleased apps
Requires:       kmix
Requires:       kwalletmanager


%description
%{summary}.

%prep

%build

%install

%check

%files


%changelog
* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-2
- temporarily disable kcm-gtk and kcm-user-manager

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-2.beta
- kcm-sddm renamed to sddm-kcm
- Requires: breeze-icon-theme (should be required by plasma-breeze probably)

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Thu Nov 13 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-2
- Adapt to changes in plasma-oxygen packaging

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

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
