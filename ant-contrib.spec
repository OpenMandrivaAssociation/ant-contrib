%global beta_number b2

Summary:        Collection of tasks for Ant
Name:           ant-contrib
Version:        1.0
Release:        0.12.%{beta_number}
License:        ASL 2.0
URL:            http://ant-contrib.sourceforge.net/
Group:          Development/Java
Source0:        http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}%{beta_number}-src.tar.gz
Source1:        http://mirrors.ibiblio.org/pub/mirrors/maven2/%{name}/%{name}/1.0b2/%{name}-1.0b2.pom
Patch0:         ant-contrib-build_xml.patch
Patch2:         ant-contrib-antservertest.patch
BuildRequires:  jpackage-utils >= 1.5
BuildRequires:  junit >= 3.8.0
BuildRequires:  ant-junit >= 1.6.2
BuildRequires:  xerces-j2
BuildRequires:  bcel >= 5.0
BuildRequires:  java-devel >= 1.4.2
Requires:       java >= 1.4.2
Requires:       junit >= 3.8.0
Requires:       ant >= 1.6.2
Requires:       xerces-j2
BuildArch:      noarch

%description
The Ant-Contrib project is a collection of tasks
(and at one point maybe types and other tools)
for Apache Ant.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Api documentation for %{name}.

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
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
CLASSPATH=build/lib/ant-contrib-%{version}.jar:$CLASSPATH
echo $ANT_HOME
ant -Dsource=1.4 -Dversion=%{version} -Dbcel.jar=file://%{_javadir}/bcel.jar all

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -Dpm 644 build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/ant/%{name}.jar

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 
rm -rf build/docs/api

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "ant/ant-contrib" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/ant-contrib

%add_to_maven_depmap %{name} %{name} %{version} JPP/ant %{name}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}.pom

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_sysconfdir}/ant.d/ant-contrib
%{_javadir}/ant/*.jar
%{_mavenpomdir}/*
%{_mavendepmapdir}
%doc build/docs/LICENSE.txt
%doc build/docs/tasks/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

# -----------------------------------------------------------------------------

