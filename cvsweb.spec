Summary:	Visual (www) interface to explore a cvs repository
Summary(pl):	Wizualny (WWW) interfejs do przegl±dania repozytorium cvs
Name:		cvsweb
Version:	3.0.4
Release:	0.1
Epoch:		1
License:	BSD
Group:		Development/Tools
Source0:	http://people.FreeBSD.org/~scop/cvsweb/%{name}-%{version}.tar.gz
# Source0-md5:	c77280df12609b9270ec13172ef49a8c
URL:		http://www.freebsd.org/projects/cvsweb.html
Patch0:		%{name}-config.patch
# for %{_libdir}/cgi-bin
Requires:	FHS >= 2.3-8
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
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%define _cgibindir %{_libdir}/cgi-bin
%define _appdir	 %{_datadir}/%{name}

%prep
%setup -q
%patch0 -p1

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
# Use `service' instead running initscript or (worse) apachectrl directly (think about boa f.e.).
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
