import pyautogui as spam
import time 

print("How many messages do you want to send? ") 
limit = int(input()) 
message = input("What do you want to send? ")

i = 0 

time.sleep(5) 

while i < limit: 
    spam.typewrite(message)
    spam.press("enter")
    i += 1 