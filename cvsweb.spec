Summary:	Visual (www) interface to explore a cvs repository
Summary(pl):	Wizualny (WWW) interfejs do przegl±dania repozytorium cvs
Name:		cvsweb
Version:	3.0.1
Release:	1
Epoch:		1
License:	BSD
Group:		Development/Tools
Source0:	http://people.FreeBSD.org/~scop/cvsweb/%{name}-%{version}.tar.gz
# Source0-md5:	08cc35e620773517b392bea4fc1e9f6b
URL:	http://www.freebsd.org/projects/cvsweb.html
Patch0:		%{name}-config.patch
Patch1:		%{name}-fix_perl_options.patch
Requires:	perl(Cwd)
Requires:	perl(File::Basename)
Requires:	perl(File::Path)
Requires:	perl(File::Spec::Functions)
Requires:	perl(File::Temp)
Requires:	perl(IPC::Run)
Requires:	perl(Time::Local)
Requires:	perl(URI::Escape)
Requires:	rcs
Requires:	webserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildArch:	noarch

%description
cvsweb is a visual (www) interface to explore a cvs repository. This
is an enhanced cvsweb developed by Henner Zeller. Enhancements include
recognition and display of popular mime-types, visual, color-coded,
side by side diffs of changes and the ability sort the file display
and to hide old files from view. One living example of the enhanced
cvsweb is the KDE cvsweb.

cvsweb requires the server to have cvs and a cvs repository worth
exploring.

%description -l pl
cvsweb jest wizualnym interfejsem do eksploracji repozytorium cvs.
Jest to ulepszona wersja programu cvsweb Hennera Zellera. Do ulepszeñ
zaliczyæ mo¿na rozpoznawanie i wy¶wietlanie popularnych typów MIME;
wizualnych, kolorowych, umieszczonych obok siebie ró¿nic miêdzy
plikami oraz zdolno¶æ sortowania widoku plików oraz ukrywania starych
plików. ¯ywym przyk³adem ulepszonego cvsweba jest cvsweb projektu KDE.

cvsweb wymaga, by na serwerze by³ zainstalowany CVS oraz repozytorium
CVS warte eksploracji.

%define _cgibindir /home/services/httpd/cgi-bin
%define _appdir	 %{_datadir}/%{name}

%prep
%setup -q
%patch0 -p1
# no longer needed? See http://tinyurl.com/5ebn3
#%%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_appdir}/{css,enscript,icons},%{_cgibindir},%{_sysconfdir}/httpd}

install %{name}.cgi	$RPM_BUILD_ROOT%{_cgibindir}
install %{name}.conf	$RPM_BUILD_ROOT%{_sysconfdir}
install css/*		$RPM_BUILD_ROOT%{_appdir}/css
install enscript/*	$RPM_BUILD_ROOT%{_appdir}/enscript
install icons/*		$RPM_BUILD_ROOT%{_appdir}/icons
install cvsweb.conf*	$RPM_BUILD_DIR/%{name}-%{version}/samples


echo "Alias /%{name}  %{_appdir}" > $RPM_BUILD_ROOT%{_sysconfdir}/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" %{_sysconfdir}/httpd/httpd.conf; then
	echo "Include %{_sysconfdir}/httpd/%{name}.conf" >> %{_sysconfdir}/httpd/httpd.conf
elif [ -d %{_sysconfdir}/httpd/httpd.conf ]; then
	 ln -sf %{_sysconfdir}/httpd/%{name}.conf %{_sysconfdir}/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	%{_sbindir}/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d %{_sysconfdir}/httpd/httpd.conf ]; then
		rm -f %{_sysconfdir}/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" %{_sysconfdir}/httpd/httpd.conf > \
			%{_sysconfdir}/httpd/httpd.conf.tmp
		mv -f %{_sysconfdir}/httpd/httpd.conf.tmp %{_sysconfdir}/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			%{_sbindir}/apachectl restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL NEWS README TODO samples
%attr(755,root,root) %{_cgibindir}/cvsweb.cgi
%{_datadir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/%{name}.conf
