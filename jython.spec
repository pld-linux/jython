Summary:	Python implementation in Java
Summary(pl):	Implementacja jêzyka Python w Javie
Name:		jython
Version:	2.1
Release:	5
License:	BSD
Group:		Development/Languages/Java
Source0:	http://dl.sourceforge.net/jython/%{name}-21.class
# Source0-md5:	e3e6be56646fb7cd6d19a6a69bd76e2f
URL:		http://www.jython.org/
BuildRequires:	jdk
Requires:	jre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javalibdir	%{_datadir}/java
%define		jredir		%{_libdir}/java/jre/lib

%description
Python implementation in Java.

%description -l pl
Implementacja jêzyka Python w Javie.

%prep
%setup -q -c -T
install %{SOURCE0} .
java -classpath . jython-21 -o . demo lib source

%build
JAVA_HOME=%{_libdir}/java
export JAVA_HOME

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javalibdir}

install %{name}.jar $RPM_BUILD_ROOT%{_javalibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt NEWS LICENSE.txt
%{_javalibdir}/*.jar
