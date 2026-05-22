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
    
    def get_summary(self):
        print("summary report with test_id",self.test_id,"test_name",self.test_name,"status",self.status)
            
tc1=test_case("tc01","logintest","pass","pass")
tc2=test_case("tc02","pwdtest","pass","fail")
tc3=test_case("tc03","logouttest","fail","fail")
    
tc1.check_result()
tc2.check_result()
tc3.check_result()

tc1.get_summary()
tc2.get_summary()
tc3.get_summary()