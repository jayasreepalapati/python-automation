test_suite=[{"test_id":"tc01","test_name":"logintest","login":"jaya","pwd":"jaya@123"},
            {"test_id":"tc02","test_name":"pwdtest","pwd":"jaya"},
            {"test_id":"tc03","test_name":"searchtest","found":"yes"},
            {"test_id":"tc04","test_name":"ispalindrome","result":"yes"},
            {"test_id":"tc05","test_name":"isfibonacci","result":"yes"}]

def run_test(test_suite):
    for test in test_suite:
        print("test cases",test["test_id"])
        
run_test(test_suite)

mn_try=1
mx_try=2



    
    
    