Summary:	Python implementation in Java
Summary(pl.UTF-8):	Implementacja języka Python w Javie
Name:		jython
Version:	2.2.1
Release:	2
License:	BSD
Group:		Development/Languages/Java
Source0:	http://dl.sourceforge.net/jython/%{name}_installer-%{version}.jar
# Source0-md5:	774543534bef2d68247953882237d448
URL:		http://www.jython.org/
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Requires:	jre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python implementation in Java.

%description -l pl.UTF-8
Implementacja języka Python w Javie.

%package doc
Summary:	Manual for %{name}
Summary(pl.UTF-8):	Podręcznik dla pakietu %{name}
Group:		Development/Languages/Java

%description doc
Documentation for %{name}.

%description doc -l it.UTF-8
Documentazione di %{name}.

%description doc -l fr.UTF-8
Documentation pour %{name}.

%description doc -l pl.UTF-8
Dokumentacja dla pakietu %{name}.

%package javadoc
Summary:	API documentation for Jython
Summary(pl.UTF-8):	Dokumentacja API Jythona
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
JavaDoc-generated API documentation for Jython.

%description javadoc -l pl.UTF-8
Dokumentacja API Jythona, wygenerowana przez JavaDoc.

%package modules
Summary:	Python modules for Jython
Summary(pl.UTF-8):	Moduły Pythona dla Jythona
Group:		Development/Languages/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description modules
Python modules for Jython.

%description modules -l pl.UTF-8
Moduły Pythona dla Jythona.

%package tools
Summary:	Jython tools
Summary(pl.UTF-8):	Narzędzia Jythona
Group:		Development/Languages/Java
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description tools
Jython tools.

%description tools -l pl.UTF-8
Narzędzia Jythona.

%package examples
Summary:	Jython examples
Summary(pl.UTF-8):	Przykłady użycia Jythona
Group:		Development/Languages/Java

%description examples
Jython examples (Demo).

%description examples -l pl.UTF-8
Przykłady użycia Jythona.

%prep
%setup -q -c -T
install %{SOURCE0} .

%build
unset CLASSPATH || :
unset JAVA_HOME || :
export JAVA_HOME="%{java_home}"

%java -jar jython_installer-%{version}.jar --silent --directory installed/ --type all

ln -s %{_javadocdir}/%{name}-%{version} javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{name}-%{version},/var/cache/%{name}} \
	$RPM_BUILD_ROOT{%{_bindir},%{_examplesdir}/%{name}-%{version},%{_datadir}/%{name}}

cd installed

install %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

cp -a Doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a Lib Tools $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a Demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
ln -sf /var/cache/%{name} $RPM_BUILD_ROOT%{_datadir}/%{name}/cachedir

unset CLASSPATH || :
export JAVA_HOME="%{java_home}"

%java -Dpython.home=. -classpath jython.jar "org.python.util.jython" -c "import compileall; compileall.compile_dir(\"$RPM_BUILD_ROOT%{_datadir}/%{name}/Lib\", ddir=\"$RPM_BUILD_ROOT\")"

cat >$RPM_BUILD_ROOT%{_bindir}/%{name} <<'EOF'
#!/bin/sh

. %{_javadir}-utils/java-functions
set_javacmd

exec $JAVACMD -Dpython.home="%{_datadir}/%{name}" -classpath "%{_javadir}/%{name}-%{version}.jar:$CLASSPATH" "org.python.util.jython" "$@"
EOF

cat >$RPM_BUILD_ROOT%{_bindir}/jythonc <<'EOF'
#/bin/sh

exec %{_bindir}/%{name} "%{_datadir}/%{name}/Tools/jythonc/jythonc.py" "$@"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
# rebuild cache
umask 022
%{_bindir}/%{name} -c "import site"

%post modules
# rebuild cache
umask 022
%{_bindir}/%{name} -c "import site"

%preun
if [ "$1" = "0" ]; then
	rm -rf /var/cache/%{name}/*
fi

%files
%defattr(644,root,root,755)
%doc installed/{ACKNOWLEDGMENTS,README.txt,NEWS,LICENSE.txt}
%attr(755,root,root) %{_bindir}/%{name}
%{_javadir}/*.jar
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/cachedir
/var/cache/%{name}
%dir %{_datadir}/%{name}/Lib
%{_datadir}/%{name}/Lib/UserDict.py
%{_datadir}/%{name}/Lib/UserDict$py.class
%{_datadir}/%{name}/Lib/javaos.py
%{_datadir}/%{name}/Lib/javaos$py.class
%{_datadir}/%{name}/Lib/javapath.py
%{_datadir}/%{name}/Lib/javapath$py.class
%{_datadir}/%{name}/Lib/site.py
%{_datadir}/%{name}/Lib/site$py.class
%{_datadir}/%{name}/Lib/stat.py
%{_datadir}/%{name}/Lib/stat$py.class
%{_datadir}/%{name}/Lib/string.py
%{_datadir}/%{name}/Lib/string$py.class

%files modules
%defattr(644,root,root,755)
%{_datadir}/%{name}/Lib/*
%exclude %{_datadir}/%{name}/Lib/UserDict.py
%exclude %{_datadir}/%{name}/Lib/UserDict$py.class
%exclude %{_datadir}/%{name}/Lib/javaos.py
%exclude %{_datadir}/%{name}/Lib/javaos$py.class
%exclude %{_datadir}/%{name}/Lib/javapath.py
%exclude %{_datadir}/%{name}/Lib/javapath$py.class
%exclude %{_datadir}/%{name}/Lib/site.py
%exclude %{_datadir}/%{name}/Lib/site$py.class
%exclude %{_datadir}/%{name}/Lib/stat.py
%exclude %{_datadir}/%{name}/Lib/stat$py.class
%exclude %{_datadir}/%{name}/Lib/string.py
%exclude %{_datadir}/%{name}/Lib/string$py.class

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jythonc
%{_datadir}/%{name}/Tools

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files doc
%defattr(644,root,root,755)
%doc installed/Doc/*.html installed/Doc/images javadoc

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
