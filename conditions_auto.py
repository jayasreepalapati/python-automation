status_code=int(input("enter the https_stats_code"))

if status_code == 200:
    print("test passed")
elif status_code == 400:
    print("error page not found")
elif status_code == 500:
    print("error server not found")
else :
    print("unknown test code")

