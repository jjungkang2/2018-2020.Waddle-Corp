import json

def lambda_handler(event, context):
    params = event['params']
    qs = params['querystring']
    return_name = ''
    return_erase_list = ''
    return_multi_choice = ''

    filter_json = open("filter.json").read()
    filter_data = json.loads(filter_json)

    for x in filter_data:
        if x['component'] == int(qs['component']+100):
            return_name = x['name']
            return_erase_list = x['erase_list']
            return_multi_choice = x['multi_choice']
            break

    return {"name": return_name,
            "erase_list": return_erase_list,
            "multi_choice": return_multi_choice}

if __name__ == "__main__":
    pass
    # print(lambda_handler({'params':{'querystring':{'component':'397416'}}}, None))