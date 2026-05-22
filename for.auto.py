test_urls=["https://facebook.com","https://google.com","https://amazon.com"]
for url in test_urls:
    print("testing:"+ url)
    test_results=[]
    test_results.append("login test-passed")
    test_results.append("search test failed")
    test_results.append("checkout test passed")
    
    print("\n test results:")
    for result in test_results:
        print(result)