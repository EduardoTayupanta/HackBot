import json

country_num = {
    "1": "co",
    "2": "mx",
    "3": "pe",
    "4": "ec",
    "5": "ch"
}

country_name = {
    'Colombia': '1',
    'Mexico': '2',
    'México': '2',
    'Peru': '3',
    'Ecuador': '4',
    'Chile': '5'
}

supported_card = {
    "1": {
        "debit": "Visa y Mastercard",
        "credit": "Visa, Mastercard, American Express y Dinners Club",
    },
    "2": {
        "debit": "Visa y Mastercard",
        "credit": "Visa, Mastercard y American Express",
    },
    "3": {
        "debit": "Visa y Mastercard",
        "credit": "Visa, Mastercard, American Express, Discover y Dinners Club",
    },
    "4": {
        "debit": "Visa, Alia y Mastercard",
        "credit": "Visa, Mastercard, American Express y Alia",
    },
    "5": {
        "debit": "Visa, Alia y Mastercard",
        "credit": "Visa, Mastercard, American Express, Dinners Club y",
    },
}

intents_url = {
    "Tarjetas_soportadas": "https://docs.kushki.com/co/one-time-payments/card/supported-card-brands"
}

def close_response(intent, slots, message):
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                'name': intent,
                'slots': slots,
                'state':'Fulfilled'
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }

def lambda_handler(event, context):
    print(event)
    print(context)
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    print(intent)
    print(slots)
    
    response = {}
    return_slot = ''
    dialog_type = 'Delegate'
    message = ''
    
    try:
        if intent == 'Tarjetas_soportadas':
            if not slots['key_search']: 
                dialog_type = 'ElicitSlot'
                return_slot = 'key_search'
            if not slots['user_country']: 
                dialog_type = 'ElicitSlot'
                return_slot = 'user_country'
                
        if intent == "Cash_out":
            if not slots['key_cashout']: 
                dialog_type = 'ElicitSlot'
                return_slot = 'key_cashout'
            if not slots['user_country_cashout']: 
                dialog_type = 'ElicitSlot'
                return_slot = 'user_country_cashout'
        
        if intent == "Pagos_qr":
            if not slots['key_pagosqr']: 
                dialog_type = 'ElicitSlot'
                return_slot = 'key_pagosqr'
                
        if intent == "Pagos":
            if not slots['key_pagos']: 
                dialog_type = 'ElicitSlot'
                return_slot = 'key_pagos'
        
        if intent == "Bancos_transferout":
            if not slots['key_bancos_transferout']: 
                dialog_type = 'ElicitSlot'
                return_slot = 'key_bancos_transferout'
            if not slots['key_country_cashout_1']: 
                dialog_type = 'ElicitSlot'
                return_slot = 'key_country_cashout_1'
            if not slots['key_country_cashout_2']: 
                dialog_type = 'ElicitSlot'
                return_slot = 'key_country_cashout_2'
        
        response["sessionState"] = { 
            "dialogAction": {
                'slotToElicit': return_slot,
                'type': dialog_type
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        }
        
        if intent == 'Calificacion' and slots['ranking']:
            calificacion = slots['ranking']['value']['interpretedValue']
            if int(calificacion) > 3:
                message = "Gracias por tu calificacion."
            else:
                message = "Continuaremos mejorando tu experencia."
                
            message = message + " " + "Hasta la proxima."
            response = close_response(intent, slots, message)
        
        if intent == 'Cierre' and slots['confirmacion_cierre']:
            confirmacion_cierre = slots['confirmacion_cierre']['value']['interpretedValue']
            if confirmacion_cierre == "Si":
                message = "Genial, encantado de ayudarte. Podrias calificar mi atencion siendo 1 insatisfecho y 5 muy satisfecho."
            else:
                message = "Lamento no poder ayudarte, tienes otra pregunta?"
            response = close_response(intent, slots, message)
        
        if intent == 'Tarjetas_soportadas' and slots['key_search'] and slots['user_country']:
            user_country = slots['user_country']['value']['interpretedValue']
            country_code = country_name[user_country]
            message = f"En {user_country} las tarjetas soportadas son las siguientes: para débito se soporta {supported_card[country_code]['debit']} y para crédito se soportan las tarjetas {supported_card[country_code]['credit']}.\n Si deseas conocer mas detalle consulta en {intents_url[intent]}"
            message = message + '\n' + "¿Te sirvió la información?"
            response = close_response(intent, slots, message)
            
        if intent == 'Cash_out' and slots['key_cashout'] and slots['user_country_cashout']:
            user_country = slots['user_country_cashout']['value']['interpretedValue']
            country_code = country_name[user_country]
            if country_code != '1':
                message = f"El servicio de Cash Out no se encuentra disponible en {user_country}, solo está disponible para Colombia."
            else:
                message = f"El servicio de Cash Out solo está disponible para este país."
            message = message + '\n' + "¿Te sirvió la información?"
            response = close_response(intent, slots, message)
            
        if intent == 'Pagos_qr' and slots['key_pagosqr']:
            message = f"Actualmente Kushki no tiene la funcionalidad de pagos con QR."
            message = message + '\n' + "¿Te sirvió la información?"
            response = close_response(intent, slots, message)
        
        if intent == 'Pagos' and slots['key_pagos']:
            message = f"Kushki acepta como medios de pagos; tarjetas, tranferencias y efectivo."
            message = message + '\n' + "¿Te sirvió la información?"
            response = close_response(intent, slots, message)
            
        if intent == 'Bancos_transferout' and slots['key_bancos_transferout'] and slots['key_country_cashout_1'] and slots['key_country_cashout_2']:
            option_mx = "- Transfer Out en México funciona con todos los bancos mediante STP. Si deseas conocer mas detalle consulta en: \n https://docs.kushki.com/mx/payouts/transfer/overview"
            option_co = "- Transfer Out en Colombia funciona con todos los bancos que soporte ACH. Si deseas conocer mas detalle consulta en: \n https://docs.kushki.com/co/payouts/transfer/overview"
            
            op_country_1 = slots['key_country_cashout_1']['value']['interpretedValue']
            op_country_2 = slots['key_country_cashout_2']['value']['interpretedValue']
            if op_country_1 == 'Mexico' and op_country_2 == 'Colombia':
                message = option_mx + '\n' + option_co
            if op_country_2 == 'Mexico' and op_country_1 == 'Colombia':
                message = option_co + '\n' + option_mx
            message = message + '\n' + "¿Te sirvió la información?"
            response = close_response(intent, slots, message)
    except:
        message = 'Al momento me encuntro aprendiendo. Ingresa de nuevo tu pregunta.'
        response = close_response(intent, slots, message)

    return response
