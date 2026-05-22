def run_test(test_name,expected,actual):
    if expected==actual:
        status="pass"
        message="test case passed succesfully"
    else:
        status="fail"
        message="expected this"+expected+"but got this"+actual
    return status,message

status,message=run_test("lohintest","pass","pass")
print("status",status)
print("message",message)
print("--------")
status,message=run_test("passwordtest","pass","fail")
print("status",status)
print("message",message)
print("--------")

status,message=run_test("search test","fail","fail")
print("status",status)
print("message",message)
