%define framework kfileaudiopreview
#%define snapshot 20140206

Name:           kf5-%{framework}
Version:        4.98.0
Release:        2.20140428git8e1768fd%{?dist}
Summary:        KDE Frameworks 5 Tier 4 addon with audio preview functionality
License:        LGPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kfileaudiopreview-8e1768fd.tar



BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  phonon-qt5-devel

BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kdoctools-devel

Requires:       kf5-filesystem

%description
This is a plugin for KIO that provides a component for previewing audio
files, for example in the Open File dialog.


%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING.LIB README.md
%{_kf5_qtplugindir}/kf5/kfileaudiopreview.so


%changelog
* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140428git8e1768fd
- Update to git: 8e1768fd

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428git8e1768fd
- Update to git: 8e1768fd

* Wed Apr 23 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140423gitb993448a
- Update to git: b993448a

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git4386c6f4
- Update to git: 4386c6f4

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Thu Feb 06 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140206git
- Update to pre-relase snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Thu Jan 9 2014 Lukáš Tinkl <ltinkl@redhat.com>
- initial version
