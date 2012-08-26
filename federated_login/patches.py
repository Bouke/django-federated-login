# Patches openid's Consumer to function with Google Apps.
#
# Google Apps returns claimed_id values according to a working draft, but these
# are not part of the current 2.0 specification.
#
# See also:
# https://github.com/openid/python-openid/pull/39
# https://sites.google.com/site/oauthgoog/fedlogininterp/openiddiscovery

import copy
from urlparse import urldefrag

from openid.consumer import consumer
from openid.consumer.discover import OpenIDServiceEndpoint, OPENID_2_0_TYPE
from openid.message import OPENID2_NS, OPENID1_NS, no_default
from openid import oidutil

# decorator by Guido
# http://mail.python.org/pipermail/python-dev/2008-January/076194.html
def monkeypatch_method(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        print 'override', cls, func.__name__, func
        return func
    return decorator

@monkeypatch_method(consumer.GenericConsumer)
def _verifyDiscoveryResultsOpenID2(self, resp_msg, endpoint):
    print 'inside patched function!'
    to_match = OpenIDServiceEndpoint()
    to_match.type_uris = [OPENID_2_0_TYPE]
    to_match.claimed_id = resp_msg.getArg(OPENID2_NS, 'claimed_id')
    to_match.local_id = resp_msg.getArg(OPENID2_NS, 'identity')

    # Raises a KeyError when the op_endpoint is not present
    to_match.server_url = resp_msg.getArg(
        OPENID2_NS, 'op_endpoint', no_default)

    # claimed_id and identifier must both be present or both
    # be absent
    if (to_match.claimed_id is None and
        to_match.local_id is not None):
        raise consumer.ProtocolError(
            'openid.identity is present without openid.claimed_id')

    elif (to_match.claimed_id is not None and
          to_match.local_id is None):
        raise consumer.ProtocolError(
            'openid.claimed_id is present without openid.identity')

    # This is a response without identifiers, so there's really no
    # checking that we can do, so return an endpoint that's for
    # the specified `openid.op_endpoint'
    elif to_match.claimed_id is None:
        return OpenIDServiceEndpoint.fromOPEndpointURL(to_match.server_url)

    # The claimed ID doesn't match, so we have to do discovery
    # again. This covers not using sessions, OP identifier
    # endpoints and responses that didn't match the original
    # request.
    if to_match.server_url.startswith(u'https://www.google.com/a/'):
        import urllib
        claimed_id = u'https://www.google.com/accounts/o8/user-xrds?uri=%s' % urllib.quote_plus(to_match.claimed_id)
    else:
        claimed_id = to_match.claimed_id

    if not endpoint:
        oidutil.log('No pre-discovered information supplied.')
        endpoint = self._discoverAndVerify(claimed_id, [to_match])
    else:
        # The claimed ID matches, so we use the endpoint that we
        # discovered in initiation. This should be the most common
        # case.
        try:
            self._verifyDiscoverySingle(endpoint, to_match)
        except consumer.ProtocolError, e:
            oidutil.log(
                "Error attempting to use stored discovery information: " +
                str(e))
            oidutil.log("Attempting discovery to verify endpoint")
            endpoint = self._discoverAndVerify(
                claimed_id, [to_match])

    # The endpoint we return should have the claimed ID from the
    # message we just verified, fragment and all.
    if endpoint.claimed_id != to_match.claimed_id:
        endpoint = copy.copy(endpoint)
        endpoint.claimed_id = to_match.claimed_id
    return endpoint

@monkeypatch_method(consumer.GenericConsumer)
def _verifyDiscoverySingle(self, endpoint, to_match):
    """Verify that the given endpoint matches the information
    extracted from the OpenID assertion, and raise an exception if
    there is a mismatch.

    @type endpoint: openid.consumer.discover.OpenIDServiceEndpoint
    @type to_match: openid.consumer.discover.OpenIDServiceEndpoint

    @rtype: NoneType

    @raises consumer.ProtocolError: when the endpoint does not match the
        discovered information.
    """
    print 'inside patched function!'

    # Every type URI that's in the to_match endpoint has to be
    # present in the discovered endpoint.
    for type_uri in to_match.type_uris:
        if not endpoint.usesExtension(type_uri):
            raise consumer.TypeURIMismatch(type_uri, endpoint)

    # Fragments do not influence discovery, so we can't compare a
    # claimed identifier with a fragment to discovered information.
    if to_match.server_url.startswith(u'https://www.google.com/a/'):
        import urllib
        claimed_id = u'https://www.google.com/accounts/o8/user-xrds?uri=%s' % urllib.quote_plus(to_match.claimed_id)
    else:
        claimed_id = to_match.claimed_id

    defragged_claimed_id, _ = urldefrag(claimed_id)
    if defragged_claimed_id != endpoint.claimed_id:
        raise consumer.ProtocolError(
            'Claimed ID does not match (different subjects!), '
            'Expected %s, got %s' %
            (defragged_claimed_id, endpoint.claimed_id))

    if to_match.server_url.startswith(u'https://www.google.com/a/'):
        import urllib
        local_id = u'https://www.google.com/accounts/o8/user-xrds?uri=%s' % urllib.quote_plus(to_match.local_id)
    else:
        local_id =  to_match.getLocalID()

    if local_id != endpoint.getLocalID():
        raise consumer.ProtocolError('local_id mismatch. Expected %s, got %s' %
                            (local_id, endpoint.getLocalID()))

    # If the server URL is None, this must be an OpenID 1
    # response, because op_endpoint is a required parameter in
    # OpenID 2. In that case, we don't actually care what the
    # discovered server_url is, because signature checking or
    # check_auth should take care of that check for us.
    if to_match.server_url is None:
        assert to_match.preferredNamespace() == OPENID1_NS, (
            """The code calling this must ensure that OpenID 2
           responses have a non-none `openid.op_endpoint' and
           that it is set as the `server_url' attribute of the
           `to_match' endpoint.""")

    elif to_match.server_url != endpoint.server_url:
        raise consumer.ProtocolError('OP Endpoint mismatch. Expected %s, got %s' %
                            (to_match.server_url, endpoint.server_url))
