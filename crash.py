try:
    number = int(input("enter a number \n"))
    result= 10/number
    print("result is",result)

except ZeroDivisionError:
    print(" cannot be divided by zero")

except ValueError:
    print("please enter a valid number")
    
finally:
    print("program continues")
    
    