
Summary:	Python implementation in Java
Summary(pl):	Implementacja jêzyka Python w Javie
Name:		jython
Version:	2.1
Release:	2
License:	distributable
Group:		Development/Languages/Java
URL:		http://www.jython.org
Source0:	http://prdownloads.sourceforge.net/jython/%{name}-21.class
BuildRequires:	jdk
Requires:	jre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javaclassdir	%{_libdir}/java/
%define		jredir			%{_libdir}/java-sdk/jre/lib

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
install -d $RPM_BUILD_ROOT%{_javaclassdir}

install %{name}.jar $RPM_BUILD_ROOT%{_javaclassdir}

gzip -9nf README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%{_javaclassdir}/*.jar
