test_result=[]
for i in range(1,6):
    result="test" +str(i) +"-passed"
    test_result.append(result)
    print("test cases ran =" ,len(test_result))
    print("all results" ,test_result)