Summary:	a CGI interface to CVS trees
Summary(pl):	interfejs CGI do drzew CVS
Name:		cvsweb
Version:	0.1
Release:	1
Group:		Development/Tools
Group(pl):	Programowanie/Narzêdzia
Copyright:	Distributable
Source: 	http://lemming.stud.fh-heilbronn.de/~zeller/download/%{name}.tar.gz
Patch:		%{name}.patch
URL:		http://lemming.stud.fh-heilbronn.de/~zeller/cvsweb.cgi
Vendor:		Henner Zeller <zeller@think.de>
Requires:	webserver
Requires:	rcs
Requires:	cvs
BuildRoot:	/tmp/%{name}-%{version}-root
BuildArch:	noarch

%description
a CGI interface to CVS trees.
By default it search for CVS repository in "/usr/src/CVSROOT".

%description -l pl
Interfejs CGI do drzew CVS.
Standardowo repozytorium jest poszukiwane w "/usr/src/CVSROOT".

%prep
%setup -q -n %{name}
%patch -p1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/home/httpd/{cgi-bin/,icons/}
install -d $RPM_BUILD_ROOT/etc/httpd/

install	%{name}.cgi				$RPM_BUILD_ROOT/home/httpd/cgi-bin
install icons/{miniback,minidir,minitext}.gif	$RPM_BUILD_ROOT/home/httpd/icons
install %{name}.conf				$RPM_BUILD_ROOT/etc/httpd/

gzip -9nf INSTALL README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {INSTALL,README,TODO}.gz

%attr(755,root,root) /home/httpd/cgi-bin/*
%attr(644,root,root) /home/httpd/icons/*.gif
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
