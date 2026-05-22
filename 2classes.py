class test_case:
    def __init__(self,test_id,test_name,expected,actual):
        self.test_id=test_id
        self.test_name=test_name
        self.expected=expected
        self.actual=actual
        self.status="no result"
    
    def check_result(self):
        if self.expected==self.actual:
           self.status="pass"
           print("pass",self.test_name)
        else:
            self.status="fail"
            print("fail",self.test_name)
    
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

tc1=test_case("tc01","lohintest","pass","fail")
tc2=test_case("tc02","pwdtest","pass","pass")
tc3=test_case("tc03","searchtest","fail","fail")
tc4=test_case("tc04","admintest","pass","pass")
tc5=test_case("tc05","payment","pass","fail")

suit=test_suite("regression testing")
suit.add_test(tc1)
suit.add_test(tc2)
suit.add_test(tc3)
suit.add_test(tc4)
suit.add_test(tc5)

suit.run_all()
suit.print_report()
                
            