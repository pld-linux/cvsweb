%include	/usr/lib/rpm/macros.perl
Summary:	Visual (www) interface to explore a cvs repository
Summary(pl):	Wizualny (WWW) interfejs do przegl±dania repozytorium cvs
Name:		cvsweb
Version:	3.0.5
Release:	0.2
Epoch:		1
License:	BSD
Group:		Development/Tools
Source0:	http://people.FreeBSD.org/~scop/cvsweb/%{name}-%{version}.tar.gz
# Source0-md5:	572dbb2d66ad6487c0a3536f93023086
URL:		http://www.freebsd.org/projects/cvsweb.html
Patch0:		%{name}-config.patch
# for %{_libdir}/cgi-bin
Requires:	FHS >= 2.3-8
Requires:	rcs
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
wersji zosta³ uporz±dkowany i oczysczony, usuniêtych zosta³o równie¿
wiele b³êdów. Wprowadzono tak¿e du¿o poprawek bezpieczeñstwa oraz
rozbudowano funkcjonalno¶æ.

%define _cgibindir %{_libdir}/cgi-bin
%define _appdir	 %{_datadir}/%{name}

%prep
%setup -q
%patch0 -p1

# remove backups
find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_appdir}/{css,enscript,icons},%{_cgibindir},%{_sysconfdir}/httpd}

install %{name}.cgi	$RPM_BUILD_ROOT%{_cgibindir}
install %{name}.conf	$RPM_BUILD_ROOT%{_sysconfdir}
install css/*		$RPM_BUILD_ROOT%{_appdir}/css
install enscript/*	$RPM_BUILD_ROOT%{_appdir}/enscript
install icons/*		$RPM_BUILD_ROOT%{_appdir}/icons
install cvsweb.conf*	$RPM_BUILD_DIR/%{name}-%{version}/samples

# "a configuration snippet" suitable for apache{1,2}, boa(?).
# /etc/httpd directory should be common for all webservers (for such "snippets") and their own
# configuration files should be moved to /etc/{apache{1,2},boa} directories.
# "here ducuments" are prefered for small configuration files:
cat <<EOF > $RPM_BUILD_ROOT/etc/httpd/%{name}.conf
Alias /%{name}  %{_appdir}
ScriptAlias /cgi-bin/%{name}.cgi %{_cgibindir}/%{name}.cgi
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
#<deprecated>
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
	# 09_ instead of 99_ is for ScriptAlias /cgi-bin/cvsweb.cgi ...
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/09_%{name}.conf
fi
#</deprecated>

# support for reloading configuration of various installed webservers.
# Use `service' instead running initscript or (worse) apachectl directly (think about boa f.e.).
# `service' is a "next abstraction layer"
WEBSRV=$(for a in $(rpm -q --whatprovides webserver)
do rpm -ql $a | awk 'BEGIN { FS = "/" } /init\.d/ { print $5 }' ; done)
# impossibly - fallback: apache
[ -z "$WEBSRV" ] && WEBSRV=httpd

for SRV in $WEBSRV
do
	[ -f /var/lock/subsys/$SRV ] && /sbin/service $SRV reload 1>&2 || :
done

%preun
if [ "$1" = "0" ]; then
	#<deprecated>	
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/09_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp || :
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	#/<deprecated>
	
	WEBSRV=$(for a in $(rpm -q --whatprovides webserver)
	do rpm -ql $a | awk 'BEGIN { FS = "/" } /init\.d/ { print $5 }' ; done)

	[ -z "$WEBSRV" ] && WEBSRV=httpd

	for SRV in $WEBSRV
	do [ -f /var/lock/subsys/$SRV ] && /sbin/service $SRV reload 1>&2 || :
	done
fi

# not tested:
%triggerun -- apache <= 1.9.99, apache1 <= 1.9.99, boa
echo 'ERROR: cvsweb upgrade failed intentionally.'
echo 'After upgrade, cvsweb will not operate with apache 1.3.x default configuration.'
echo 'Probably directive "ScriptAlias /cgi-bin/cvsweb.cgi /usr/lib/cgi-bin/cvsweb.cgi"'
echo 'must be placed before "ScriptAlias /cgi-bin/ /home/services/httpd/cgi-bin/" .'
exit 1

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL NEWS README TODO samples
%attr(755,root,root) %{_cgibindir}/cvsweb.cgi
%{_datadir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
