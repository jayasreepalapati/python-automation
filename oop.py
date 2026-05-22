class test_case:
    def __init__(self,test_id,test_name,expected,actual):
        self.test_id=test_id
        self.test_name=test_name
        self.expected=expected
        self.actual=actual
    
    def check_result(self):
        if self.expected==self.actual:
            print("pass",self.test_name)
        else:
            print("fail",self.test_name)
            
tc1=test_case("tc01","logintest","pass","pass")
tc2=test_case("tc02","pwdtest","pass","fail")
tc3=test_case("tc03","logouttest","fail","fail")
    
tc1.check_result()
tc2.check_result()
tc3.check_result()
    
        
        