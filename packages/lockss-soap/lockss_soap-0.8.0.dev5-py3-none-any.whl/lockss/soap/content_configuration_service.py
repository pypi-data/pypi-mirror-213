#!/usr/bin/env python3

# Copyright (c) 2000-2023, Board of Trustees of Leland Stanford Jr. University
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

SERVICE = 'ContentConfigurationService'

from lockss.soap.util import _construct_query, _make_client

def add_au_by_id(node_object, auid):
    """
    Adds the given AU to the given host (by AUID), and returns a record with
    these attributes:
    
    *  ``id`` (string): the AUID
    *  ``isSuccess`` (boolean): a success flag
    *  ``message`` (string): an error message
    *  ``name`` (string): the AU name
    
    Performs an ``addAuById`` SOAP operation.
    
    :param node_object: A node object returned by `lockss.soap.node`.
    :param auid: An AUID.
    :return: An object (with attributes described above), or ``None`` if
    """
    client = _make_client(node_object, SERVICE)
    ret = client.service.addAuById(auId = auid)
    return ret


def add_au_by_id_list(node_object, auids):
    """
    Adds the given AUs to the given host (by AUID), and returns a list of
    records with these attributes:

    *  ``id`` (string): the AUID
    *  ``isSuccess`` (boolean): a success flag
    *  ``message`` (string): an error message
    *  ``name`` (string): the AU name

    Performs an ``addAuByIdList`` SOAP operation.

    :param node_object: A node object returned by `lockss.soap.node`.
    :param auid: An AUID.
    :return: An object (with attributes described above), or ``None`` if
    """
    client = _make_client(node_object, SERVICE)
    ret = client.service.addAuByIdList(auIds=auids)
    return ret
