import warnings

from django.core.urlresolvers import reverse
from django.test import TestCase

from federated_login.admin import patch_admin, unpatch_admin


class RedirectTest(TestCase):
    def test(self):
        response = self.client.get(reverse('fl_login'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('Location', response)
        self.assertTrue(response['Location'].startswith('https://www.google.com/a/webatoom.nl/'
                                                        'o8/ud?be=o8&openid.assoc_handle='))


class AdminTest(TestCase):
    def test_nopatch(self):
        self.assertContains(self.client.get('/admin/'), 'username')

    def test_warning(self):
        warnings.simplefilter("always")
        with warnings.catch_warnings(record=True) as w:
            from federated_login import patch_admin  # noqa
            self.assertEqual([str(m.message) for m in w],
                             ['federeated_login.patch_admin has been '
                              'deprecated in favor of a setting called '
                              'FL_PATCH_ADMIN, which is set to auto-patch. '
                              'Please update your settings accordingly.'])

    def test_patch(self):
        try:
            patch_admin()
        except RuntimeError:
            raise
        else:
            response = self.client.get('/admin/')
            self.assertEqual(response.status_code, 302)
            self.assertIn('Location', response)
            self.assertEqual(response['Location'],
                             '%s%s' % ('http://testserver', reverse('fl_login')))
        finally:
            unpatch_admin()
