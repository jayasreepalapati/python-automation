test_passed=[]
test_failed=[]
status_code=[200,404,200,500,200,308,606]
for code in status_code:
    if code ==200:
        test_passed.append(code)
    else:
        test_failed.append(code)
total=len(test_passed)+len(test_failed)
pass_rate=(len(test_passed)/total)*100

print ("test cases run totally are", total)
print("test cases passes are ",len(test_passed))
print("test cases failed are ", len(test_failed))
print("pass rate",pass_rate ,"%")