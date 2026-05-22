class test_suite:
    def __init__(self,test_suit_name):
        self.testcases=[]
        self.test_suit_name=test_suit_name
        
    
    def add_test(self,testcase):
        self.testcases.append(testcase)
        
    def run_all(self):
        print("running",self.test_suit_name)
        for test in self.testcases:
            test.check_result()
    
    def print_report(self):
        print("\n summary")
        passed=[]
        failed=[]
        for test in self.testcases:
            if test.status=="pass":
                passed.append(test.test_id)
            else:
                failed.append(test.test_id)
        print("total:",len(self.testcases))
        print("passed are ",len(passed))
        print("failed are ",len(failed))
