from test_case import test_case
from test_suite import test_suite
from test_data import test_data

suite=test_suite("regression testing")

for data in test_data:
    tc=test_case(data["test_id"],
                 data["test_name"],
                 data["expected"],
                 data["actual"])
    suite.add_test(tc)
    
suite.run_all()
suite.print_report()
    