import argparse
from lxml import etree


def main():
    parser = argparse.ArgumentParser(
        prog="junit-to-md-py",
        description="Converts JUnit XML report to markdown format",
    )
    parser.add_argument("file", help="Path to the JUnit XML report file")
    args = parser.parse_args()

    failedTestDetails = []
    allTests = []

    try:
        xmlDoc = etree.parse(args.file)
    except Exception:
        print(f"Error parsing the text from junitOutput!")
        return

    suites = xmlDoc.xpath("//testsuite")
    for suite in suites:
        tests = suite.xpath(".//testcase")
        for test in tests:
            allTests.append(test)
            failures = test.xpath(".//failure")
            for failure in failures:
                failedTestDetails.append(
                    suite.get("name")
                    + "/"
                    + test.get("name")
                    + "\n\n```\n"
                    + failure.text
                    + "\n```"
                )

    if failedTestDetails:
        returnMsg = "### Test Failures:\n"
        for failure in failedTestDetails:
            returnMsg += "- " + failure + "\n"
        print(returnMsg)
    else:
        print("")
