import json
import yaml
from liveramp_automation.logger import Logger


class Report:

    @staticmethod
    def read_json_report(path) -> dict:
        with open(path, 'r') as file:
            # Read all the content of the file
            json_string = file.read()
            data = json.loads(json_string)
        return data

    @staticmethod
    def load_config(env):
        with open(f"config/config.{env}.yaml") as f:
            return yaml.safe_load(f)

    @staticmethod
    def deal_api_json(item):
        nodeid = item["nodeid"]
        outcome = item["outcome"]
        groupName = nodeid.split("/")[1]
        testcase = {}
        testcase["groupName"] = groupName
        testcase["className"] = nodeid.split("/")[2].split("::")[0]
        testcase["caseName"] = nodeid.split("/")[-1].split("::")[-1]
        if outcome.upper() == "failed".upper():
            flag = 0
            errorMessage = str(item["call"]["crash"])
        else:
            flag = 1
            errorMessage = None
        testcase["flag"] = flag
        testcase["errorMessage"] = errorMessage
        testcase["duration"] = float(item["call"]["duration"])
        return testcase

    @staticmethod
    def read_junit_xml_report(path):
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        # Get the root element of the XML tree
        root = tree.getroot()
        # Get the values of the errors, failures, skipped, and tests attributes from the testsuite element
        testsuite = root.find('testsuite')
        errors = int(testsuite.get('errors'))
        failures = int(testsuite.get('failures'))
        skipped = int(testsuite.get('skipped'))
        tests = int(testsuite.get('tests'))
        if errors == 0 and failures == 0 and tests > 0:
            print('Exit code 0')
            Logger.info("All test cases run sucessfully")
            # sys.exit(0)
            print(0)
        elif errors == 0 and failures != 0 and tests > 0:
            print('Exit code 1')
            print(1)
            Logger.info("Some test cases run failed")
        elif errors != 0:
            print('Exit code 3')
            print(3)
            Logger.info("Some scripts have issues and please check")


if __name__ == '__main__':
    Report.read_junit_xml_report("./reports/junit.xml")
