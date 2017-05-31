try:
    print("This is a test line")

except Exception as e:
    print("exection happend:")
    print(str(e))
    
finally:
    print("Program stopped")