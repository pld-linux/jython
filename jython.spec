%include /usr/lib/rpm/macros.java
Summary:	Python implementation in Java
Summary(pl):	Implementacja jêzyka Python w Javie
Name:		jython
Version:	2.1
Release:	6
License:	BSD
Group:		Development/Languages/Java
Source0:	http://dl.sourceforge.net/jython/%{name}-21.class
# Source0-md5:	e3e6be56646fb7cd6d19a6a69bd76e2f
URL:		http://www.jython.org/
BuildRequires:	jdk
BuildRequires:	jpackage-utils
Requires:	jre
Requires:	jpackage-utils
BuildArch:	noarch
ExclusiveArch:	i586 i686 pentium3 pentium4 athlon %{x8664} noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python implementation in Java.

%description -l pl
Implementacja jêzyka Python w Javie.

%package doc
Summary:	Manual for %{name}
Group:		Development/Languages/Java

%description doc
Documentation for %{name}.

%description doc -l it
Documentazione di %{name}.

%description doc -l fr
Documentation pour %{name}.

%package javadoc
Summary:	API documentation for Jython
Summary(pl):	Dokumentacja API Jythona
Group:		Development/Languages/Java

%description javadoc
JavaDoc-generated API documentation for Jython.

%description javadoc -l pl
Dokumentacja API Jythona, wygenerowana przez JavaDoc.

%package modules
Summary:	Python modules for Jython
Summary(pl):	Modu³y pythona dla Jythona
Group:		Development/Languages/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description modules
Python modules for Jython.

%description modules -l pl
Modu³y pythona dla Jythona.

%package tools
Summary:	Jython tools
Summary(pl):	Narzêdzia Jythona
Group:		Development/Languages/Java
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description tools
Jython tools.

%description tools -l pl
Narzêdzia Jythona.

%package examples
Summary:	Jython examples
Summary(pl):	Przyk³ady u¿ycia Jythona
Group:		Development/Languages/Java

%description examples
Jython examples (Demo).

%description examples -l pl
Przyk³ady u¿ycia Jythona.

%prep
%setup -q -c -T
install %{SOURCE0} .

%build
unset CLASSPATH || :
unset JAVA_HOME || :
export JAVA_HOME="%{java_home}" 
java -classpath . jython-21 -o . demo lib source

ln -s %{_javadocdir}/%{name}-%{version} javadoc

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{name}-%{version},/var/cache/%{name}} \
	$RPM_BUILD_ROOT{%{_bindir},%{_examplesdir}/%{name}-%{version},%{_datadir}/%{name}}

install %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

cp -ar Doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -ar Lib Tools $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -ar Demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
ln -sf /var/cache/%{name} $RPM_BUILD_ROOT%{_datadir}/%{name}/cachedir

unset CLASSPATH || :
export JAVA_HOME="%{java_home}" 

cat >$RPM_BUILD_ROOT/%{_bindir}/%{name} <<EOF
#/bin/sh

. %{_javadir}-utils/java-functions
set_javacmd

\$JAVACMD -Dpython.home="%{_datadir}/%{name}" -classpath "%{_javadir}/%{name}-%{version}.jar:\$CLASSPATH" "org.python.util.jython" "\$@"
EOF

cat >$RPM_BUILD_ROOT/%{_bindir}/jythonc <<EOF
#/bin/sh

%{_bindir}/%{name} "%{_datadir}/%{name}/Tools/jythonc/jythonc.py" "\$@"
EOF

%post
# rebuild cache
%{_bindir}/%{name} -c "import site"

%post modules
# rebuild cache
%{_bindir}/%{name} -c "import site"

%preun
if [ "$1" = "0" ]; then
rm -rf /var/cache/%{name}/*
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt NEWS LICENSE.txt
%attr(755,root,root) %{_bindir}/%{name}
%{_javadir}/*.jar
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/cachedir
/var/cache/%{name}
%{_datadir}/%{name}/Lib/site.py

%files modules
%{_datadir}/%{name}/Lib
%exclude %{_datadir}/%{name}/Lib/site.py

%files tools
%attr(755,root,root) %{_bindir}/jythonc
%{_datadir}/%{name}/Tools

%files examples
%{_examplesdir}/%{name}-%{version}

%files doc
%doc Doc/*.html Doc/images javadoc

%files javadoc
%{_javadocdir}/%{name}-%{version}
