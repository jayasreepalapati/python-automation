test_cases=["lohintest","password  test","search test","google test"]
for test in test_cases:
    print("running:",test)


for index ,test in enumerate(test_cases):
    print(index +1,"running:",test)
    
for i in range(1,6):
    print("test number:",i)
    
test={"test-id":"tc01","test-name":"login test","status":"pass"}

print("\n test details")
for key,value in test.items():
    print(key,":",value)