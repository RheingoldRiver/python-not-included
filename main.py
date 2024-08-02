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
            self.update_materials(template)
        if template.has('amount1'):
            self.update_amounts(template)

    def update_materials(self, template: Template):
        materials = []
        i = 1
        # make sure that `materials` is ordered correctly
        # because we will delete all of the previous params as we go
        template.add('materials', '', before='material1')
        while template.has('material' + str(i)):
            material = template.get('material' + str(i)).value.strip()
            materials.append(material)
            template.remove('material' + str(i))
            i += 1
        materials = ', '.join(materials)
        template.add('materials', materials)

    def update_amounts(self, template: Template):
        amounts = []
        i = 1
        # make sure that `amounts` is ordered correctly
        # because we will delete all of the previous params as we go
        template.add('amounts', '', before='amount1')
        while template.has('amount' + str(i)):
            amount = template.get('amount' + str(i)).value.strip()
            amounts.append(amount)
            template.remove('amount' + str(i))
            i += 1
        amounts = ', '.join(amounts)
        template.add('amounts', amounts)


TemplateModifier(site, 'Infobox Building',
                 summary=summary).run()
