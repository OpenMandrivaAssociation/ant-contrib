%define gcj_support 1
%define beta_number b2

Summary:        Collection of tasks for Ant
Name:           ant-contrib 
Version:        1.0
Release:        %mkrel 0.4.%{beta_number}.1
License:        Apache License
URL:            http://ant-contrib.sourceforge.net/
Group:          Development/Java
Source0:        http://prdownloads.sourceforge.net/ant-contrib/ant-contrib-%{version}%{beta_number}-src.tar.gz
Patch0:         ant-contrib-build_xml.patch
Patch2:         ant-contrib-antservertest.patch
BuildRequires:  jpackage-utils >= 1.5
BuildRequires:  junit >= 3.8.0
BuildRequires:  ant-junit >= 1.6.2
BuildRequires:  ant-nodeps >= 1.6.2
BuildRequires:  xerces-j2
BuildRequires:  bcel >= 5.0
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel >= 1.0.31
Requires(post):   java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
%else
BuildRequires:  java-devel >= 1.4.2
Requires:       java >= 1.4.2
%endif
Requires:       junit >= 3.8.0
Requires:       ant >= 1.6.2
Requires:       xerces-j2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The Ant-Contrib project is a collection of tasks 
(and at one point maybe types and other tools) 
for Apache Ant.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%prep
%setup -q  -n %{name}
rm -rf test/src/net/sf/antcontrib/antclipse

%patch0
%patch2
sed -i "s/\r//" manual/tasks/foreach.html manual/tasks/for.html

%build
export JUNIT_VER=`rpm -q --queryformat='%%{version}' junit`
mkdir -p test/lib
(cd test/lib
ln -s $(find-jar junit-$(JUNIT_VER)) junit-$(JUNIT_VER).jar
)
export OPT_JAR_LIST="ant/ant-junit junit ant/ant-nodeps"
export CLASSPATH=
CLASSPATH=build/lib/ant-contrib-%{version}.jar:$CLASSPATH
echo $ANT_HOME
%{ant} -Dsource=1.4 -Dversion=%{version} -Dbcel.jar=file://%{_javadir}/bcel.jar all


%install
rm -rf $RPM_BUILD_ROOT

# jars
install -Dpm 644 build/lib/%{name}.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
rm -rf build/docs/api


%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
%doc build/docs/LICENSE.txt
%doc build/docs/tasks/*

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%dir %doc %{_javadocdir}/%{name}

# -----------------------------------------------------------------------------
