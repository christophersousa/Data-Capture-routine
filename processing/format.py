from processing.data_transform import create_dataframe, transform_uuid
from utils.list_state import list_state_code
from utils.stages import getPipeline

# List state code
list_state_code_uppercase = {state.upper(): details for state, details in list_state_code.items()}

def format_deals(response) -> list:
    stage = response['deal_stage']['id'] or None
    pipeline = getPipeline(stage)
    organization =  None
    if response.get('organization'):
        organization = response['organization']
    obj = {
            'deal_rd_id': response['id'],
            'name': response['name'],
            'pipeline': pipeline,
            'stage': stage,
            'closed_at': response['closed_at'] or None,
            'organization': organization,
            'date_create': response['created_at'],
            'date_update': response['updated_at'],
            'rating_id': None,
        }
    data = create_dataframe([obj])
    first_row = data.iloc[0].to_dict()
    return first_row

def format_organization(response) -> list:
    obj=[{
        'organization_rd_id': response['id'],
        'name': response['name'] or " ",
        'date_create': response['created_at'],
        'date_update': response['updated_at'],
        'document': " ",
        'contacts': response['contacts'],
        'custom_fields': response['custom_fields'],
    }]
    data = create_dataframe(obj)
    first_row = data.iloc[0].to_dict()
    return first_row

# def format_rating(responses) -> list:
#     result_list = []
#     if len(responses) > 0:
#         for response in responses:
#             obj={
#                 'id': response['id'],
#                 'rank': response[''],
#                 'name': response['state'],
#                 'date_create': response['created_at'],
#                 'date_update': response['updated_at'],
#             }
#             result_list.append(obj)
#     return result_list

def format_contact(response) -> list:
    # Handle edge cases where phones or emails might be empty
    phones = response.get('phones', [])
    emails = response.get('emails', [])

    # Get the first phone and email (if available)
    phone = phones[0]['phone'] if phones else '-'
    email = emails[0]['email'] if emails else '-'
    obj={
        'contact_rd_id': response['id'],
        'name': response['name'] or "-",
        'phone': phone,
        'email': email,
        'date_create': response['created_at'],
        'date_update': response['updated_at']
    }
    data = create_dataframe([obj])
    first_row = data.iloc[0].to_dict()
    return first_row

def format_address(responses, date_created, date_updated) -> list:
    obj={
        'cep': None,
        'state': None,
        'state_code': None,
        'lat': None,
        'lon': None,
        'date_create': date_created,
        'date_update': date_updated
    }
    if len(responses) > 0:
        for response in responses:
            if(response['custom_field']['label'] == 'Estado'):
                obj['state'] = response['value']
                state_code = list_state_code_uppercase.get(str(response['value']).upper())
                code =  state_code['sigla'] if state_code else None
                obj['state_code'] = code
            elif(response['custom_field']['label'] == 'CEP'):
                obj['cep'] = response['value']
    data = create_dataframe([obj])
    first_row = data.iloc[0].to_dict()
    return first_row

def format_resume(response) -> list:
    obj={
        'text': response['text'],
        'report': response['user_id'] or None,
        'date_create': response['date'],
        'date_update': response['date'],
        'deal_id': response['deal_id'],
    }
    data = create_dataframe([obj])
    first_row = data.iloc[0].to_dict()
    return first_row

def format_organization_contact_rl(organization, contact):
    obj_organization_contact_rl = {
      "contact_id": contact['id'],
      "organization_id": organization['id'],
      "is_active": True,
      "date_create": organization['date_create'],
      "date_update": organization['date_update']
    }
    return format_object_dataframe(obj_organization_contact_rl)

def format_organization_address_rl(organization, address):
    obj_organization_address_rl = {
      "address_id": address['id'],
      "organization_id": organization['id'],
      "is_active": True,
      "date_create": organization['date_create'],
      "date_update": organization['date_update']
    }
    return format_object_dataframe(obj_organization_address_rl)

def format_organization_deals_rl(organization_id, deals):
    obj_organization_address_rl = {
      "address_id": deals['id'],
      "organization_id": organization_id,
      "is_active": True,
      "date_create": deals['date_create'],
      "date_update": deals['date_update']
    }
    return format_object_dataframe(obj_organization_address_rl)

def format_object_dataframe(obj):
    data = create_dataframe([obj])
    first_row = data.iloc[0].to_dict()
    return first_row