Summary:	Visual (www) interface to explore a cvs repository
Summary(pl):	Wizualny (WWW) interfejs do przegl±dania repozytorium cvs
Name:		cvsweb
Version:	1.112
Release:	7
Epoch:		1
License:	BSD-like
Group:		Development/Tools
URL:		http://stud.fh-heilbronn.de/~zeller/cgi/cvsweb.cgi/
Source0:	http://stud.fh-heilbronn.de/~zeller/download/%{name}-%{version}.tar.gz
# Source0-md5:	30ff2783ff8e01bf72193902decd0c73
Patch0:		%{name}-config.patch
Patch1:		%{name}-fix_perl_options.patch
Requires:	perl(IPC::Open2)
Requires:	perl(Time::Local)
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

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{/home/services/httpd/cgi-bin,%{_sysconfdir}}

install cvsweb.cgi $RPM_BUILD_ROOT/home/services/httpd/cgi-bin
install cvsweb.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL README TODO
%doc icons
%attr(755,root,root) /home/services/httpd/cgi-bin/cvsweb.cgi
%config(noreplace) %{_sysconfdir}/cvsweb.conf
