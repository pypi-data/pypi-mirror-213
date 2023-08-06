from .quickbase import QuickbaseClient
from .qb_errors import *
import requests
import json
import xml.etree.ElementTree as ET

class JsonQuickbaseClient(QuickbaseClient):
    def __init__(self, credentials=None, timeout=None, default=None, **kwargs):
        if not credentials:
            credentials = kwargs
        super().__init__(credentials, timeout)
        self.headers = {
            'QB-Realm-Hostname': self.realmhost,
            'Content-Type': 'application/json',
        }
        if self.user_token is not None:
            self.headers.update(
                {'Authorization': f'QB-USER-TOKEN {self.user_token}'})
        else:
            raise QBAuthError("In order to use this SDK, you must provide a Quickbase user token.")
        
        self.default = default

    # ---------------------------------------- formatting functions ----------------------------------------
    def nest(self, data_list):
        for index, data in enumerate(data_list):
            data_list[index] = self.nest_record(data)

        return data_list

    def denest(self, data_list):
        for index, data in enumerate(data_list):
            data_list[index] = self.denest_record(data)

        return data_list
    
    def replace_empty_values(self, data_list, default_value):
        for index, data in enumerate(data_list):
            data_list[index] = self.replace_empty_values_record(data, default_value)

        return data_list

    def none_to_0(self, data_list):
        return self.replace_empty_values(data_list, 0)

    def round_ints(self, data_list):
        for index, data in enumerate(data_list):
            data_list[index] = self.round_ints_record(data)

        return data_list
    
    def nest_record(self, data):
        return {key: {'value': value} for key, value in data.items()}
    
    def denest_record(self, data):
        return {key: value['value'] for key, value in data.items()}
    
    def replace_empty_values_record(self, data, default_value):
        return {key: default_value if value is None else value for key, value in data.items()}
    
    def none_to_0_record(self, data):
        return self.replace_empty_values_record(data, 0)
    
    def round_ints_record(self, data):
        for key, value in data.items():
            if isinstance(value, float) and value.is_integer():
                data[key] = int(value)
        return data
    # ---------------------------------------- info gathering functions ----------------------------------------
    def _get_sort_list(self, fids, ascending):
        if ascending:
            order = 'ASC'
        else:
            order = 'DESC'

        if fids:
            return [{'fieldId': fid, 'order': order} for fid in fids]
        else:
            return []

    def get_schema(self, database=None, include_permissions=False):
        params = {
            'tableId': database or self.database,
            'includeFieldPerms': 'true' if include_permissions else 'false'
        }

        response = self._request(
            'https://api.quickbase.com/v1/fields',
            'get',
            self.headers,
            params=params,
            json=True
        )
        return response

    def get_primary_key(self, database=None):
        schema = self.get_schema(database)
        for record in schema:
            if record['properties']['primaryKey']:
                return str(record['id'])

    def _get_report_query(self, qid, database=None):
        params = {
            'tableId': database or self.database,
        }
        url = f"https://api.quickbase.com/v1/reports/{qid}"
        response = self._request(url, 'get', self.headers, params=params, json=True)

        return {
            'where': response['query']['filter'],
            'sortBy': response['query']['sortBy'],
            'groupBy': response['query']['groupBy'],
        }
    # ---------------------------------------- query functions ----------------------------------------
    def do_query(self, query=None, qid=None, columns=None, sort=None,
                 num=None, skip=None, ascending=True,
                 database=None, round_ints=True, require_all=False, default=None):
        
        
        if sort == None:
            sort = [3]
        
        if query:

            body = {
                "from": database,
                "select": [
                    column for column in (columns or [])
                ],
                "where": query,
                "sortBy": self._get_sort_list(sort, ascending)
            }

            response = self._get_data(body, skip, num, require_all)

        elif qid and not columns:
            body = {
                'database': database,
                'qid': qid,
            }

            response = self._get_data(body, skip, num, require_all, report=True)

        elif qid and columns:
            query_info = self._get_report_query(qid, database)
            body = {
                "from": database,
                "select": [
                    column for column in (columns or [])
                ],
                "where": query_info['where'],
                "sortBy": query_info['sortBy'],
            }
            if query_info.get('groupBy'):
                body['groupBy'] = query_info['groupBy']

            response = self._get_data(body, skip, num, require_all)
        else:
            raise ValueError('Must provide either a query or a qid')

        if default == None:
            default = self.default
        
        for index, data in enumerate(response):
            data = self.denest_record(data)
            data = self.replace_empty_values_record(data, default)
            if round_ints:
                data = self.round_ints_record(data)
            response[index] = data

        return response

    def _run_report(self, qid, database=None, skip=None, top=None):
        params = {
            'tableId': database or self.database,
            'skip': skip,
            'top': top,
        }
        url = f"https://api.quickbase.com/v1/reports/{qid}/run"
        response = self._request(url, 'post', self.headers, params=params, json=True)

        return response

    def _run_query(self, body, skip=None, top=None):
        url = 'https://api.quickbase.com/v1/records/query'
        body.update({'options': {
            'skip': int(skip or 0),
            'top': int(top or 0)
        }})
        response = self._request(url, 'post', self.headers, data=body, json=True)

        return response

    def _get_data(self, body, skip=None, top=None, require_all=False, report=False):
        if require_all:
            return self._get_all_data(body, skip, top, report)
        else:
            return self._get_returned_data(body, skip, top, report)

    def _get_all_data(self, body, skip=None, top=None, report=False):
        offset = skip or 0
        goal = top or 0
        database = body.get('from')
        pk = self.get_primary_key(database)
        body.get('select', []).append(pk)

        response = self._get_returned_data(body, offset, goal, report, return_meta=True)

        metadata = response.get('metadata', {})
        num_records = metadata.get('numRecords', 0)
        total_records = metadata.get('totalRecords', 0)

        if goal and goal <= total_records - offset:
            goal -= num_records
        else:
            goal = total_records - num_records - offset
        
        offset += num_records

        data = response.get('data', [])
        if not data:
            return data
        while goal > 0:
            response = self._get_returned_data(body, offset, goal, report, return_meta=True)
            data.extend(response.get('data', []))
            num_records = response.get('metadata', {}).get('numRecords', 0)

            offset += num_records
            goal -= num_records

        for index, record in enumerate(data):
            data[index] = json.dumps(record)

        data = list(set(data))

        for index, record in enumerate(data):
            data[index] = json.loads(record)
            
        return data

    def _get_returned_data(self, body, skip=None, top=None, report=False, return_meta=False):
        if report:
            response = self._run_report(body.pop('qid'), body.pop('database'), skip, top)
        else:
            response = self._run_query(body, skip, top)
        if return_meta:
            return response
        else:
            return response.get('data', [])
    # ---------------------------------------- single record functions ----------------------------------------
    def add_record(self, fields, database=None, uploads=None, safemode=False, return_fields=None):

        if safemode:
            pk = self.get_primary_key(database)
            if pk in fields.keys():
                raise ValueError(f'Primary key fid: {pk} cannot be set in safemode')

        response = self._insert_update_record(fields, uploads, return_fields, database=database)
        response_metadata = response.get('metadata', {})

        if len(response_metadata.get('createdRecordIds')) > 1:
            rids = response_metadata.get('createdRecordIds')
            raise QuickbaseError(f"More than one record created, record ids: {rids}")

        if len(response_metadata.get('updatedRecordIds')) > 0:
            rids = response_metadata.get('updatedRecordIds')
            raise QuickbaseError(f'Record updated instead of created, record ids: {rids}')
        
        if return_fields:
            return self.denest(response['data'])[0]
        else:
            return response_metadata.get('createdRecordIds')[0]

    def edit_record(self, rid=None, key=None, fields=None, database=None, uploads=None, return_fields=None):
        if not fields:
            fields = {}

        if not rid and not key:
            raise ValueError('Must provide either a rid or a key')
        if rid:
            fields.update({'3': rid})
        elif key:
            fields.update({self.get_primary_key(database): key or rid})
        

        response = self._insert_update_record(fields, uploads, return_fields, database=database)
        response_metadata = response.get('metadata', {})

        try:
            if len(response_metadata.get('createdRecordIds')) > 0:
                rids = response_metadata.get('createdRecordIds')
                raise QuickbaseError(f"Created instead of updated a record, record ids: {rids}", response)
            
            if len(response_metadata.get('updatedRecordIds')) > 1:
                rids = response_metadata.get('updatedRecordIds')
                raise QuickbaseError(f'More than one record updated, record ids: {rids}', response)
        except Exception as e:
            raise QuickbaseError('Error Attempting to update records', response) from e
        
        if return_fields:
            return self.denest(response['data'])[0]
        else:
            try:
                return response_metadata.get('updatedRecordIds')[0]
            except IndexError:
                return response_metadata.get('unchangedRecordIds')[0]

    def _insert_update_record(self, body, uploads, return_fields, database=None):
 
        if uploads:
            for upload in uploads:
                body.update({upload['field']: {
                    'fileName': upload['filename'],
                    'data': upload['value'] if not isinstance(upload['value'], bytes) else upload['value'].decode('utf-8'),
                }})

        return self._insert_update_records([body], return_fields, database=database)

    def delete_record(self, rid, database=None):
        body = {
            'from': database or self.database,
            'where': "{3.EX.'%s'}" % rid
        }
        url = 'https://api.quickbase.com/v1/records'
        response = self._request(url, 'delete', self.headers, data=body, json=True)

        return response
    # ---------------------------------------- multiple record functions ----------------------------------------
    def add_multiple_records(self, data, database=None, return_fields=None, round_ints=False, safemode=False):

        if safemode:
            pk = self.get_primary_key(database)
            for index, record in enumerate(data):
                if pk in record.keys():
                    raise ValueError(f'Primary key fid: {pk} cannot be set in safemode (record {index})')

        response = self._insert_update_records(data, return_fields, database)

        response['data'] = self.denest(response['data'])
        if round_ints:
            response['data'] = self.round_ints(response['data'])
        return response 

    def edit_multiple_records(self, data, database=None, return_fields=None, round_ints=False):
        pk = self.get_primary_key(database)
        for record in data:
            if pk not in record.keys():
                raise ValueError(f'Primary key fid: {pk} must be set in edit_multiple_records')
            
        response = self._insert_update_records(data, return_fields, database)
        
        response['data'] = self.denest(response['data'])
        if round_ints:
            response['data'] = self.round_ints(response['data'])
        return response

    def _insert_update_records(self, records, return_fields, database=None):
        if return_fields is None:
            return_fields = [3]

        for value in records[0].values():
            if not isinstance(value, dict) or value.get('value') is None:
                records = self.nest(records)
                break

        url = 'https://api.quickbase.com/v1/records'
        body = {
            'to': database or self.database,
            'data': records,
            'fieldsToReturn': return_fields
        }
        response = self._request(url, 'post', self.headers, data=body, json=True)
        response_metadata = response.get('metadata', {})
        if response_metadata.get('lineErrors'):
            key = list(response_metadata['lineErrors'].keys())[0]
            raise QuickbaseError(f'Your record has invalid data: {response_metadata["lineErrors"][key]}')

        return response

    def purge_records(self, database=None, rids=None, query=None):
        if not rids and not query:
            raise ValueError('Must provide either a list of rids or a query')
        
        if rids:
            rids = [str(rid) for rid in rids]
            query = 'OR'.join(["{3.EX.'%s'}" % rid for rid in rids])
        
        body = {
            'from': database or self.database,
            'where': query
        }
        url = 'https://api.quickbase.com/v1/records'
        response = self._request(url, 'delete', self.headers, data=body, json=True)

        return response
    # ---------------------------------------- file functions ----------------------------------------
    def upload_file(self, rid, upload, database=None):
        record = {
            '3': rid,
            upload['field']: {
                'fileName': upload['filename'],
                'data': upload['value']
            }
        }
        response = self._insert_update_records([record], None, database=database)

        return response

    def get_file(self, url=None, database=None, record=None, field=None, version=0):
        if record and field:
            url = f"https://api.quickbase.com/v1/files/{database or self.database}/{record}/{field}/{version}"
        else:
            url = f"https://api.quickbase.com/v1{url}"

        response = self._request(url, 'get', self.headers, json=False)

        return response, response.content
    # ---------------------------------------- misc functions ----------------------------------------
    def import_from_csv(self, records_csv, clist, database=None):
        csv = records_csv.splitlines()
        data = []

        try:
            for recordData in csv:
                record = {}
                for fieldkey, field in enumerate(recordData.split(',')):
                    record[f'{clist[fieldkey]}'] = field

                if len(record) != len(clist):
                    raise IndexError

                data.append(record)
                record = {}
        except IndexError:
            print("csv string or clist is invalid")

        try:
            response = self.add_multiple_records(database=database, data=data)
        except IndexError:
            response = False
        return response

    def change_record_owner(self, rid, database, new_owner):
        if not rid:
            raise ValueError(
                message="A record id is needed to modify a record!")

        url = f"https://{self.realmhost}/db/{database}?a=API_ChangeRecordOwner&rid={rid}&newowner={new_owner}&usertoken={self.user_token}"

        response = requests.get(url)
        # read xml response
        root = ET.fromstring(response.text)

        error_code = root.find('errcode')

        if error_code.text != "0":
            error_text = root.find('errtext')
            error_text = error_text.text if error_text is not None else '[no error text]'
            return f"Quickbase error: {error_text}"

        return "Successfully changed record owner."