#BusSchedule.py
#Name: Pierce Limbo
#Date: 10/20/2025
#Assignment: Homework 2 

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

STOP_NUM = 6767          
ROUTE_NUM = 2
DIRECTION = "WEST"      
def loadURL(url):
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=opts)
    driver.get(url)
    txt = driver.find_element(By.XPATH, "/html/body").text
    driver.quit()
    return txt

def loadTestPage():
    f = open("testPage.txt", "r", encoding="utf-8")
    stuff = f.read()
    f.close()
    return stuff

def parse_times(visible_text):
    result = []
    for line in visible_text.splitlines():
        s = line.strip()
        if ":" in s and ("AM" in s or "PM" in s):
            parts = s.split()
            if len(parts) >= 2:
                maybe = parts[0] + " " + parts[1]
                if ("AM" in maybe or "PM" in maybe) and ":" in maybe:
                    result.append(maybe.replace("am","AM").replace("pm","PM"))
            else:
                result.append(s)
    return result

def getHours(t):
    hh = int(t.split(":")[0])
    pm = "PM" in t
    am = "AM" in t
    if pm and hh != 12:
        hh += 12
    if am and hh == 12:
        hh = 0
    return hh

def getMinutes(t):
    mm = t.split(":")[1].split()[0]
    return int(mm)

def minutes_of_day(h, m):
    return h * 60 + m

def main():
    url = f"https://myride.ometro.com/Schedule?stopCode={STOP_NUM}&routeNumber={ROUTE_NUM}&directionName={DIRECTION}"

    page_text = loadTestPage()

    times = parse_times(page_text)

    from zoneinfo import ZoneInfo
    now_local = datetime.datetime.now(ZoneInfo("America/Chicago"))
    ch, cm = now_local.hour, now_local.minute
    print("Current Time", now_local.strftime("%I:%M %p"))

    central_guess = now_utc - datetime.timedelta(hours=5)  
    ch = central_guess.hour
    cm = central_guess.minute
    now_min = minutes_of_day(ch, cm)

    upcoming = []
    for t in times:
        try:
            bh = getHours(t)
            bm = getMinutes(t)
            bus_min = minutes_of_day(bh, bm)
            if bus_min > now_min:
                upcoming.append((bh, bm))
        except:
            pass
        if len(upcoming) == 2:
            break

    print("Current Time", central_guess.strftime("%I:%M %p"))
    if len(upcoming) == 0:
        print("No upcoming buses found.")
        return

    n1 = minutes_of_day(upcoming[0][0], upcoming[0][1]) - now_min
    print(f"The next bus will arrive in {n1} minutes.")

    if len(upcoming) > 1:
        n2 = minutes_of_day(upcoming[1][0], upcoming[1][1]) - now_min
        print(f"The following bus will arrive in {n2} minutes.")

if __name__ == "__main__":
    main()
