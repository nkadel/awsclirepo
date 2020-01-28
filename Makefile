#
# Makefile - build wrapper for awscli on CentPOS 7
#
#	git clone RHEL 7 SRPM building tools from
#	https://github.com/nkadel/[package] into designated
#	AWSCLIPKGS below
#
#	Set up local 

# Rely on local nginx service poingint to file://$(PWD)/awsclirepo
#REPOBASE = http://localhost
REPOBASE = file://$(PWD)

# Placeholder RPMs for python2-foo packages to include python-foo
EPELPKGS+=python2-contextlib2-srpm
EPELPKGS+=python2-d2to1-srpm
EPELPKGS+=python2-dateutil-srpm
EPELPKGS+=python2-extras-srpm
EPELPKGS+=python2-fixtures-srpm
EPELPKGS+=python2-linecache2-srpm
EPELPKGS+=python2-mimeparse-srpm
EPELPKGS+=python2-pbr-srpm
EPELPKGS+=python2-pyasn1-srpm
EPELPKGS+=python2-testtools-srpm
EPELPKGS+=python2-unittest2-srpm

# Build python3 versions of packages
EPELPKGS+=python-colorama-srpm
EPELPKGS+=python-d2to1-srpm
EPELPKGS+=python-extras-srpm
EPELPKGS+=python-jmespath-srpm
EPELPKGS+=python-mimeparse-srpm
EPELPKGS+=python-unittest2-srpm
EPELPKGS+=python-PyYAML-srpm
EPELPKGS+=python3-dateutil-srpm

# Actually compilable with epel-6-x86_64
EPELPKGS+=python-awscli-srpm

# dependencies

AWSCLIPKGS+=python3-fixtures-srpm


AWSCLIPKGS+=python-linecache2-srpm

AWSCLIPKGS+=python-botocore-srpm
AWSCLIPKGS+=python-boto3-srpm

AWSCLIPKGS+=python3-rsa-srpm

AWSCLIPKGS+=python3-testtools-srpm
AWSCLIPKGS+=python3-pbr-srpm

AWSCLIPKGS+=python3-s3transfer-srpm

AWSCLIPKGS+=python-fedcred-srpm

REPOS+=awsclirepo/el/6
REPOS+=awsclirepo/el/7
REPOS+=awsclirepo/el/8

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

# No local dependencies at build time
CFGS+=awsclirepo-6-x86_64.cfg
CFGS+=awsclirepo-7-x86_64.cfg
CFGS+=awsclirepo-8-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=epel-6-x86_64.cfg
MOCKCFGS+=epel-7-x86_64.cfg
MOCKCFGS+=epel-8-x86_64.cfg

all:: install
install:: $(CFGS) $(MOCKCFGS)
install:: $(REPODIRS)
install:: $(EPELPKGS)
install:: $(AWSCLIPKGS)

build install clean getsrc build:: FORCE
	@for name in $(EPELPKGS) $(AWSCLIPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done  

# It is sometimes useful to build up all the more independent EPEL packages first
epel:: $(EPELPKGS)

# Dependencies for order sensitivity
python-awscli-srpm::

python3-fixtures-srpm:: python3-testtools-srpm

python-botocore-srpm:: python-jmespath-srpm
python-botocore-srpm:: python3-dateutil-srpm

python-boto3-srpm:: python-botocore-srpm

python-linecache2-srpm:: python3-fixtures-srpm
python-linecache2-srpm:: python-unittest2-srpm

python3-pbr-srpm:: python-d2to1-srpm

python-fedcred-srpm:: python-boto3-srpm

# Actually build in directories
$(EPELPKGS):: FORCE
	(cd $@; $(MAKE) $(MLAGS) install)

$(AWSCLIPKGS):: FORCE
	(cd $@; $(MAKE) $(MLAGS) install)

repos: $(REPOS) $(REPODIRS)
$(REPOS):
	install -d -m 755 $@

.PHONY: $(REPODIRS)
$(REPODIRS): $(REPOS)
	@install -d -m 755 `dirname $@`
	/usr/bin/createrepo `dirname $@`


.PHONY: cfg cfgs
cfg cfgs:: $(CFGS) $(MOCKCFGS)

awsclirepo-6-x86_64.cfg: epel-6-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-6-x86_64/awsclirepo-6-x86_64/g' $@
	@echo >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[awsclirepo]' >> $@
	@echo 'name=awsclirepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/awsclirepo/el/6/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

awsclirepo-7-x86_64.cfg: epel-7-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-7-x86_64/awsclirepo-7-x86_64/g' $@
	@echo >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[awsclirepo]' >> $@
	@echo 'name=awsclirepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/awsclirepo/el/7/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

awsclirepo-8-x86_64.cfg: epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-8-x86_64/awsclirepo-8-x86_64/g' $@
	@echo "    Disabling 'best=' for $@"
	@sed -i '/^best=/d' $@
	@echo "best=0" >> $@
	@echo >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[awsclirepo]' >> $@
	@echo 'name=awsclirepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/awsclirepo/el/8/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

$(MOCKCFGS)::
	ln -sf --no-dereference /etc/mock/$@ $@

repo: awsclirepo.repo
awsclirepo.repo:: Makefile awsclirepo.repo.in
	if [ -s /etc/fedora-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/fedora/|g" > $@; \
	elif [ -s /etc/redhat-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/el/|g" > $@; \
	else \
		echo Error: unknown release, check /etc/*-release; \
		exit 1; \
	fi

awsclirepo.repo:: FORCE
	cmp -s /etc/yum.repos.d/$@ $@       


nginx:: nginx/default.d/awsclirepo.conf

nginx/default.d/awsclirepo.conf:: FORCE nginx/default.d/awsclirepo.conf.in
	cat $@.in | \
		sed "s|@REPOBASEDIR@;|$(PWD)/;|g" | tee $@;

nginx/default.d/awsclirepo.conf:: FORCE
	cmp -s $@ /etc/$@ || \
	    diff -u $@ /etc/$@

clean::
	find . -name \*~ -exec rm -f {} \;
	rm -f *.cfg
	rm -f *.out
	rm -f nginx/default.d/*.conf
	@for name in $(AWSCLIPKGS); do \
	    $(MAKE) -C $$name clean; \
	done

distclean:
	rm -rf $(REPOS)

maintainer-clean:
	rm -rf $(AWSCLIPKGS)

FORCE::
