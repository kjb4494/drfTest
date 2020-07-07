from preprocessing import crawling
import json


def get_dump_data(model, fields_list):
    data_list = []
    for fields in fields_list:
        data_list.append({
            'model': model,
            'fields': fields
        })
    return data_list


def generate_json_file(dump_data, output_name='dumpdata.json'):
    with open(output_name, 'w') as fout:
        json.dump(dump_data, fout)


def main_code():
    try:
        modifier_list = crawling.get_modifier_list_from_eu4_wiki(with_default_value=True)
        dump_data = get_dump_data('testapp.modifier', modifier_list)
        output_name = '../modifier_data.json'
        generate_json_file(dump_data=dump_data, output_name=output_name)
        print(output_name, '파일을 생성했습니다.')
    except Exception as err:
        print("데이터 파일 생성에 실패했습니다.", err)

    try:
        country_list = crawling.get_country_list_from_eu4_wiki()
        dump_data = get_dump_data('testapp.country', country_list)
        output_name = '../country_data.json'
        generate_json_file(dump_data=dump_data, output_name=output_name)
        print(output_name, '파일을 생성했습니다.')
    except Exception as err:
        print("데이터 파일 생성에 실패했습니다.", err)


if __name__ == '__main__':
    main_code()
