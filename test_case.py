class test_case:
    def __init__(self,test_id,test_name,expected,actual):
        self.test_id=test_id
        self.test_name=test_name
        self.expected=expected
        self.actual=actual
        self.status="not run"
    
    def check_result(self):
        try:
            if self.expected==self.actual:
               self.status="pass"
               print("pass",self.test_name)
            else:
               self.status="fail"
               print("fail",self.test_name)
        except Exception as e:
            self.status="error"
            print("error",self.test_name,":",str(e))
            

