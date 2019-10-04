from Products.LDAPMultiPlugins.interfaces import ILDAPMultiPlugin
from plone import api
from plone.api.exc import UserNotFoundError
from zope.publisher.browser import BrowserView


class WhoCanDoView(BrowserView):
    def __init__(self, *args, **kwargs):
        super(WhoCanDoView, self).__init__(*args, **kwargs)
        self.user_ids = self.get_user_ids()

    def _get_ldap_plugin_id(self):
        try:
            return [plug.getId() for plug in self.context.acl_users.objectValues()
                    if ILDAPMultiPlugin.providedBy(plug)][0]
        except IndexError:
            return 'NoPluginInstalled'

    def get_user_ids(self):
        return {item[0] for item in self.context.acl_users.portal_role_manager._principal_roles.items()}

    def get_user_ids_with_changed_roles(self):
        portal_membership = api.portal.get_tool('portal_membership')
        roles = portal_membership.getPortalRoles()
        user_ids = []
        for role in roles:
            user_ids.append(self.context.acl_users.portal_role_manager.listAssignedPrincipals(role))

    def get_user_permission_data(self):
        user_data = []
        for user_id in self.user_ids:
            memberdata = api.user.get(user_id)

            if memberdata:
                user = memberdata.getUser()
                is_ldap_user = False

                if self._get_ldap_plugin_id() in user.listPropertysheets():
                    is_ldap_user = True

                try:
                    user_permissions = api.user.get_permissions(user_id)
                    user_data.append({'user_id': user_id,
                                      'is_ldap_user': is_ldap_user,
                                      'view_permission': user_permissions['View'],
                                      'edit_permission': user_permissions['Modify portal content'],
                                      'admin_permission': user_permissions['Plone Site Setup: Overview']})
                except UserNotFoundError:
                    continue

        return sorted(user_data, key=lambda x: x['user_id'])
