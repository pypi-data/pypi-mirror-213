from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component

from ..pydantic_models.info import PersonType, Country, State, Interest


class InfoService(Component):
    _inherit = 'base.rest.service'
    _name = 'info.service'
    _usage = 'info'
    _collection = 'photovoltaic_api.services'


    @restapi.method(
        [(['/person_types'], 'GET')],
        output_param=restapi.PydanticModelList(PersonType)
    )
    def person_types(self):
        '''
        Gets the list of person type ID and name
        '''
        types = self.env['res.partner.type'].search([])
        return [Country.from_orm(t) for t in types]

    @restapi.method(
        [(['/countries'], 'GET')],
        output_param=restapi.PydanticModelList(Country)
    )
    def countries(self):
        '''
        Gets the list of countries ID and name
        '''
        countries = self.env['res.country'].with_context(lang="es_ES").search([])
        return [Country.from_orm(c) for c in countries]

    @restapi.method(
        [(['/states'], 'GET')],
        output_param=restapi.PydanticModelList(State)
    )
    def states(self):
        '''
        Gets the list of all states ID and name
        '''
        states = self.env['res.country.state'].search([])
        return [State.from_orm(s) for s in states]

    @restapi.method(
        [(['/states_by_country/<int:_id>'], 'GET')],
        output_param=restapi.PydanticModelList(State)
    )
    def states_by_country(self, _id):
        '''
        Gets the list of states ID and name for that country_id
        '''
        states = self.env['res.country.state'].search([('country_id', '=', _id)])
        return [State.from_orm(s) for s in states]

    @restapi.method(
        [(['/interests'], 'GET')],
        output_param=restapi.PydanticModelList(Interest)
    )
    def interests(self):
        '''
        Gets the list of existing interests
        '''
        interests = self.env['res.partner.interest'].search([])
        return [Interest.from_orm(s) for s in interests]
