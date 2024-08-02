from mwcleric import WikiggClient
from mwcleric.auth_credentials import AuthCredentials
from mwcleric.template_modifier import TemplateModifierBase
from mwparserfromhell.nodes import Template

credentials = AuthCredentials(user_file="me")
site = WikiggClient('gg', credentials=credentials)
summary = 'Bot edit'


class TemplateModifier(TemplateModifierBase):
    def update_template(self, template: Template):
        template.add('other new param', 'goodbye world', before='decor')


TemplateModifier(site, 'Infobox Building',
                 summary=summary).run()
