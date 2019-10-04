from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.whocando.tests import FunctionalTestCase


class TestWhoCanDoView(FunctionalTestCase):

    @browsing
    def test_get_roles_for_users(self, browser):
        self.grant('Manager')
        browser.login()
        self.create_some_users()
        browser.open(self.portal, view='whocando')
        actual = browser.css('.global-roles').first.lists()
        expected = [
                ['', 'Lesen', 'Schreiben', 'Administrator', 'Is from LDAP'],
                ['annemaria.webi', u'\u2713', '', '', ''],
                ['bernd.adlebert', u'\u2713', u'\u2713', u'\u2713', ''],
                ['berta.muller', u'\u2713', u'\u2713', u'\u2713', ''],
                ['hildegard.wessenhachen', u'\u2713', u'\u2713', '', ''],
                ['hugo.boss', u'\u2713', '', '', '']
                ]

        self.assertEqual(expected, actual)

    def create_some_users(self):
        reader = create(Builder('user')
                        .named('Hugo', 'Boss')
                        .with_roles('Reader'))
        admin = create(Builder('user')
                       .named('Berta', u'M\xfcller')
                       .with_roles('Site Administrator'))
        editor = create(Builder('user')
                        .named('Hildegard', 'Wessenhachen')
                        .with_roles('Editor'))
        authenticated = create(Builder('user')
                               .named('Annemaria', 'Webi')
                               .with_roles('Authenticated'))
        manager = create(Builder('user')
                         .named('Bernd', 'Adlebert')
                         .with_roles('Manager'))

        return {'reader': reader, 'admin': admin, 'editor': editor,
                'authenticated': authenticated, 'manager': manager}
