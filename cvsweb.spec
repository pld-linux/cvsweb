%define	name	cvsweb
%define	version	1.79
%define	release	1
%define	serial	1

Summary:	visual (www) interface to explore a cvs repository
Name:		%{name}
Version:	%{version}
Release:	%{release}
Serial:		%{serial}
Copyright:	BSD type
Group:		Development/Tools
URL:		http://stud.fh-heilbronn.de/~zeller/cgi/cvsweb.cgi/
Source:		%{name}-%{version}.tar.bz2
Patch:		%{name}-1.73-config.patch
BuildRoot:	/var/tmp/%{name}-%{version}
BuildArchitectures: noarch

%description
cvsweb is a visual (www) interface to explore a cvs repository. This is an
enhanced cvsweb developed by Henner Zeller. Enhancements include recognition
and display of popular mime-types, visual, color-coded, side by side diffs
of changes and the ability sort the file display and to hide old files
from view. One living example of the enhanced cvsweb is the KDE cvsweb

cvsweb requires the server to have cvs and a cvs repository worth exploring.

%description -l pl
cvsweb jest wizualnym interfejsem do eksploracji repozytorium cvs. Jest to
ulepszona wersja programu cvsweb Hennera Zellera. Do ulepszeñ zaliczyæ mo¿na
rozpoznawanie i wy¶wietlanie popularnych typów MIME; wizualnych, kolorowych, 
umieszczonych obok siebie ró¿nic miêdzy plikami oraz zdolno¶æ sortowania 
widoku plików oraz ukrywania starych plików. ¯ywym przyk³adem ulepszonego
cvsweba jest cvsweb projektu KDE.

cvsweb wymaga, by na serwerze by³ zainstalowany CVS oraz repzytorium CVS 
warte eksploracji.

%prep
%setup -q -n cvsweb
%patch -p1

%build

%install
if [ -d $RPM_BUILD_ROOT ]; then rm -r $RPM_BUILD_ROOT ; fi
mkdir -p $RPM_BUILD_ROOT/{home/httpd/cgi-bin,etc/httpd/conf}
install -m 755 cvsweb.cgi $RPM_BUILD_ROOT/home/httpd/cgi-bin
install -m 644 cvsweb.conf $RPM_BUILD_ROOT/etc/httpd/conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc INSTALL README TODO
%doc icons
/home/httpd/cgi-bin/cvsweb.cgi
%config(noreplace) /etc/httpd/conf/cvsweb.conf

%changelog
* Tue Nov  9 1999 Peter Hanecak <hanecak@megaloman.sk>
- updated to 1.79

* Tue Oct 12 1999 Peter Hanecak <hanecak@megaloman.sk>
- initial spec (based on Ryan Weaver's <ryanw@infohwy.com> gtksee spec
  because i like the style of it)
