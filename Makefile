#
# Makefile - build wrapper for awscli on CentPOS 7
#
#	git clone RHEL 7 SRPM building tools from
#	https://github.com/nkadel/[package] into designated
#	AWSCLIPKGS below
#
#	Set up local 

# Rely on local nginx service poingint to file://$(PWD)/awsclirepo
#REPOBASE = file://$(PWD)
REPOBASE = http://localhost

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
EPELPKGS+=python-botocore-srpm
EPELPKGS+=python-colorama-srpm
EPELPKGS+=python-d2to1-srpm
EPELPKGS+=python-extras-srpm
EPELPKGS+=python-jmespath-srpm
EPELPKGS+=python-mimeparse-srpm
EPELPKGS+=python-unittest2-srpm
EPELPKGS+=python-PyYAML-srpm
EPELPKGS+=python3-dateutil-srpm
EPELPKGS+=python3-fixtures-srpm

# Actually compilable with epel-6-x86_64
EPELPKGS+=python-awscli-srpm

AWSCLIPKGS+=python3-rsa-srpm

AWSCLIPKGS+=python3-testtools-srpm
AWSCLIPKGS+=python3-pbr-srpm

AWSCLIPKGS+=python3-s3transfer-srpm

# dependencies
AWSCLIPKGS+=python-linecache2-srpm

REPOS+=awsclirepo/el/6

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

# No local dependencies at build time
CFGS+=awsclirepo-6-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=epel-6-x86_64.cfg

all:: $(CFGS) $(MOCKCFGS)
all:: $(REPODIRS)
all:: $(EPELPKGS)
all:: $(AWSCLIPKGS)

all install clean:: FORCE
	@for name in $(EPELPKGS) $(AWSCLIPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done  

epel:: $(EPELPKGS)

# Build for locacl OS
build:: FORCE
	@for name in $(AWSCLIPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done

# Dependencies
python-awscli-srpm::

python-linecacwe-srpm:: python-fixtures-srpm
python-linecacwe-srpm:: python-unittest2-srpm

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
	@echo '"""' >> $@
	@echo >> $@
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
	@uniq -u $@ > $@~
	@mv $@~ $@

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
