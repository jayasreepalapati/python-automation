test_suite=[{"test-id":"tc01",
            "test-name":"enter valid credentilas",
            "expected":"pass",
            "actual":"pass"},
            {"test-id":"tc02",
            "test-name":"enter wrong password",
            "expected":"fail",
            "actual":"fail"},
            {"test-id":"tc03",
            "test-name":"enter empty username",
            "expected":"fail",
            "actual":"pass"},
            {"test-id":"tc04",
            "test-name":"enter admin credentisls",
            "expected": "pass",
            "actual":"pass"}]
test_passed=[]
test_failed=[]
for test in test_suite:
    if test["expected"]==test["actual"]:
        test_passed.append(test["test-id"])
        print("test passed :",test["test-name"])
    else:
        test_failed.append(test["test-id"])
        print("test failed:",test["test-name"])
        
#summary
print("total no. of test cases run",len(test_suite))
print("test cases pass =",len(test_passed))
print("test cases failed =",len(test_failed))
print("failed are ",test_failed)