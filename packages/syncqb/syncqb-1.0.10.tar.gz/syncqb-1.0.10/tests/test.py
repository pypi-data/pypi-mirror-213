# from syncqb import qb_client
import qb_client
from memory_profiler import profile
# from pprint import pprint
# from lxml.etree import _Element
@profile
def main():
    # table info:
    # database: bnsucj684
    # values valid for fid 6: 'Misc', '_other'
    # values valid for fid 9: 23
    # fid 3 is the record id, which is auto generated
    # use a value from fid 3 to update or delete a record
    # create a series of tests to test the functionality of each method for both xml and json
    # ONLY MODIFY OR DELETE RECORDS THAT YOU CREATED
    test = 'dGVzdA=='
    record_data = [
        {
            '6': {'value': 'Misc'},
            '9': {'value': 23},
        },
        {
            '19': {
                'fileName': 'test.txt',
                'data': test,
            },
            '6': 'Misc',
            '9': 23,
        },
    ]
    

    # client = qb_client.get_xml_client()
    client2 = qb_client.get_json_client()

    # xml_res = client.do_query(
    #     query='{3.EX.128}',
    #     # qid=10, 
    #     columns=[3, 6, 9], 
    #     database='bnsucj684', 
    #     # structured=True,
    #     # qid_custom_headers=True
    # )
    xml_res = 'N/A'
    # json_res = client2.do_query(
    #     query=main_asset_query,
    #     database=database,
    #     columns=columns,
    #     # high_volume=True,
    #     require_all=True,
    # )
    json_res = client2.add_multiple_records(
        data=record_data,
        database='bnsucj684',
    )
    # json_res = 'N/A'

    # print('xml_res:', xml_res)
    print('json_res:', json_res)
    




if __name__ == '__main__':
    main()