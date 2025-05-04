# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = ./_build
<<<<<<< HEAD
APP = /app
=======
APP = ../synch_backend

>>>>>>> df22a06b37407ac0c1e9773f7ff916f345cfe58f

.PHONY: html livehtml apidocs Makefile

# Put it first so that "make" without argument is like "make html".
html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -c .

# Build, watch and serve docs with live reload
livehtml:
<<<<<<< HEAD
	sphinx-autobuild -b html --host 0.0.0.0 --port 9000 --watch $(APP) -c . $(SOURCEDIR) $(BUILDDIR)/html
=======
	sphinx-autobuild -b html --open-browser --port 9000 --watch $(APP) -c . $(SOURCEDIR) $(BUILDDIR)/html
>>>>>>> df22a06b37407ac0c1e9773f7ff916f345cfe58f

# Outputs rst files from django application code
apidocs:
	sphinx-apidoc -o $(SOURCEDIR)/api $(APP)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -c .
