# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, CloudBlue
# All rights reserved.
#

from connect.client import R

from reports.utils import get_basic_value, get_value


def generate(client, parameters, progress_callback):
    hubs_dict = _get_hubs_dict(client)
    customers = _get_customers(client, parameters)

    progress = 0
    total = customers.count()

    for customer in customers:
        contact = customer['contact_info']

        yield (
            get_basic_value(customer, 'id'),
            get_basic_value(customer, 'external_id'),
            'Yes' if 'customer' in customer['scopes'] else '-',
            'Yes' if 'tier1' in customer['scopes'] else '-',
            'Yes' if 'tier2' in customer['scopes'] else '-',
            _get_provider(hubs_dict, get_value(customer, 'hub', 'id'), 'id'),
            _get_provider(hubs_dict, get_value(customer, 'hub', 'id'), 'name'),
            get_basic_value(customer, 'name'),
            get_basic_value(customer, 'tax_id'),
            get_basic_value(contact, 'address_line1'),
            get_basic_value(contact, 'address_line2'),
            get_basic_value(contact, 'city'),
            get_basic_value(contact, 'state'),
            get_basic_value(contact, 'postal_code'),
            get_basic_value(contact, 'country'),
            get_value(contact, 'contact', 'first_name'),
            get_value(contact, 'contact', 'last_name'),
            get_value(contact, 'contact', 'email'),
            _create_phone(contact['contact']['phone_number']),
            'Available',
        )
        progress += 1
        progress_callback(progress, total)


def _get_customers(client, parameters):
    query = R()

    if parameters.get('date') and parameters['date']['after'] != '':
        query &= R().events.created.at.ge(parameters['date']['after'])
        query &= R().events.created.at.le(parameters['date']['before'])
    if parameters.get('tier_type') and parameters['tier_type']['all'] is False:
        query &= R().scopes.oneof(parameters['tier_type']['choices'])

    return client.ns('tier').accounts.filter(query).order_by('-events.created.at').limit(1000)


def _get_hubs_dict(client):
    hubs = {}
    for marketplace in client.marketplaces.all():
        if 'hubs' in marketplace:
            for hub in marketplace['hubs']:
                if 'hub' in hub and hub['hub']['id'] not in hubs:
                    hubs[hub['hub']['id']] = marketplace['owner']

    return hubs


def _get_provider(hubs_dict, hub, prop):
    if not hub or hub == '-' or hub not in hubs_dict:  # pragma: no branch
        return '-'  # pragma: no cover
    return hubs_dict[hub][prop]


def _create_phone(pn):
    return f'{pn["country_code"]}{pn["area_code"]}{pn["phone_number"]}{pn["extension"]}'
