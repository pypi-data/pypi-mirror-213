from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
from odoo.exceptions import AccessError, MissingError
from pydantic import parse_obj_as

from ..pydantic_models.contract import Contract
from ..pydantic_models.list_response import ListResponse
from ..pydantic_models import false_to_none


class ContractService(Component):
    _inherit = 'base.rest.service'
    _name = 'contracts.service'
    _usage = 'contracts'
    _collection = 'photovoltaic_api.services'


    @restapi.method(
        [(['/<int:_id>'], 'GET')],
        output_param=restapi.PydanticModel(Contract)
    )
    def get(self, _id):
        try:
            contract = self.env['contract.participation'].browse(_id)
            return self._to_pydantic(contract)

        except AccessError:
            # Return 404 even if it is from a different user
            # to not leak information
            raise MissingError('Access error')

    @restapi.method(
        [(['/'], 'GET')],
        input_param=restapi.CerberusValidator('_validator_search'),
        output_param=restapi.PydanticModel(ListResponse[Contract])
    )
    def search(self, offset=0, limit=None):
        try:
            contracts = self.env['contract.participation'].search(
                [('partner_id', '=', self.env.user.partner_id.id), ('photovoltaic_power_station_id.name', '!=', 'LAS NAVES BRILLEN'), ('product_mode_id.name', '!=', 'Comunero')], limit, offset)
            return self._list_to_pydantic(contracts)

        except AccessError:
            # Return 404 even if it is from a different user
            # to not leak information
            raise MissingError('Access error')

    @restapi.method(
        [(['/<int:_id>'], 'PUT')],
        input_param=restapi.CerberusValidator('_validator_update'),
        output_param=restapi.PydanticModel(Contract)
    )
    def update(self, _id, **params):
        contract = self.env['contract.participation'].search([('id', '=', _id), ('partner_id', '=', self.env.user.partner_id.id)])
        bank_acc = self.env['res.partner.bank'].browse(params['bank_account_id'])

        try:
            bank_acc.read(['id']) # Check access permission
            contract.sudo().write({'bank_account_id': bank_acc.id})
            return self._to_pydantic(contract)
        except AccessError:
            # Return 404 even if it is from a different user
            # to not leak information
            raise MissingError('Access error')

    @restapi.method(
        [(['/'], 'PUT')],
        input_param=restapi.CerberusValidator('_validator_update_some'),
        output_param=restapi.PydanticModel(ListResponse[Contract])
    )
    def update_some(self, **params):
        '''
        Modify bank_account_id for some contracts
        '''
        contracts = self.env['contract.participation'].search([('id', 'in', params['ids']), ('partner_id', '=', self.env.user.partner_id.id)])
        bank_acc = self.env['res.partner.bank'].browse(params['bank_account_id'])

        try:
            bank_acc.read(['id']) # Check access permission
            contracts.sudo().write({'bank_account_id': bank_acc.id})
            return self._list_to_pydantic(contracts)
        except AccessError:
            # Return 404 even if it is from a different user
            # to not leak information
            raise MissingError('Access error')


    # Private methods
    def _calculate_production_data(self, contract):
        generated_power = 0
        tn_co2_avoided = 0
        eq_family_consumption = 0
        for contract_production in contract.contract_production_ids:
            generated_power += contract_production.energy_generated_contract
            tn_co2_avoided += contract_production.tn_co2_avoided_contract
            eq_family_consumption += contract_production.eq_family_consum_contract
        return generated_power, tn_co2_avoided, eq_family_consumption

    def _to_pydantic(self, contract):
        generated_power, tn_co2_avoided, eq_family_consumption = self._calculate_production_data(contract)
        return Contract.parse_obj({
            'id': contract.id,
            'name': contract.name,
            'date': contract.contract_date,
            'investment': contract.inversion,
            'power_plant': {
                'id': contract.photovoltaic_power_station_id.id,
                'name': contract.photovoltaic_power_station_id.name,
                'display_name': false_to_none(contract.photovoltaic_power_station_id, 'name_display'),
                'province': contract.photovoltaic_power_station_id.province,
                'city': contract.photovoltaic_power_station_id.city
            },
            'bank_account': contract.bank_account_id.acc_number,
            'peak_power': contract.peak_power,
            'stage': contract.stage_id.name,
            'generated_power': generated_power,
            'tn_co2_avoided': tn_co2_avoided,
            'eq_family_consumption': eq_family_consumption,
            'sent_state': false_to_none(contract, 'sent_state'),
            'product_mode': contract.product_mode_id.name,
            'payment_period': false_to_none(contract.payment_period_id, 'name'),
            'percentage_invested': contract.percentage,
            'crece_solar_activated': contract.crece_active
        })

    def _list_to_pydantic(self, contracts):
        return parse_obj_as(ListResponse[Contract], {
            'total': len(contracts),
            'rows': [self._to_pydantic(c) for c in contracts]
        })

    def _validator_search(self):
        return {
            'offset': {'type': 'integer'},
            'limit':  {'type': 'integer'}
        }

    def _validator_update(self):
        return {
            'bank_account_id': {'type': 'integer'}
        }

    def _validator_update_some(self):
        return {
            'bank_account_id': {'type': 'integer'},
            'ids':             {'type': 'list', 'schema': {'type': 'integer'}}
        }
