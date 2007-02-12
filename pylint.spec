Summary:	Python tool that checks if a module satisfy a coding standard
Summary(pl.UTF-8):   Pythonowe narzędzie sprawdzające zgodność modułu ze standardem kodowania
Name:		pylint
Version:	0.12.2
Release:	1
License:	GPL
Group:		Development/Languages/Python
Source0:	ftp://ftp.logilab.fr/pub/pylint/%{name}-%{version}.tar.gz
# Source0-md5:	38333614235969f9e715c71666cc596f
URL:		http://www.logilab.org/projects/pylint/view
BuildRequires:	python-devel
BuildRequires:	python-modules >= 2.2.1
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%pyrequires_eq	python-modules
Requires:	python-logilab-astng >= 0.16.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python tool that checks if a module satisfy a coding standard.

%description -l pl.UTF-8
Narzędzie sprawdzające zgodność modułów napisanych w języku Python
z regułami tworzenia kodu źródłowego.

%package gui
Summary:	GUI for pylint
Summary(pl.UTF-8):   Graficzny interfejs użytkownika dla pylinta
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-tkinter

%description gui
Tk based GUI for pylint.

%description gui -l pl.UTF-8
Oparty na bibliotece Tk graficzny interfejs użytkownika dla pylinta.

%prep
%setup -q

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir}/man1}

python setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
install examples/pylintrc $RPM_BUILD_ROOT%{_sysconfdir}/pylintrc

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog TODO README examples/* doc/*.txt
%attr(755,root,root) %{_bindir}/pylint
%attr(755,root,root) %{_bindir}/symilar
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pylintrc
%{py_sitescriptdir}/*
%{_mandir}/man1/*

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pylint-gui
