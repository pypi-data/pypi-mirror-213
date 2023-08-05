# -*- coding:UTF-8 -*-
import unittest
from halring.jenkins_lib.halring_jenkins import JenkinsUtil


class TestAutoIntegTool(unittest.TestCase):
    def test_001_jenkins_get_job_info(self):
        util= JenkinsUtil("http://196.123.133.13:8080","bpc01","111111")
        util.jenkins_login()
        result = util.jenkins_get_job_info("test_no_build_job")
        print(result)

    def test_002_jenkins_build_job(self):
        util = JenkinsUtil("http://196.123.133.13:8080","bpc01","111111")
        util.jenkins_login()
        result = util.build_job("bpc-bizdata-build-rh7",{'Version' : '10.10.10'})
        print(result)

    def test_004_jenkins_wrong_url(self):
        util = JenkinsUtil("http://196.123.133.13:8080", "bpc01", "111111")
        util.jenkins_login()
        result = util.build_job("bpc-EzBZ-RHEL7-build",{"BuildType":"release","Version":"10.10.10","Dynamic_Lib_MOD":"Y"})
        print(result)

    def test_005_jenkins_get_job_info(self):
        util = JenkinsUtil("http://196.123.133.13:8080", "bpc01", "Jen@8kins")
        util.jenkins_login()
        result = util.jenkins_get_job_info("bpc-auto-install-build")
        print(result)


    def test_006_jenkins_build_hidden_parameters(self):
        util = JenkinsUtil("http://196.123.133.13:8080", "bpc01", "Jen@8kins")
        util.jenkins_login()
        result = util.build_job

    def test_007_jenkins_build_not_enough_parameters(self):
        util = JenkinsUtil("http://10.112.6.207:8080", "admin", "Cvsopuser@2019")
        util.jenkins_login()
        result = util.build_job("Test-Switch-Build",{"SuccessSwitch":"T"})

    def test_decorator_001(self):
        util = JenkinsUtil("http://10.112.6.207:8080", "admin", "Cvsopuser@2019")
        util.jenkins_login()
        print(util.check_job_in_building_with_retry("Test-Switch-Build",retry_times=4))

    def test_008_jenkins_console_output(self):
        util = JenkinsUtil("http://196.123.133.13:8080", "admin", "Cvsopuser@2019")
        util.jenkins_login()
        result = util.jenkins_get_build_console_output("http://196.123.133.13:8080/view/TDGW/job/TDGW_auxiliary_build/20/")
        print(result)
        pass

    def test_009_jenkins_key_console_output(self):
        util = JenkinsUtil("http://196.123.133.13:8080", "admin", "Cvsopuser@2019")
        util.jenkins_login()
        result = util.find_str_after_key_from_console_output("http://196.123.133.13:8080/view/TDGW/job/TDGW_auxiliary_build/20/", "artifactory_daily_package_path:")
        print(result)
        pass

    def test_010_jenkins_key_console_output(self):
        util = JenkinsUtil("http://10.112.6.207:8080", "admin", "Cvsopuser@2019")
        util.jenkins_login()
        result = util.get_jobs_not_in_views()
        print(result)
        pass

    def test_011_jenkins_key_console_output(self):
        util = JenkinsUtil("http://196.123.133.13:8080", "admin", "Cvsopuser@2019")
        util.jenkins_login()
        result = util.get_jobs_not_in_views()
        print(result)
        pass



