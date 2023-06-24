%global greeter gtkgreet

Name:           greetd-%{greeter}
Version:        0.7
Release:        0.2%{?dist}
Summary:        GTK based greeter for greetd

License:        GPLv3
URL:            https://git.sr.ht/~kennylevinsen/%{greeter}
#Source0:        %{url}/archive/%{version}.tar.gz#/%{greeter}-%{version}.tar.gz
# Desktop session file support - https://todo.sr.ht/~kennylevinsen/gtkgreet/8
#Source100:      %{greeter}-update-environments
#Source101:      %{greeter}.css
#Source102:      %{greeter}-sway.conf
#Source103:      %{greeter}-wayfire.ini
#Source104:      %{greeter}-river-init
# Fix -Wsign-compare error on 32-bit systems
#Patch0:         %{url}/commit/b8218e3.patch#/proto-fix-signed-ness-error.patch
#Patch1:         %{url}/commit/3471aaa.patch#/proto-use-uint32_t-offsets-and-message-lengths.patch

BuildRequires:  gcc
BuildRequires:  meson >= 0.47
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk-layer-shell-0)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(scdoc) >= 1.9.7

Requires:       greetd >= 0.6
Provides:       greetd-greeter = 0.6
# gtkgreet requires a wayland compositor
Requires:       (sway or wayfire or river or cage or hyprland)
Suggests:       sway

# Terminates the compositor once the greeter is done
Recommends:     wayland-logout

%description
%{summary}.


%prep
#%autosetup -p1 -n %{greeter}-%{version}
cd %{_builddir}
git clone %{URL}.git ./ --recursive
%_fixperms .


%build
%meson
%meson_build


%install
%meson_install

#install -D -m755 -vp %{SOURCE100} %{buildroot}%{_libexecdir}/gtkgreet-update-environments
#install -D -m644 -vp %{SOURCE101} %{buildroot}%{_sysconfdir}/gtkgreet/gtkgreet.css
#install -D -m644 -vp %{SOURCE102} %{buildroot}%{_sysconfdir}/gtkgreet/gtkgreet-sway.conf
#install -D -m644 -vp %{SOURCE103} %{buildroot}%{_sysconfdir}/gtkgreet/gtkgreet-wayfire.ini
# River config is an executable that talks with river via riverctl or wayland
# protocol and starts the apps
#install -D -m755 -vp %{SOURCE104} %{buildroot}%{_sysconfdir}/gtkgreet/gtkgreet-river-init

mkdir -p %{buildroot}%{_sysconfdir}/greetd
touch %{buildroot}%{_sysconfdir}/greetd/environments


%post
# initialize list of session commands
if [ ! -f %{_sysconfdir}/greetd/environments ]; then
    %{_libexecdir}/gtkgreet-update-environments -w %{_sysconfdir}/greetd/environments
fi
exit 0


%files
%doc README.md
%license LICENSE
%dir %{_sysconfdir}/gtkgreet
%config %ghost     %{_sysconfdir}/greetd/environments
%config(noreplace) %{_sysconfdir}/gtkgreet/gtkgreet.css
%config(noreplace) %{_sysconfdir}/gtkgreet/gtkgreet-sway.conf
%config(noreplace) %{_sysconfdir}/gtkgreet/gtkgreet-wayfire.ini
%config(noreplace) %{_sysconfdir}/gtkgreet/gtkgreet-river-init
%{_bindir}/gtkgreet
%{_libexecdir}/gtkgreet-update-environments
%{_mandir}/man1/gtkgreet.1*


%changelog
* Sat Apr 30 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.7-0.2
- Add upstream patches to fix 32-bit builds
- Cleanup spec and configs for review
- Breaking: move compositor configuration files to /etc/gtkgreet/

* Tue Dec 22 2020 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.7-0.1
- Update to 0.7

* Mon Nov 23 2020 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.6-0.3
- Add helper script for populating environments file

* Thu Oct 29 2020 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.6-0.2
- Add wayfire config and make gtkgreet depend on any of sway, wayfire or cage

* Thu Sep 17 2020 Aleksei Bavshin <alebastr89@gmail.com> - 0.6-0.1
- Rename and refactor spec

* Tue Jul 14 2020 Aleksei Bavshin <alebastr89@gmail.com> - 0.6-1
- Initial package 

