import pyautogui
import time

def twampclient():
    # Open Windows start manu
    pyautogui.press('win')
    time.sleep(1.5)  # 

    # Execute the twampclirnt
    pyautogui.typewrite('twampclient')
    pyautogui.press('enter')
    time.sleep(1.5)  # 

    # Click Destination text box
    pyautogui.click(-1126, 259)
    time.sleep(1.5)  # 

    # Enter the destination address
    pyautogui.typewrite('\b'*10 +'2001:db8:1:1::201')
    pyautogui.press('enter')
    time.sleep(1.5)  #

    # Click light mode check box
    pyautogui.click(-871, 301)
    time.sleep(11.5)  # 

    # Click start button 
    pyautogui.click(-1226, 320)
    time.sleep(510)  # 

    # Click result button 
    pyautogui.click(-900, 553)
    time.sleep(1.5)  # 
   
     # Click close the program button  
    pyautogui.click(-669, 220)
    time.sleep(1.5)  # 

def startRadiusServer():
    # Open Windows start manu
    pyautogui.press('win')
    time.sleep(1.5)  # 

    # Execute the twampclirnt
    pyautogui.typewrite('tekradius lt manager')
    pyautogui.press('enter')
    time.sleep(5)  # 

    # Permit 
    pyautogui.click(792, 524)
    time.sleep(10)  # 


def stopRadiusServer():
    # Service 
    pyautogui.click(128, 93)
    time.sleep(1.5)  # 

    # Stop 
    pyautogui.click(128, 90)
    time.sleep(1.5)  # 

    # Click close the program button  
    pyautogui.click(975, 63)
    time.sleep(1.5)  # 
