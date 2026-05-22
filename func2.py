def check_result(test_name,expected,actual,priority="medium"):
    if expected==actual:
        print("test case pass",test_name,priority)
    else:
        print("test case failed",test_name,priority)
        
        
check_result("login test","pass","pass")

check_result("passwordtest","fail","fail",priority="high")
check_result("searchtest","pass","fail",priority="low")