from flask import abort

def validate_post_args(function):
    def wrapper(self, name, price):
        fields = {
            'name': {
                'required': True,
                'expected_type': 'str',
                'value': name
            },
            'price': {
                'required': True,
                'expected_type': 'float',
                'value': price
            }
        }

        for field in fields:
            field_name = field
            field = fields[field]
            field_type = type(field['value']).__name__

            if not field['value']:
                abort(403, 'The "'+field_name+'" field is required.')
            
            if field_type != field['expected_type']:
                abort(403, 'The type of "'+field_name+'" field is invalid. "'+field_type+'" was given but "'+field['expected_type']+'" was expected.')
    
        return function(self, name, price)
    
    return wrapper