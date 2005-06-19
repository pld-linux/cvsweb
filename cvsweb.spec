%include	/usr/lib/rpm/macros.perl
Summary:	Visual (www) interface to explore a CVS repository
Summary(pl):	Wizualny (WWW) interfejs do przegl±dania repozytorium CVS
Name:		cvsweb
Version:	3.0.5
Release:	0.15
Epoch:		1
License:	BSD
Group:		Development/Tools
Source0:	http://people.FreeBSD.org/~scop/cvsweb/%{name}-%{version}.tar.gz
# Source0-md5:	572dbb2d66ad6487c0a3536f93023086
URL:		http://www.freebsd.org/projects/cvsweb.html
Patch0:		%{name}-config.patch
# for %{_prefix}/lib/cgi-bin
Requires:	FHS >= 2.3-8
BuildRequires:	rpmbuild(macros) >= 1.223
Requires:	rcs
# for /etc/mime.types
Requires:	mailcap
Requires:	webserver
# because of wrong module load order
Conflicts:	apache1 < 1.3.33-6.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_appdir		%{_datadir}/%{name}
%define		_cgibindir	%{_prefix}/lib/cgi-bin

%description
CVSweb is a WWW interface for CVS repositories with which you can
browse a file hierarchy on your browser to view each file's revision
history in a very handy manner. CVSweb was originally written by Bill
Fenner for the FreeBSD Project. FreeBSD-CVSweb, formerly known as
knu-CVSweb, is an enhanced version of CVSweb based on Henner Zeller's
CVSweb, which is an extended version of the original CVSweb. This
version contains numerous cleanups, bug-fixes, security enhancements
and feature improvements.

%description -l pl
CVSweb jest interfejsem WWW dla repozytoriów CVS dziêki któremu mo¿na
przegl±daæ ich zawarto¶æ w przegl±darce WWW widz±c pe³n± historiê
zmian i numerów rewizji dla ka¿dego z plików. CVSWeb zosta³ stworzony
przez Billa Fennera dla projektu FreeBSD. FreeBSD-CVSweb dawniej znany
jako knu-CVSweb jest rozszerzon± wersj± opart± na wersji Hennera
Zellera, która z kolei by³a oparta na oryginalnej wersji. Kod obecnej
wersji zosta³ uporz±dkowany i oczyszczony, usuniêtych zosta³o równie¿
wiele b³êdów. Wprowadzono tak¿e du¿o poprawek bezpieczeñstwa oraz
rozbudowano funkcjonalno¶æ.

%prep
%setup -q
%patch0 -p1

install cvsweb.conf* samples

# remove backups
find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_appdir}/{css,enscript,icons},%{_cgibindir},%{_sysconfdir}}

install %{name}.cgi	$RPM_BUILD_ROOT%{_cgibindir}
install css/*		$RPM_BUILD_ROOT%{_appdir}/css
install enscript/*	$RPM_BUILD_ROOT%{_appdir}/enscript
install icons/*		$RPM_BUILD_ROOT%{_appdir}/icons

install %{name}.conf	$RPM_BUILD_ROOT%{_sysconfdir}
echo '# vim:syn=perl' >> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

cat <<EOF > $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
Alias /%{name}/ %{_appdir}/
ScriptAlias /cgi-bin/%{name}.cgi %{_cgibindir}/%{name}.cgi

<Location /cgi-bin/cvsweb.cgi>
   # See also $charset in cvsweb.conf.
   #AddDefaultCharset UTF-8

   # mod_perl >= 1.99:
   <IfModule mod_perl.c>
	   SetHandler perl-script
	   PerlResponseHandler ModPerl::Registry
	   PerlOptions +ParseHeaders
	   Options ExecCGI
   </IfModule>
</Location>

# vim: filetype=apache ts=4 sw=4 et
EOF

%post
if [ "$1" = 1 ]; then
%banner %{name} -e <<'EOF'
You might want to install optionally 'cvsgraph' program.
EOF
fi

%clean
rm -rf $RPM_BUILD_ROOT

# 09_ instead of 99_ is for ScriptAlias /cgi-bin/cvsweb.cgi ...
%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache.conf -n 09

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1 -n 09

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache.conf -n 09

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2 -n 09

%triggerpostun -- %{name} < 1:3.0.5-0.11
# migrate from old config location (only apache2, as there was no apache1 support)
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/apache.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

# place new config location, as trigger puts config only on first install, do it here.
# apache1
if [ -d /etc/apache/conf.d ]; then
	ln -sf %{_sysconfdir}/apache.conf /etc/apache/conf.d/09_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi
# apache2
if [ -d /etc/httpd/httpd.conf ]; then
	ln -sf %{_sysconfdir}/apache.conf /etc/httpd/httpd.conf/09_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL NEWS README TODO samples
%dir %attr(750,root,http) %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,http) %{_sysconfdir}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,root) %{_sysconfdir}/apache.conf
%attr(755,root,root) %{_cgibindir}/cvsweb.cgi
%{_datadir}/%{name}
