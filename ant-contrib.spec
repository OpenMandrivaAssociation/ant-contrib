%global beta_number b2

Summary:	Collection of tasks for Ant
Name:		ant-contrib
Version:	1.0
Release:	0.12.%{beta_number}
License:	ASL 2.0
Group:		Development/Java
Url:		http://ant-contrib.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}%{beta_number}-src.tar.gz
Source1:	http://mirrors.ibiblio.org/pub/mirrors/maven2/%{name}/%{name}/1.0b2/%{name}-1.0b2.pom
Patch0:		ant-contrib-build_xml.patch
Patch2:		ant-contrib-antservertest.patch
BuildArch:	noarch
BuildRequires:	ant-junit >= 1.6.2
BuildRequires:	bcel >= 5.0
BuildRequires:	jpackage-utils >= 1.5
BuildRequires:	junit >= 3.8.0
BuildRequires:	xerces-j2
BuildRequires:	java-devel >= 1.4.2
Requires:	java >= 1.4.2
Requires:	junit >= 3.8.0
Requires:	ant >= 1.6.2
Requires:	xerces-j2

%description
The Ant-Contrib project is a collection of tasks
(and at one point maybe types and other tools)
for Apache Ant.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description    javadoc
Api documentation for %{name}.

%prep
%setup -qn %{name}
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
# jars
install -Dpm 644 build/lib/%{name}.jar %{buildroot}%{_javadir}/ant/%{name}.jar

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} 
rm -rf build/docs/api

mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo "ant/ant-contrib" > %{buildroot}%{_sysconfdir}/ant.d/ant-contrib

%add_to_maven_depmap %{name} %{name} %{version} JPP/ant %{name}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%doc build/docs/LICENSE.txt
%doc build/docs/tasks/*
%{_sysconfdir}/ant.d/ant-contrib
%{_javadir}/ant/*.jar
%{_mavenpomdir}/*
%{_mavendepmapdir}

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


