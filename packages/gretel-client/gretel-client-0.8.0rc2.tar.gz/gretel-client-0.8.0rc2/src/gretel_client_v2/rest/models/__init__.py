# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from gretel_client_v2.rest.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from gretel_client_v2.rest.model.artifact import Artifact
from gretel_client_v2.rest.model.project import Project
