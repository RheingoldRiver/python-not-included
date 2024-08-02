from mwcleric import WikiggClient
from mwcleric.auth_credentials import AuthCredentials
from mwcleric.template_modifier import TemplateModifierBase
from mwparserfromhell.nodes import Template

credentials = AuthCredentials(user_file="me")
site = WikiggClient('gg', credentials=credentials)
summary = 'Bot edit'

site.save_title(site.client.pages['User:RheingoldRiver/test2'], 'hello world')

# class TemplateModifier(TemplateModifierBase):
#     def update_template(self, template: Template):
#         return
#
#
# TemplateModifier(site, 'TEMPLATEYOUCAREABOUT',
#                  summary=summary).run()
