#
# Conditional build:
%bcond_without	python2	# Python 2.x version (available as 'py2lint')
%bcond_with	python3	# Python 3.x version (available as 'py3lint')
%bcond_without	doc	# Sphinx documentation

Summary:	Python 2 tool that checks if a module satisfy a coding standard
Summary(pl.UTF-8):	Narzędzie Pythona 2 sprawdzające zgodność modułu ze standardem kodowania
Name:		python-pylint
Version:	1.9.5
Release:	1
License:	GPL v2+
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/pylint
Source0:	https://github.com/PyCQA/pylint/archive/pylint-%{version}.tar.gz
# Source0-md5:	3db0fde1876d50ad313fd707ecd6562b
Patch0:		%{name}-rc.patch
URL:		http://www.pylint.org/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-pytest-runner
BuildRequires:	python-setuptools >= 7.0
%if %{with tests}
BuildRequires:	python-astroid >= 1.6.0
BuildRequires:	python-astroid < 2.0
BuildRequires:	python-backports.functools_lru_cache
BuildRequires:	python-configparser
BuildRequires:	python-isort >= 4.2.5
BuildRequires:	python-mccabe
BuildRequires:	python-pytest
BuildRequires:	python-pytest-xdist
BuildRequires:	python-singledispatch
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-modules < 1:3.7
BuildRequires:	python3-pytest-runner
BuildRequires:	python3-setuptools >= 7.0
%if %{with tests}
BuildRequires:	python3-astroid >= 1.6.0
BuildRequires:	python3-astroid < 2.0
BuildRequires:	python3-isort >= 4.2.5
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-xdist
BuildRequires:	python3-mccabe
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg >= 1
%endif
Suggests:	python-devel-src
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 2 tool that checks if a module satisfy a coding standard.

This package contains only the Python modules used by the tool.

%description -l pl.UTF-8
Narzędzie Pythona 2 sprawdzające zgodność modułów napisanych w języku
Python z regułami tworzenia kodu źródłowego.

Ten pakiet zawiera tylko moduły Pythona używane przez to narzędzie.

%package -n py2lint
Summary:	Python 2 tool that checks if a module satisfy a coding standard (modules)
Summary(pl.UTF-8):	Narzędzie Pythona sprawdzające zgodność modułu ze standardem kodowania (moduły)
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n py2lint
Python 2 tool that checks if a module satisfy a coding standard.

%description -n py2lint -l pl.UTF-8
Narzędzie Pythona 2 sprawdzające zgodność modułów napisanych w języku
Python z regułami tworzenia kodu źródłowego.

%package -n python3-pylint
Summary:	Python 3 tool that checks if a module satisfy a coding standard (moduły)
Summary(pl.UTF-8):	Narzędzie Pythona 3 sprawdzające zgodność modułu ze standardem kodowania (modules)
Group:		Libraries/Python

%description -n python3-pylint
Python 3 tool that checks if a module satisfy a coding standard.

This package contains only the Python modules used by the tool.

%description -n python3-pylint -l pl.UTF-8
Narzędzie Pythona 3 sprawdzające zgodność modułów napisanych w języku
Python z regułami tworzenia kodu źródłowego.

Ten pakiet zawiera tylko moduły Pythona używane przez to narzędzie.

%package -n py3lint
Summary:	Python 3 tool that checks if a module satisfy a coding standard
Summary(pl.UTF-8):	Narzędzie Pythona 3 sprawdzające zgodność modułu ze standardem kodowania
Group:		Development/Languages/Python
Requires:	python3-pylint = %{version}-%{release}
Obsoletes:	pylint-python3 < 1.0.0-2

%description -n py3lint
Python 3 tool that checks if a module satisfy a coding standard.

Python 3.x version, available via the 'py3lint' command.

%description -n py3lint -l pl.UTF-8
Narzędzie Pythona 3 sprawdzające zgodność modułów napisanych w języku
Python z regułami tworzenia kodu źródłowego.

Wersja dla Pythona 3.x, dostępna przez polecenie 'py3lint'.

%package doc
Summary:	Documentation for pylint module and tool
Summary(pl.UTF-8):	Dokumentacja do modułu i narzędzia pylint
Group:		Documentation

%description doc
Documentation for pylint module and tool.

%description doc -l pl.UTF-8
Dokumentacja do modułu i narzędzia pylint.

%prep
%setup -q -n pylint-pylint-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%if %{with doc}
%{__make} -C doc text \
	PYTHONPATH=$PWD
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir}/man1}

%if %{with python2}
%py_install
%py_postclean

for tool in epylint pylint pyreverse symilar ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${tool} $RPM_BUILD_ROOT%{_bindir}/${tool}-2
	cp -p man/${tool}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${tool}-2.1
done

cp -p examples/pylintrc $RPM_BUILD_ROOT%{_sysconfdir}/pylintrc-2
%endif

%if %{with python3}
%py3_install

for tool in epylint pylint pyreverse symilar ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${tool} $RPM_BUILD_ROOT%{_bindir}/${tool}-3
	cp -p man/${tool}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${tool}-3.1
done
# old PLD package compatibility
ln -s epylint-3 $RPM_BUILD_ROOT%{_bindir}/epy3lint
ln -s pylint-3 $RPM_BUILD_ROOT%{_bindir}/py3lint
ln -s pyreverse-3 $RPM_BUILD_ROOT%{_bindir}/py3reverse
echo '.so epylint-3.1' >$RPM_BUILD_ROOT%{_mandir}/man1/epy3lint.1
echo '.so pylint-3.1' >$RPM_BUILD_ROOT%{_mandir}/man1/py3lint.1
echo '.so pyreverse-3.1' >$RPM_BUILD_ROOT%{_mandir}/man1/py3reverse.1

cp -p examples/pylintrc $RPM_BUILD_ROOT%{_sysconfdir}/pylintrc-3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc ChangeLog README.rst examples
%{py_sitescriptdir}/pylint
%{py_sitescriptdir}/pylint-%{version}-py*.egg-info

%files -n py2lint
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/epylint-2
%attr(755,root,root) %{_bindir}/pylint-2
%attr(755,root,root) %{_bindir}/pyreverse-2
%attr(755,root,root) %{_bindir}/symilar-2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pylintrc-2
%{_mandir}/man1/epylint-2.1*
%{_mandir}/man1/pylint-2.1*
%{_mandir}/man1/pyreverse-2.1*
%{_mandir}/man1/symilar-2.1*
%endif

%if %{with python3}
%files -n python3-pylint
%defattr(644,root,root,755)
%doc ChangeLog README.rst examples
%{py3_sitescriptdir}/pylint
%{py3_sitescriptdir}/pylint-%{version}-py*.egg-info

%files -n py3lint
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/epylint-3
%attr(755,root,root) %{_bindir}/pylint-3
%attr(755,root,root) %{_bindir}/pyreverse-3
%attr(755,root,root) %{_bindir}/symilar-3
%attr(755,root,root) %{_bindir}/epy3lint
%attr(755,root,root) %{_bindir}/py3lint
%attr(755,root,root) %{_bindir}/py3reverse
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pylintrc-3
%{_mandir}/man1/epylint-3.1*
%{_mandir}/man1/pylint-3.1*
%{_mandir}/man1/pyreverse-3.1*
%{_mandir}/man1/symilar-3.1*
%{_mandir}/man1/epy3lint.1*
%{_mandir}/man1/py3lint.1*
%{_mandir}/man1/py3reverse.1*
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/_build/text/*
%endif
