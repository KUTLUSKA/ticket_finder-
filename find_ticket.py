import asyncio
from pyppeteer import launch
import random

# Example usage:
url = "https://ebilet.tcddtasimacilik.gov.tr/view/eybis/tnmGenel/tcddWebContent.jsf"

#arravie
search_box_id1 = "nereden"  
text_to_write1 = "Ankara Gar" 

#varış
search_box_id2 = "nereye"
text_to_write2 = "İstanbul(Söğütlüçeşme)"

#arama butonu
search_button_id = "btnSeferSorgula"

#tarih bilgisi
time_id = "trCalGid_input"
time= "21.09.2023"


#seferler

seferler = ["//*[@id=\"mainTabView:gidisSeferTablosu:0:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:1:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:2:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:3:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:4:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:5:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:6:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:7:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:8:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:9:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:10:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:11:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:12:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:13:j_idt109:0:somVagonTipiGidis1_input\"]",
            "//*[@id=\"mainTabView:gidisSeferTablosu:14:j_idt109:0:somVagonTipiGidis1_input\"]"
            
]




async def way_to_ticket(url, search_box_id1, text_to_write1, search_button_id, search_box_id2, text_to_write2, time_id, time ,seferler):
    #to open browser
    browser = await launch({"headless": False, "args": ["--start-maximized"]})  
    page = await browser.newPage()
    await page.goto(url,{'waitUntil': 'networkidle2'})
    await page.setViewport({"width": 1920, "height": 1080})
    
    #to access search box "nereden"
    try:
        await page.waitForSelector(f"#{search_box_id1}", timeout=5000)  
        await page.type(f"#{search_box_id1}", text_to_write1)  
        print(f"Typed '{text_to_write1}' in the 'nereden' search box successfully!")
    except Exception as e:
        print(f"Failed to write in the 'nereden' search box: {e}")
    
    #to access search box "nereye"
    try:
        await page.waitForSelector(f"#{search_box_id2}", timeout=5000)  
        await page.type(f"#{search_box_id2}", text_to_write2)  
        print(f"Typed '{text_to_write2}' in the 'nereye' search box successfully!")
    except Exception as e:
        print(f"Failed to write in the 'nereye' search box: {e}")


    #to access search box "tarih"
    try:
        await page.waitForSelector(f"#{time_id}", timeout=5000)  
        await page.click(f"#{time_id}", clickCount=3)  # Select all text in the input field
        await page.evaluate(f'document.querySelector("#{time_id}").value = "";')  # Clear the input field's value
        await page.type(f"#{time_id}", time)  
        print(f"Typed '{time}' in the 'time' search box successfully!")
    except Exception as e:
        print(f"Failed to write in the 'time' search box: {e}")

    #to access search box "tarih"'s close button
    try:
        await page.waitForSelector('.ui-datepicker-close', timeout=5000)  
        await page.click('.ui-datepicker-close')  # Click the button with the specified class
        print("Button clicked successfully!")
    except Exception as e:
        print(f"Failed to click the button: {e}")

    
    
    #to access button "ARA"
    try:
        await asyncio.sleep(3)
        await page.waitForSelector(f"#{search_button_id}") 
        await page.click(f"#{search_button_id}")   
        print("selected")
    except Exception as e:
        print(f"Failed to search button: {e}")
    
    
    sefer_sayaç = 0
    a = True
    a_sayaç = 0
    try:
        while a:
            try:
                for button_sefer in seferler:    
                    if sefer_sayaç == 14:
                        sefer_sayaç == 0
                    else:
                        pass
                    await page.reload(timeout = 5000)
                    await asyncio.sleep(3)
                    button_sefer = await page.waitForXPath(seferler[sefer_sayaç])
                    text_b = await page.evaluate('(button_sefer) => button_sefer.textContent',button_sefer)
                    substring = text_b[23:26]
                    substring_int = int(substring)
                    print (substring," boş yer var")


                    if substring_int > 3:
                        print("ticket find")
                        a = False    
                        sefer_sayaç += 1
                    else:
                        print(a_sayaç,". try still searching")
                        sefer_sayaç+=1
        
        
            except Exception as e:
                print(f"Failed to search button: {e}")
    except Exception as e:
                print(f"Failed to search button: {e}")






    #to see what we done last
    await asyncio.sleep(10)
    await browser.close()

#it starts everything
asyncio.get_event_loop().run_until_complete(way_to_ticket(url, search_box_id1, text_to_write1, search_button_id,search_box_id2,text_to_write2, time_id,time, seferler))