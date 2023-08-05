#!/usr/bin/env python3
import requests
import time
import re
from pathlib import Path
from qualys_etl.etld_lib import etld_lib_functions as etld_lib_functions
from qualys_etl.etld_lib import etld_lib_config as etld_lib_config
from qualys_etl.etld_lib import etld_lib_credentials as etld_lib_credentials
from qualys_etl.etld_lib.etld_lib_sqlite_tables import get_q_knowledgebase_min_max_dates
from qualys_etl.etld_lib import etld_lib_extract_transform_load_distribute as etld_lib_extract_transform_load_distribute

global url
global payload
global use_cookie
global qualys_headers
global kb_last_modified_after
global xml_file


def setup_vars_required_for_direct_execution_of_main():
    global kb_last_modified_after
    global xml_file
    (min_date, max_date) = get_q_knowledgebase_min_max_dates(etld_lib_config.kb_sqlite_file)
    # TODO add date_time function to convert YYYY-MM-DDThh:mm:ssZ into date - 7 days.
    # TODO take guess work out of knowledgebase updates using last modified - 7 from db.
    etld_lib_functions.logger.info(f"Found Q_KnowledgeBase Min Date: {min_date} Max Date: {max_date}")
    if str(min_date).__contains__("1999"):
        kb_last_modified_after = re.sub(" .*$", "T00:00:00Z", max_date)
        etld_lib_functions.logger.info(f"Found knowledgebase max date of: {max_date}")
        etld_lib_config.kb_last_modified_after = kb_last_modified_after
        etld_lib_functions.logger.info(f"     using kb_last_modified_after={kb_last_modified_after}")
    else:
        etld_lib_functions.logger.info(f"Did not find full knowledgebase, rebuilding...")
        etld_lib_functions.logger.info(f"     using kb_last_modified_after=1970-01-01T00:00:00Z")
        etld_lib_config.kb_last_modified_after = '1970-01-01T00:00:00Z'
        kb_last_modified_after = etld_lib_config.kb_last_modified_after

    try:
        xml_file
    except:
        xml_file = etld_lib_config.kb_xml_file


def check_initial_user(cred_dict):
    if cred_dict['username'] == 'initialuser':
        etld_lib_functions.logger.error(f"Please create your credentials using qetl_manage_user. User is default user {cred_dict['username']}")
        exit(1)


def knowledgebase_extract():
    global url
    global payload
    global use_cookie
    global qualys_headers
    global kb_last_modified_after
    global xml_file

    cred_dict = etld_lib_credentials.get_cred()
    check_initial_user(cred_dict)
    authorization = cred_dict['authorization']
    use_cookie = etld_lib_credentials.use_cookie
    url = f"https://{cred_dict['api_fqdn_server']}/api/2.0/fo/knowledge_base/vuln/"

    payload = {'action': 'list', 'details': 'All', 'show_disabled_flag': '1', 'show_qid_change_log': '1',
               'show_supported_modules_info': '1', 'show_pci_reasons': '1',
               'last_modified_after': kb_last_modified_after}

    etld_lib_functions.logger.info(f"api call    - {url}")
    etld_lib_functions.logger.info(f"api options - {payload}")
    etld_lib_functions.logger.info(f"cookie      - {use_cookie}")

    if use_cookie is False:
        headers = {'X-Requested-With': 'qualysetl', 'Authorization': authorization}
    else:
        headers = {'X-Requested-With': 'qualysetl', 'Cookie': etld_lib_credentials.get_cred()}

    # TODO: create method to build payload.  Allow users options to adjust payload.
    try_extract_max_count = 3
    chunk_size_calc = 20480
    try_extract_max_count = 3
    http_conn_timeout = 30  #
    qualys_headers = {}
    multi_proc_batch_number = None
    etld_lib_extract_transform_load_distribute.extract_qualys(
        try_extract_max_count=try_extract_max_count,
        url=url,
        headers=headers,
        payload=payload,
        http_conn_timeout=http_conn_timeout,
        chunk_size_calc=chunk_size_calc,
        xml_file=xml_file,
        cred_dict=cred_dict,
        qualys_headers_dict=qualys_headers,
        multi_proc_batch_number=multi_proc_batch_number)

    # chunk_size_calc = 20480
    # try_extract_max_count = 3
    # for _ in range(try_extract_max_count):
    #     try:
    #         with requests.request("POST", url, stream=True, headers=headers, data=payload, timeout=30) as r:
    #             #  TODO: check concurrent connections information
    #             qualys_headers = etld_lib_credentials.get_qualys_headers(r)
    #             if r.status_code == 200:
    #                 with open(xml_file, "w", encoding='utf-8') as f:
    #                     for chunk in r.iter_content(chunk_size=chunk_size_calc):
    #                         #  TODO: add chunks to queue, use queue limited to last 2, concat and check for errors.
    #                         f.write(chunk.decode('utf-8'))
    #             else:
    #                 if r.status_code == 401:
    #                     etld_lib_functions.logger.error(f"HTTP {r.status_code}. "
    #                                           f"Validate credentials for user: {cred_dict['username']}  url: {url}")
    #                 elif r.status_code == 409:
    #                     etld_lib_functions.logger.error(f"Exceeding concurrent connections for endpoint: {url}")
    #                 else:
    #                     etld_lib_functions.logger.error(f"HTTP {r.status_code}, exiting.")
    #                 exit(1)
    #     except Exception as e:
    #         etld_lib_functions.logger.warning(f"Warning for extract xml file: {Path(xml_file).name}")
    #         etld_lib_functions.logger.warning(f"Warning {e}")
    #         etld_lib_functions.logger.warning(f"Retry attempt number: {_}")
    #         time.sleep(10)
    #         continue
    #     else:
    #         break  # Success
    # else:
    #     etld_lib_functions.logger.error(f"Max retries attempted: {try_extract_max_count}")
    #     etld_lib_functions.logger.error(f"extract xml file: {Path(xml_file).name}")
    #     exit(1)


def start_msg_knowledgebase_extract():
    etld_lib_functions.logger.info(f"start")


def end_msg_knowledgebase_extract():
    global url
    global qualys_headers
    global kb_last_modified_after
    global xml_file
    etld_lib_functions.log_file_info(url, 'in')
    etld_lib_functions.log_file_info(xml_file)
    for h in qualys_headers.keys():
        etld_lib_functions.logger.info(f"Qualys Header: {h} = {qualys_headers[h]}")
    etld_lib_functions.logger.info(f"end")


def main():
    start_msg_knowledgebase_extract()
    setup_vars_required_for_direct_execution_of_main()
    knowledgebase_extract()
    end_msg_knowledgebase_extract()


if __name__ == "__main__":
    etld_lib_functions.main(my_logger_prog_name='knowledgebase_extract')
    etld_lib_config.main()
    etld_lib_credentials.main()
    main()
