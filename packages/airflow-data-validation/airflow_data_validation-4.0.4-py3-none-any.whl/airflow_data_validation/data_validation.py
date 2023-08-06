import datetime
import logging
import sys
import requests
import json
# airflow_data_validation

# google
from google.cloud import bigquery

PY3 = sys.version_info[0] == 3


class Data_validation():
    # template_fields = ['run_date','run_id']

    def __init__(
            self,
            slack_token,
            bigquery_conn_id='bigquery_default',
            gcp_project='guesty-data',
            on_call=None,
            *args, **kwargs):
        super(Data_validation, self).__init__(*args, **kwargs)
        self.bigquery_conn_id = bigquery_conn_id
        self.gcp_project = gcp_project
        self.slack_token = slack_token
        self.on_call = on_call

    ui_color = '#A6E6A6'

    def send_slack_alert(self, test_name, table_name, slack_token, on_call):
        today = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        text = f'FYI: <!channel>\n' \
               'BI On Call: <{0}>\n' \
               '*Test Name*: {1}\n' \
               '-----------------------------\n' \
               ':large_blue_circle: *DQA Notification*\n' \
               '-----------------------------\n' \
               '*Table*:               {2}\n' \
               '*Execution Time*:    {3}'.format(on_call, test_name, table_name, today)

        alert = {
            "text": text
        }

        requests.post(slack_token, json.dumps(alert))

    def get_dup_query(self, destination_table, column_ids_list, is_partitioned, partition_field):
        column_id = ','.join(column_ids_list)
        sql = f'''
            SELECT EXISTS (
            SELECT {column_id}
            FROM `{destination_table}`
        '''
        if is_partitioned:
            sql += f'''    WHERE {partition_field} >= DATE_SUB(current_date, INTERVAL 1 DAY)  
                             AND {partition_field} = (SELECT MAX({partition_field}) FROM `{destination_table}` WHERE {partition_field} >= DATE_SUB(current_date, INTERVAL 1 DAY))'''
        sql += f'''
            GROUP BY {column_id}
            HAVING COUNT(*) > 1
            )
            '''
        return sql

    def test_set_of_values(self, destination_table, column_ids_list, set_of_values, is_partitioned, partition_field):
        values = ','.join("'" + col + "'" for col in set_of_values)
        column_id = ','.join(column_ids_list)
        sql = f'''
            SELECT EXISTS (
            SELECT {column_id}
            FROM `{destination_table}`
        '''
        if is_partitioned:
            sql += f'''    WHERE {column_id} not in ({values})
                             AND {partition_field} >= DATE_SUB(current_date, INTERVAL 1 DAY) 
                             AND {partition_field} = (SELECT MAX({partition_field}) FROM `{destination_table}` 
                                                    WHERE {partition_field} >= DATE_SUB(current_date, INTERVAL 1 DAY)))'''
        else:
            sql += f"WHERE {column_id} not in ({values}) )"

        return sql

    def test_range_of_values(self, destination_table, column_ids_list, min_value, max_value, is_partitioned,
                             partition_field):
        column_id = ','.join(column_ids_list)
        sql = f'''
            SELECT EXISTS (
            SELECT {column_id}
            FROM `{destination_table}`
        '''
        if is_partitioned:
            sql += f'''    WHERE {column_id} not between {min_value} and {max_value} 
                             AND {partition_field} >= DATE_SUB(current_date, INTERVAL 1 DAY) 
                             AND {partition_field} = (SELECT MAX({partition_field}) FROM `{destination_table}` 
                                                    WHERE {partition_field} >= DATE_SUB(current_date, INTERVAL 1 DAY)))'''
        else:
            sql += f"WHERE {column_id} not between {min_value} and {max_value} )"

        return sql

    def test_table_rows_count(self, destination_table, min_value, max_value, is_partitioned, partition_field):
        sql = f'''
            SELECT EXISTS (
            SELECT COUNT(*) 
            FROM `{destination_table}`
        '''
        if is_partitioned:
            sql += f'''    WHERE  {partition_field} >= DATE_SUB(current_date, INTERVAL 1 DAY) 
                             AND {partition_field} = (SELECT MAX({partition_field})
                                                        FROM `{destination_table}` 
                                                        WHERE {partition_field} >= DATE_SUB(current_date, INTERVAL 1 DAY))'''
        sql += f'''
            HAVING COUNT(*) between {min_value} and {max_value} 
            )
            '''

        return sql

    def get_values_not_null_query(self, destination_table, column_ids_list, is_partitioned, partition_field):
        new_c = []
        column_id = ','.join(column_ids_list)
        for v in column_ids_list:
            new_c.append(v + ' is null')

        condition_not_null = ' or '.join(new_c)

        sql = f'''
            SELECT EXISTS (
            SELECT {column_id}
            FROM `{destination_table}`
        '''
        if is_partitioned:
            sql += f'''  WHERE ({condition_not_null})
                           AND {partition_field} >= DATE_SUB(current_date, INTERVAL 1 DAY) 
                           AND {partition_field} = (SELECT MAX({partition_field}) FROM `{destination_table}` WHERE {partition_field} >= DATE_SUB(current_date, INTERVAL 1 DAY))'''
        else:
            sql += f"WHERE {condition_not_null}"
        sql += f'''
            GROUP BY {column_id}
            HAVING COUNT(*) > 1
            )
            '''
        return sql

    def run_query(self, sql):
        print(f'Executing query: {sql}')
        client = bigquery.Client(project=self.gcp_project)
        if sql is not None:
            query = list(client.query(sql).result())[0][0]
            return query

    def convert_to_integer(self, value):
        if value is not None:
            if isinstance(value, int):
                return value
            elif isinstance(value, str):
                integer_value = int(value)
                return integer_value
            elif isinstance(value, float):
                float_value = float(value)
                integer_value = int(float_value)
                return integer_value
            else:
                raise Exception("Error: Unable to convert the value to an integer.")

    def test_data(self, destination_table, test_name, column_ids_list,
                  is_partitioned=False, min_value=None, max_value=None,
                  set_of_values=None, partition_field='partition_date', exit_on_failure=False):
        ## duplication QA ##
        if destination_table:
            self.table_name = destination_table.split('.')[2]

        if test_name == 'expect_columns_distinct_values':
            sql = self.get_dup_query(destination_table=destination_table, column_ids_list=column_ids_list,
                                     is_partitioned=is_partitioned, partition_field=partition_field)
        elif test_name == 'expect_columns_values_not_null':
            sql = self.get_values_not_null_query(destination_table=destination_table, column_ids_list=column_ids_list,
                                                 is_partitioned=is_partitioned, partition_field=partition_field)
        elif test_name == 'expect_column_set_of_values':

            if len(column_ids_list) > 1:
                raise ValueError("this test is only available on one column")
            else:
                sql = self.test_set_of_values(destination_table=destination_table, column_ids_list=column_ids_list,
                                              is_partitioned=is_partitioned,
                                              set_of_values=set_of_values, partition_field=partition_field)
        elif test_name == 'expect_table_rows_count_to_be_between':

            sql = self.test_table_rows_count(destination_table=destination_table, is_partitioned=is_partitioned,
                                             min_value=min_value, max_value=max_value, partition_field=partition_field)
        elif test_name == 'expect_column_values_range_to_be_between':
            if len(column_ids_list) > 1:
                raise ValueError("this test is only available on one column")
            sql = self.test_range_of_values(destination_table=destination_table, column_ids_list=column_ids_list,
                                            min_value=min_value, max_value=max_value,
                                            is_partitioned=is_partitioned, partition_field=partition_field)

        qa_result = self.run_query(sql)

        if qa_result:  # True means that the quality test failed
            logging.info(f'#### {test_name} Quality Test failed ####')
            msg_text = f"You test failed {test_name}"
            logging.info(msg_text)
            logging.info(f'{msg_text}')
            logging.info(f'#################')

            if exit_on_failure:
                if exit_on_failure == True:
                    exit(1)
                    raise Exception(f'{test_name} Quality Test failed')
            else:
                self.send_slack_alert(test_name=test_name, table_name=destination_table, slack_token=self.slack_token,
                                      on_call=self.on_call)

        else:
            logging.info(f'{test_name} - TEST passed')

        logging.info(f'{test_name} - Validation test End')
