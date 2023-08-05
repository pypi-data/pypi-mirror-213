#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from typing import Any, Mapping, TypeVar, Collection
from enum import Enum


Config = Mapping[str, Any]
OID = TypeVar('OID', str, bytes)
OIDS = Collection[OID]
