%{?scl:%scl_package jackson-datatype-guava}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

Name:          %{?scl_prefix}jackson-datatype-guava
Version:       2.6.3
Release:       2.%{baserelease}%{?dist}
Summary:       Add-on module for Jackson JSON processor which handles Guava data-types
License:       ASL 2.0
URL:           http://wiki.fasterxml.com/JacksonModuleGuava
Source0:       https://github.com/FasterXML/jackson-datatype-guava/archive/%{pkg_name}-%{version}.tar.gz

BuildRequires: %{?scl_prefix_maven}maven-local
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson:jackson-parent:pom:)
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson.core:jackson-core)
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires: %{?scl_prefix}mvn(com.google.guava:guava) >= 15.0
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires: %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-site-plugin)
BuildRequires: %{?scl_prefix_maven}mvn(org.codehaus.mojo:build-helper-maven-plugin)

BuildArch:     noarch

%description
Add-on datatype-support module for Jackson that handles
Guava types (currently mostly just collection ones).

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n %{pkg_name}-%{pkg_name}-%{version}

sed -i 's/\r//' src/main/resources/META-INF/LICENSE
cp -p src/main/resources/META-INF/LICENSE .

%pom_xpath_remove "pom:properties/pom:osgi.import"
%pom_xpath_inject "pom:properties" "
    <osgi.import>
com.google.common.collect,
com.google.common.base,
com.google.common.cache,
com.google.common.hash,
com.google.common.net,
com.fasterxml.jackson.core,
com.fasterxml.jackson.core.io,
com.fasterxml.jackson.core.util,
com.fasterxml.jackson.databind,
com.fasterxml.jackson.databind.deser,
com.fasterxml.jackson.databind.deser.std,
com.fasterxml.jackson.databind.introspect,
com.fasterxml.jackson.databind.jsonFormatVisitors,
com.fasterxml.jackson.databind.jsontype,
com.fasterxml.jackson.databind.ser,
com.fasterxml.jackson.databind.ser.std,
com.fasterxml.jackson.databind.ser.impl,
com.fasterxml.jackson.databind.type,
com.fasterxml.jackson.databind.util
</osgi.import>"


%mvn_file : %{pkg_name}
%pom_remove_plugin com.google.code.maven-replacer-plugin:replacer
%pom_add_plugin org.apache.maven.plugins:maven-antrun-plugin \
  "<executions><execution><id>process-packageVersion</id><phase>generate-sources</phase></execution></executions>"
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x

%mvn_build
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc README.md release-notes/*
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Tue Jul 26 2016 Mat Booth <mat.booth@redhat.com> - 2.6.3-2.2
- Add missing package import

* Tue Jul 26 2016 Mat Booth <mat.booth@redhat.com> - 2.6.3-2.1
- Auto SCL-ise package for rh-eclipse46 collection

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct 25 2015 gil cattaneo <puntogil@libero.it> 2.6.3-1
- update to 2.6.3

* Mon Sep 28 2015 gil cattaneo <puntogil@libero.it> 2.6.2-1
- update to 2.6.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 31 2015 gil cattaneo <puntogil@libero.it> 2.5.0-1
- update to 2.5.0

* Wed Dec 17 2014 gil cattaneo <puntogil@libero.it> 2.4.2-1
- update to 2.4.2

* Fri Jul 04 2014 gil cattaneo <puntogil@libero.it> 2.4.1-1
- update to 2.4.1

* Sat Dec 07 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- initial rpm
