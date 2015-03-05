%global git_date 20150305
%global git_commit 2723f4c

Name:           kaccounts-providers
Version:        1.0
Release:        3.%{git_date}git%{git_commit}%{?dist}
Summary:        Additional service providers for KAccounts framework
License:        LGPLv2
URL:            https://projects.kde.org/projects/kdereview/kaccounts-providers
BuildArch:      noarch

# git archive --format=tar.gz --remote=git://anongit.kde.org/kaccounts-providers.git \
#             --prefix=kaccounts-providers-%%{version}/ --output=kaccounts-providers-%%{git_commit}.tar.gz \
#             %%{git_commit}

Source0:        kaccounts-providers-%{git_commit}.tar.gz

BuildRequires:  extra-cmake-modules

BuildRequires:  intltool
BuildRequires:  libaccounts-glib-devel

%description
%{summary}.

%prep
%setup -q -n kaccounts-providers-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%files
%doc COPYING
%{_datadir}/accounts/providers/*.provider
%{_sysconfdir}/signon-ui/webkit-options.d

%changelog
* Thu Mar 05 2015 Daniel Vrátil <dvratil@redhat.com> - 1.0.0-3.20150305git2723f4c
- update to latest git snapshot

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 1.0.0-2.20150122git0c2e1aa
- add icon scriptlets

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 1.0.0-1.20150122git0c2e1aa
- Initial version
