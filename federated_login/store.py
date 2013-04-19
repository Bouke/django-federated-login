import base64
import time
from openid.store.interface import OpenIDStore
from openid.store.nonce import SKEW
from openid.association import Association as OpenidAssociation

from .models import Association, Nonce


class DjangoOpenIDStore(OpenIDStore):
    def storeAssociation(self, server_url, association):
        kwargs = {'server_url': server_url, 'handle': association.handle}
        try:
            assoc = Association.objects.get(**kwargs)
        except Association.DoesNotExist:
            assoc = Association(**kwargs)
        print 'secret?', assoc.secret
        assoc.secret = base64.encodestring(association.secret)
        assoc.issued = association.issued
        assoc.lifetime = association.lifetime
        assoc.assoc_type = association.assoc_type
        assoc.save()

    def removeAssociation(self, server_url, handle):
        try:
            assoc = Association.objects.get(server_url=server_url,
                                            handle=handle)
            assoc.delete()
            return True
        except Association.DoesNotExist:
            return False

    def getAssociation(self, server_url, handle=None):
        kwargs = {'server_url': server_url}
        if handle:
            kwargs['handle'] = handle

        openid_assocs = []
        for assoc in Association.objects.filter(**kwargs).order_by('-issued'):
            openid_assoc = OpenidAssociation(assoc.handle,
                                             base64.decodestring(assoc.secret),
                                             assoc.issued,
                                             assoc.lifetime,
                                             assoc.assoc_type)

            if openid_assoc.getExpiresIn() > 0:
                openid_assocs.append(openid_assoc)
            else:
                assoc.delete()

        if openid_assocs:
            return openid_assocs[0]

    def useNonce(self, server_url, timestamp, salt):
        if abs(timestamp - time.time()) > SKEW:
            return False
        return Nonce.objects.get_or_create(server_url=server_url,
                                           timestamp=timestamp,
                                           salt=salt)[1]
