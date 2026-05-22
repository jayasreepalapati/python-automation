test_passed = []
test_failed = []


status_code =[200,404,200,500,308,200]
for code in status_code:
    if code == 200:
        test_passed.append(code)
    else:
        test_failed.append(code)
        
print("passed:",len(test_passed))
print("failed :",len(test_failed))
    