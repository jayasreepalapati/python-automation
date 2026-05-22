def check_result(test_name,actual,expected):
    if expected==actual:
        print("test case with ",test_name ,"is passed")
        return "pass"
    else :
        print("test case with ",test_name,"is failed")
        return "fail"

test_suite=[{"test-id":"tc01","name":"logintest","expected":"pass","actual":"pass"},
            {"test-id":"tc02","name":"searchtest","expected":"pass","actual":"fail"},
            {"test-id":"tc03","name":"passwordtest","expected":"fail","actual":"fail"},
            {"test-id":"tc01","name":"logout","expected":"pass","actual":"pass"}]

test_pass=[]
test_fail=[]

for test in test_suite:
    result=check_result(test["name"],test["actual"],test["expected"])
    if result=="pass":
        test_pass.append(test["test-id"])
    else:
        test_fail.append(test["test-id"])
        
print("total of test cases ran",len(test_suite))
print("passed",len(test_pass))
print("failed are ",len(test_fail))
        
    
    