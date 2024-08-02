from mwcleric.wikigg_client import WikiggClient
from mwcleric.auth_credentials import AuthCredentials
from mwcleric.page_modifier import PageModifierBase
from mwparserfromhell.nodes import Template

credentials = AuthCredentials(user_file="me")
site = WikiggClient('gg', credentials=credentials)
summary = 'Bot edit'


class PageModifier(PageModifierBase):
    def update_wikitext(self, wikitext):
        for template in wikitext.filter_templates(recursive=True):
            name = template.name
            if name.matches('Infobox Building'):
                self.update_infobox_building(template)
            elif name.matches('Not Infobox Building'):
                self.update_not_infobox_building(template)

    def update_infobox_building(self, template: Template):
        # do stuff here
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
        while template.has(kind + str(i)):
            value = template.get(kind + str(i)).value.strip()
            items.append(value)
            template.remove(kind + str(i))
            i += 1
        text = ', '.join(items)
        template.add(plural, text)

    def update_not_infobox_building(self, template: Template):
        # do stuff here
        if not template.has('param'):
            return
        template.get('param').value = 'you have been changed'


PageModifier(site, site.pages_using('Infobox Building'),
             summary=summary).run()
