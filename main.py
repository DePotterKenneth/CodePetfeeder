try:
    print("This is a test line")
    print("2")

except Exception as e:
    print("exection happend:")
    print(str(e))


finally:
    print("Program stopped")