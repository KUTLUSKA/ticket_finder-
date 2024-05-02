import asyncio
from pyppeteer import launch
import winsound

async def way_to_ticket(url, search_box_id1, text_to_write1, search_button_id, search_box_id2, text_to_write2, time_id, time ,seferler, next_button):
    browser = await launch({"headless": False, "args": ["--start-maximized"]})
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    await page.setViewport({"width": 1920, "height": 1080})
    
    # Fill the departure, destination and date fields
    await page.type(f"#{search_box_id1}", text_to_write1)
    await page.type(f"#{search_box_id2}", text_to_write2)
    await page.click(f"#{time_id}", clickCount=3)
    await page.keyboard.press('Backspace')
    await page.type(f"#{time_id}", time)
    await page.click('.ui-datepicker-close')  # Assuming this closes the date picker

    # Click the search button
    await asyncio.sleep(2)  # Allow any AJAX/Javascript to complete if necessary
    await page.click(f"#{search_button_id}")
    

    while True:
        found_ticket = False

        # Iterate through all possible train options
        for index, sefer in enumerate(seferler):
            try:
                button_sefer = await page.waitForXPath(sefer, timeout=5000)
                text_b = await page.evaluate('(element) => element.textContent', button_sefer)
                seats_available = int(text_b[23:25])  # Extracting available seats from the text

                print(f"{seats_available} seats available for option {index + 1}")

                if seats_available >= 3:
                    print(f"Ticket found for option {index + 1}, booking now...")
                    await page.click(seferler_button[index])
                    await asyncio.sleep(2)
                    await page.click(next_button)

                    found_ticket = True
                    winsound.Beep(1000, 5000)
                    winsound.Beep(1000, 5000)
                    winsound.Beep(1000, 5000)
                    
            except Exception as e:
                print(f"Error checking sefer {index + 1}: {e}")

        if found_ticket:
            print("Successfully booked a ticket.")
            break  # Break out of the while loop if a ticket is found and booked

        else:
            print("No available tickets found, reloading...")
            await page.reload({'waitUntil': 'networkidle2'})
            await asyncio.sleep(5)  # Wait for some time before the next iteration

    await asyncio.sleep(10)
    await browser.close()

# Usage
url = "https://ebilet.tcddtasimacilik.gov.tr/view/eybis/tnmGenel/tcddWebContent.jsf"
search_box_id1 = "nereden"
text_to_write1 = "İstanbul(Söğütlüçeşme)"
search_box_id2 = "nereye"
text_to_write2 = "ERYAMAN YHT"
search_button_id = "btnSeferSorgula"
time_id = "trCalGid_input"
time = "07.05.2024"
# Update XPath and CSS selectors based on actual values from the website
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
            
]
seferler_button = ['#mainTabView\:gidisSeferTablosu\:0\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:1\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:2\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:3\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:4\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:5\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:6\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:7\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:8\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:9\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:10\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:11\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:12\:j_idt117',
                   '#mainTabView\:gidisSeferTablosu\:13\:j_idt117',
                   
]
next_button = "#mainTabView\:btnDevam44"

asyncio.get_event_loop().run_until_complete(way_to_ticket(url, search_box_id1, text_to_write1, search_button_id, search_box_id2, text_to_write2, time_id, time, seferler, next_button))


