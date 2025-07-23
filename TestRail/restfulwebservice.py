# https://adc.github.trendmicro.com/Corp-ETSTools/testraildemo/tree/master/RestfulAPI
import base64
import json
import requests
from urllib.parse import urlencode


class APIClient:
    def __init__(self, base_url):
        self.user = ''
        self.password = ''
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'testrailrestful/rest/v3/'

    def send_get(self, uri, filepath=None):
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for 'get_attachment/:attachment_id'.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request('GET', uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri
        print(url)
        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {'Authorization': 'Basic ' + auth}

        if method == 'POST':
            if uri.find('add_attachment_to_result') != -1:    # add_attachment API method
                files = {'attachment': (open(data, 'rb'))}
                response = requests.post(url, headers=headers, files=files)
                files['attachment'].close()
            else:
                headers['Content-Type'] = 'application/json'
                payload = bytes(json.dumps(data), 'utf-8')
                response = requests.post(url, headers=headers, data=payload)
        else:
            headers['Content-Type'] = 'application/json'
            response = requests.get(url, headers=headers)

        if response.status_code > 201:
            try:
                error = response.json()
            except:     # response.content not formatted as JSON
                error = str(response.content)
            raise APIError('TestRail API returned HTTP %s (%s)' % (response.status_code, error))
        else:
            if uri[:15] == 'get_attachment/':   # Expecting file, not JSON
                try:
                    open(data, 'wb').write(response.content)
                    return (data)
                except:
                    return ("Error saving attachment.")
            else:
                try:
                    return response.json()
                except: # Nothing to return
                    return {}

    # attachment
    def get_attachments_for_case(self, case_id):
        return self.send_get('attachment/get_attachments_for_case/' + str(case_id))

    def get_attachments_for_test(self, test_id):
        return self.send_get('attachment/get_attachments_for_test/' + str(test_id))

    def get_attachment(self, attachment_id):
        return self.send_get('attachment/get_attachment/' + str(attachment_id))

    def add_attachment_to_result(self, result_id, dic):
        return self.send_post('attachment/add_attachment_to_result/' + str(result_id), dic)

    def delete_attachment(self, attachment_id):
        return self.send_post('attachment/delete_attachment/' + str(attachment_id), None)

    # case
    def get_case(self,case_id):
        return self.send_get('case/get_case/'+str(case_id))

    def get_cases(self,project_id,suite_id,sectoin_id):
        return self.send_get('case/get_cases/'+str(project_id)+'?suite_id='
                             +str(suite_id)+'&section_id='+str(sectoin_id))

    def add_case(self, section_id,dic):
        return self.send_post('case/add_case/'+str(section_id),dic)

    def update_case(self, case_id, dic):
        return self.send_post('case/update_case/' + str(case_id), dic)

    def delete_case(self, case_id):
        return self.send_post('case/delete_case/' + str(case_id), None)

    # case fields
    def get_case_fields(self, project_id):
        return self.send_get('ets_case/get_case_fields/' + str(project_id))
    # case type
    def get_case_types(self):
        return self.send_get('get_case_types')

    # configuration
    def get_configs(self, project_id):
        return self.send_get('configuration/get_configs/' + str(project_id))

    def add_config_group(self, project_id, dic):
        return self.send_post('configuration/add_config_group/' + str(project_id), dic)

    def update_config_group(self, config_group_id, dic):
        return self.send_post('configuration/update_config_group/' + str(config_group_id), dic)

    def add_config(self, config_group_id, dic):
        return self.send_post('configuration/add_config/' + str(config_group_id), dic)

    def update_config(self, config_id, dic):
        return self.send_post('configuration/update_config/' + str(config_id), dic)

    def delete_config(self, config_id):
        return self.send_post('configuration/delete_config/' + str(config_id), None)

    def delete_config_group(self, config_group_id):
        return self.send_post('configuration/delete_config_group/' + str(config_group_id), None)

    # milestone
    def get_milestone(self, milestone_id):
        return self.send_get('milestone/get_milestone/' + str(milestone_id))

    def get_milestones(self, project_id):
        return self.send_get('milestone/get_milestones/' + str(project_id))

    def add_milestone(self, project_id, dic):
        return self.send_post('milestone/add_milestone/' + str(project_id), dic)

    def update_milestone(self, milestone_id, dic):
        return self.send_post('milestone/update_milestone/' + str(milestone_id), dic)

    def delete_milestone(self, milestone_id):
        return self.send_post('milestone/delete_milestone/' + str(milestone_id), None)

    # plan
    def get_plan(self, milestone_id):
        return self.send_get('plan/get_plan/' + str(milestone_id))

    def get_plans(self, project_id):
        return self.send_get('plan/get_plans/' + str(project_id))

    def add_plan(self, project_id, dic):
        return self.send_post('plan/add_plan/' + str(project_id), dic)

    def update_plan(self, plan_id, dic):
        return self.send_post('plan/update_plan/' + str(plan_id), dic)

    def re_plan(self, plan_id, dic):
        return self.send_post('ets_plan/re_plan/' + str(plan_id), dic)

    def add_plan_entry(self, plan_id, dic):
        return self.send_post('plan/add_plan_entry/' + str(plan_id), dic)

    def update_plan_entry(self, plan_id, entry_id, dic):
        return self.send_post('plan/update_plan_entry/' + str(plan_id) + '/' + str(entry_id), dic)

    def delete_plan_entry(self, plan_id, entry_id):
        return self.send_post('plan/delete_plan_entry/' + str(plan_id) + '/' + str(entry_id), None)

    def close_plan(self, plan_id):
        return self.send_post('plan/close_plan/' + str(plan_id), None)

    def delete_plan(self, plan_id):
        return self.send_post('plan/delete_plan/' + str(plan_id), None)
    # priority
    def get_priorities(self):
        return self.send_get('get_proorities')
    # project
    def get_project(self, project_id):
        return self.send_get('get_project/' + str(project_id))

    def get_projects(self):
        return self.send_get('get_projects')

    # report
    def get_reports(self, porject_id):
        return self.send_get('report/get_reports/' + str(porject_id))

    def run_report(self, report_template_id):
        return self.send_get('report/run_report/' + str(report_template_id))
    # results
    def get_results_for_case(self, run_id,case_id):
        return self.send_get('result/get_results_for_case/' + str(run_id)+"/"+ str(case_id))

    def get_results_for_run(self, run_id):
        return self.send_get('result/get_results_for_run/' + str(run_id))

    def get_results(self, test_id):
        return self.send_get('result/get_results/' + str(test_id))

    def add_result_for_case(self, run_id, case_id, dic):
        return self.send_post('result/add_result_for_case/' + str(run_id) + '/' + str(case_id), dic)

    def add_results_for_cases(self, run_id, dic):
        return self.send_post('result/add_results_for_cases/' + str(run_id), dic)

    def add_result(self, test_id, dic):
        return self.send_post('result/add_result/' + str(test_id), dic)

    def add_results(self, run_id, dic):
        return self.send_post('result/add_results/' + str(run_id), dic)

    # result fields
    def get_result_fields(self):
        return self.send_get('get_result_fields')

    # run
    def get_run(self, run_id):
        return self.send_get('run/get_run/' + str(run_id))

    def get_runs(self, project_id):
        return self.send_get('run/get_runs/' + str(project_id))

    def add_run(self, project_id, dic):
        return self.send_post('run/add_run/' + str(project_id), dic)

    def update_run(self, run_id, dic):
        return self.send_post('run/update_run/' + str(run_id), dic)

    def close_run(self, run_id):
        return self.send_post('run/close_run/' + str(run_id), None)

    def delete_run(self, run_id):
        return self.send_post('run/delete_run/' + str(run_id), None)

    # section
    def get_section(self,section_id):
        return self.send_get('section/get_section/'+str(section_id))

    def get_sections(self,project_id,suite_id):
        return self.send_get('section/get_sections/'+str(project_id)+'?suite_id='+str(suite_id))

    def add_section(self,project_id,dic):
        return self.send_post('section/add_section/'+str(project_id),dic)

    def update_section(self,section_id,dic):
        return self.send_post('section/update_section/'+str(section_id),dic)

    def delete_section(self,section_id):
        return self.send_post('section/delete_section/'+str(section_id),None)

    # status
    def get_statuses(self):
        return self.send_get('get_statuses')

    # suite
    def get_suite(self, suite_id):
        return self.send_get('suite/get_suite/' + str(suite_id))

    def get_suites(self, project_id):
        return self.send_get('suite/get_suites/' + str(project_id))

    def add_suite(self, project_id, dic):
        return self.send_post('suite/add_suite/' + str(project_id), dic)

    def update_suite(self, suite_id, dic):
        return self.send_post('suite/update_suite/' + str(suite_id), dic)

    def delete_suite(self, suite_id):
        return self.send_post('suite/delete_suite/' + str(suite_id), None)

    # template
    def get_templates(self, project_id):
        return self.send_get('get_templates/' + str(project_id))

    # test
    def get_test(self, test_id):
        return self.send_get('test/get_test/' + str(test_id))

    def get_tests(self, run_id):
        return self.send_get('test/get_tests/' + str(run_id))

    #user
    def get_users(self):
        return self.send_get('user/get_users')

    def get_user(self,user_id):
        return self.send_get('user/get_user/'+str(user_id))

    def get_user_by_email(self,email):
        return self.send_get('user/get_user_by_email?email='+str(email))

    def get_sort_filter_cases(self,dic):
        params = urlencode(dic)
        return self.send_get('ets_report/suites/get_sort_filter_cases?'+params)

    def get_case_count_by_test_type(self, dic):
        params = urlencode(dic)
        return self.send_get('ets_report/suite/get_case_count_by_test_type?' + params)

    def get_case_by_test_type(self, dic):
        params = urlencode(dic)
        return self.send_get('ets_report/suite/get_case_by_test_type?' + params)


class APIError(Exception):
    pass