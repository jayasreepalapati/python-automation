class test_suite:
    def __init__(self,test_suit_name):
        self.testcases=[]
        self.test_suit_name=test_suit_name
        
    
    def add_test(self,testcase):
        self.testcases.append(testcase)
        
suit=test_suite("regression test")
print("suit name",suit.test_suit_name)
print("length of test cases are ",len(suit.testcases))

suit.add_test("login test")
suit.add_test("pwd test")
suit.add_test("search test")

print("length of test cases after adding are ",len(suit.testcases))
