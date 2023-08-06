import logging
import urllib.parse
import datetime
import json

import requests
import pyjq

import abobjs

class AB_User(abobjs.AB_Base):

    """
    A.K.A. Cycles. Not Sure why the mismatch exists
    """

    _endpoint = "/api/v1/users"
    _single = ".users[0]"
    _name = "user"

    _uid_field = "username"

    _name_field = "email"

    def __init__(self, id=None, api_info=None, **kwargs):

        #self.api_info = api_info
        #self.id = control_id
        #self.datum = kwargs.get("control_datum", dict())

        # Dunder Handling
        endpoint = kwargs.get("endpoint", self._endpoint)
        single = kwargs.get("single", self._single)
        name = kwargs.get("name", self._name)

        #print(self._strips)
        #strips = kwargs.get("strips", self._strips)

        abobjs.AB_Base.__init__(self, id=id, api_info=api_info,
                                endpoint=endpoint, single=single, name=name,
                                **kwargs)