from mwcleric import WikiggClient
from mwcleric.auth_credentials import AuthCredentials
from mwcleric.template_modifier import TemplateModifierBase
from mwparserfromhell.nodes import Template

credentials = AuthCredentials(user_file="me")
site = WikiggClient('gg', credentials=credentials)
summary = 'Bot edit'


class TemplateModifier(TemplateModifierBase):
    def update_template(self, template: Template):
        if template.has('material') and template.has('material1'):
            raise ValueError
        if template.has('amount') and template.has('amount1'):
            raise ValueError
        if template.has('material'):
            material = template.get('material').value.strip()
            template.add('material1', material, before='material')
            template.remove('material')
        if template.has('amount'):
            amount = template.get('amount').value.strip()
            template.add('amount1', amount, before='amount')
            template.remove('amount')

        if template.has('material1'):
            self.update_param(template, 'material')
        if template.has('amount1'):
            self.update_param(template, 'amount')

    def update_param(self, template, kind):
        plural = kind + 's'
        items = []
        i = 1
        # make sure that `materials` is ordered correctly
        # because we will delete all of the previous params as we go
        template.add(plural, '', before=kind + '1')
        while template.has(kind+ str(i)):
            value = template.get(kind + str(i)).value.strip()
            items.append(value)
            template.remove(kind + str(i))
            i += 1
        text = ', '.join(items)
        template.add(plural, text)


TemplateModifier(site, 'Infobox Building',
                 summary=summary).run()
