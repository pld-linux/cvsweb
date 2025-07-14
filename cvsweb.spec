Summary:	Visual (www) interface to explore a CVS repository
Summary(pl.UTF-8):	Wizualny (WWW) interfejs do przeglądania repozytorium CVS
Name:		cvsweb
Version:	3.0.6
Release:	8
Epoch:		1
License:	BSD
Group:		Development/Tools
Source0:	http://people.FreeBSD.org/~scop/cvsweb/%{name}-%{version}.tar.gz
# Source0-md5:	0e1eec962b1db00e01b295fff84b6e89
Source1:	%{name}-apache.conf
URL:		http://www.freebsd.org/projects/cvsweb.html
Patch0:		%{name}-config.patch
Patch1:		%{name}-emptyscript.patch
Patch2:		cveurl.patch
Patch3:		cvsnt.patch
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	diffutils
# for %{_prefix}/lib/cgi-bin
Requires:	filesystem >= 3.0-11
# for /etc/mime.types
Requires:	mailcap
Requires:	rcs
Requires:	webapps
Requires:	webserver(access)
Conflicts:	apache-base < 2.2.0-8
Conflicts:	apache1 < 1.3.34-6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{name}
%define		_cgibindir	%{_prefix}/lib/cgi-bin
%define		_enscriptdir	%{_datadir}/enscript/hl

%description
CVSweb is a WWW interface for CVS repositories with which you can
browse a file hierarchy on your browser to view each file's revision
history in a very handy manner. CVSweb was originally written by Bill
Fenner for the FreeBSD Project. FreeBSD-CVSweb, formerly known as
knu-CVSweb, is an enhanced version of CVSweb based on Henner Zeller's
CVSweb, which is an extended version of the original CVSweb. This
version contains numerous cleanups, bug-fixes, security enhancements
and feature improvements.

%description -l pl.UTF-8
CVSweb jest interfejsem WWW dla repozytoriów CVS dzięki któremu można
przeglądać ich zawartość w przeglądarce WWW widząc pełną historię
zmian i numerów rewizji dla każdego z plików. CVSWeb został stworzony
przez Billa Fennera dla projektu FreeBSD. FreeBSD-CVSweb dawniej znany
jako knu-CVSweb jest rozszerzoną wersją opartą na wersji Hennera
Zellera, która z kolei była oparta na oryginalnej wersji. Kod obecnej
wersji został uporządkowany i oczyszczony, usuniętych zostało również
wiele błędów. Wprowadzono także dużo poprawek bezpieczeństwa oraz
rozbudowano funkcjonalność.

%package -n enscript-%{name}
Summary:	Enscript language files for CVSweb
Summary(pl.UTF-8):	Pliki języka Enscript dla CVSweba
Group:		Applications/Publishing
Requires:	enscript >= 1.6.4-1.2

%description -n enscript-%{name}
Enscript language files for CVSweb.

%description -n enscript-%{name} -l pl.UTF-8
Pliki języka Enscript dla CVSweba.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

cp -a cvsweb.conf* samples

# remove backups
find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir}/{css,icons},%{_cgibindir},%{_enscriptdir},%{_sysconfdir}}

install %{name}.cgi	$RPM_BUILD_ROOT%{_cgibindir}
install css/*		$RPM_BUILD_ROOT%{_appdir}/css
install enscript/*	$RPM_BUILD_ROOT%{_enscriptdir}
install icons/*		$RPM_BUILD_ROOT%{_appdir}/icons

install %{name}.conf	$RPM_BUILD_ROOT%{_sysconfdir}
echo '# vim:syn=perl' >> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
%banner %{name} -e <<'EOF'
You might want to install optionally 'cvsgraph' program.
EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerpostun -- %{name} < 1:3.0.6-0.2
# rescue app config
if [ -f /etc/%{name}/cvsweb.conf.rpmsave ]; then
	mv -f %{_sysconfdir}/cvsweb.conf{,.rpmnew}
	mv -f /etc/%{name}/cvsweb.conf.rpmsave %{_sysconfdir}/cvsweb.conf
fi

# migrate from old config location (only apache2, as there was no apache1 support)
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/httpd.conf
	httpd_reload=1
fi

# migrate from apache-config macros
if [ -f /etc/%{name}/apache.conf.rpmsave ]; then
	if [ -d /etc/apache/webapps.d ]; then
		cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
		cp -f /etc/%{name}/apache.conf.rpmsave %{_sysconfdir}/apache.conf
	fi

	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
		cp -f /etc/%{name}/apache.conf.rpmsave %{_sysconfdir}/httpd.conf
	fi
	rm -f /etc/%{name}/apache.conf.rpmsave
fi

if [ -L /etc/apache/conf.d/09_%{name}.conf ]; then
	rm -f /etc/apache/conf.d/09_%{name}.conf
	apache_reload=1
fi
if [ -L /etc/apache/conf.d/79_%{name}.conf ]; then
	rm -f /etc/apache/conf.d/79_%{name}.conf
	apache_reload=1
fi
if [ -L /etc/httpd/httpd.conf/09_%{name}.conf ]; then
	rm -f /etc/httpd/httpd.conf/09_%{name}.conf
	httpd_reload=1
fi

if [ "$apache_reload" ]; then
	/usr/sbin/webapp register apache %{_webapp}
	%service -q apache reload
fi
if [ "$httpd_reload" ]; then
	/usr/sbin/webapp register httpd %{_webapp}
	%service -q httpd reload
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL NEWS README TODO samples
%dir %attr(750,root,http) %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,http) %{_sysconfdir}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,root) %{_sysconfdir}/apache.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,root) %{_sysconfdir}/httpd.conf
%attr(755,root,root) %{_cgibindir}/cvsweb.cgi
%{_appdir}

%files -n enscript-%{name}
%defattr(644,root,root,755)
%{_enscriptdir}/*
