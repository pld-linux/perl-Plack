#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Plack
%include	/usr/lib/rpm/macros.perl
Summary:	Plack - Perl Superglue for Web frameworks and Web Servers (PSGI toolkit)
#Summary(pl.UTF-8):
Name:		perl-Plack
Version:	0.9985
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Plack/%{pdir}-%{version}.tar.gz
# Source0-md5:	3d340079cdec9435991fdd0e0953c99e
Patch0:		%{name}-tests.patch
URL:		http://search.cpan.org/dist/Plack/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl(Devel::StackTrace::AsHTML) >= 0.11
BuildRequires:	perl(Filesys::Notify::Simple)
BuildRequires:	perl(HTTP::Body) >= 1.06
BuildRequires:	perl(Hash::MultiValue) >= 0.05
BuildRequires:	perl(Test::Requires)
BuildRequires:	perl(Test::TCP) >= 0.11
BuildRequires:	perl-Devel-StackTrace >= 1.23
BuildRequires:	perl-File-ShareDir >= 1.00
BuildRequires:	perl-HTTP-Request-AsCGI
BuildRequires:	perl-Try-Tiny
BuildRequires:	perl-URI >= 1.36
BuildRequires:	perl-libwww >= 5.814
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(Apache::Constants)' 'perl(Apache::Request)'

%description
Plack is a set of tools for using the PSGI stack. It contains
middleware components, a reference server and utilities for Web
application frameworks. Plack is like Ruby's Rack or Python's Paste
for WSGI.

See PSGI for the PSGI specification and PSGI::FAQ to know what PSGI
and Plack are and why we need them.



# %description -l pl.UTF-8 # TODO

%prep
%setup -q -n %{pdir}-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a eg $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}/*.pm
%{perl_vendorlib}/Plack/
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
%attr(755,root,root) %{_bindir}/plackup
%{perl_vendorlib}/HTTP/Message/PSGI.pm
%{perl_vendorlib}/HTTP/Server/PSGI.pm
%{perl_vendorlib}/auto/share/dist/Plack