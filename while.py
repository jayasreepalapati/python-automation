test_status="fail"
count=0
max_tries=3

while count<max_tries:
    count +=1
    print("attempt",count,"running-test")
    
    if count ==2:
        test_status="pass"
        break

if test_status=="pass":
    print("test passed on attempt",count)
else:
    print("test failed",max_tries,"attempts")
    