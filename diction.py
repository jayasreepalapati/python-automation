test_cases={"test_caseid":"tc001","test_name":"login with valid credentials","url":"https://google.com","username":"jaya@gmail.com","password":"test@1234","status":"not run"}
print("test_id =",test_cases["test_caseid"])
print("testname =",test_cases["test_name"])
print("loginuser =",test_cases["username"])
print("test_url =",test_cases["url"])
print("userpwd=",test_cases["password"])
print("status =",test_cases["status"])

#after running
test_cases["status"]="passed"
print("after running status =",test_cases["status"])

test_cases["execution_time"]="2.5 seconds"
print("execution time is :",test_cases["execution_time"])