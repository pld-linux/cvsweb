Summary:	visual (www) interface to explore a cvs repository
Name:		cvsweb
Version:	1.93
Release:	1
Epoch:		1
License:	BSD type
Group:		Development/Tools
Group(fr):	Development/Outils
Group(pl):	Programowanie/Narzêdzia
URL:		http://stud.fh-heilbronn.de/~zeller/cgi/cvsweb.cgi/
Source0:	http://stud.fh-heilbronn.de/~zeller/download/%{name}-%{version}.tar.gz
Patch0:		%{name}-config.patch
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

cvsweb wymaga, by na serwerze by³ zainstalowany CVS oraz repzytorium
CVS warte eksploracji.

%prep
%setup -q -n cvsweb
%patch0 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{home/httpd/cgi-bin,%{_sysconfdir}/httpd}

install cvsweb.cgi $RPM_BUILD_ROOT/home/httpd/cgi-bin
install cvsweb.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd

gzip -9nf INSTALL README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%doc icons
%attr(755,root,root) /home/httpd/cgi-bin/cvsweb.cgi
%config(noreplace) %{_sysconfdir}/httpd/cvsweb.conf
