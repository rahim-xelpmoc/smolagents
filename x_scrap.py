import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Configure Edge options
options = Options()
options.add_argument("--start-maximized")  

# Launch Edge
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

# Open Twitter search page
driver.get("https://x.com/search?q=%23ghiblistyle&src=trend_click&vertical=trends")
time.sleep(30)

# Store seen images to avoid duplicates
seen_images = set()
output_file = "ghibli_images.txt"

try:
    with open(output_file, "w") as file:  # Open file in write mode
        while True:  # Infinite loop to keep fetching images
            # Scroll down to load more images
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(2)  # Wait for new images to load

            # Find all images with class="css-9pa8cd"
            images = driver.find_elements(By.CLASS_NAME, "css-9pa8cd")

            for img in images:
                img_url = img.get_attribute("src")

                # Exclude profile images (URLs containing "profile_images")
                if img_url and "profile_images" not in img_url and img_url not in seen_images:
                    print(img_url)  # Print to console
                    file.write(img_url + "\n")  # Write to file
                    seen_images.add(img_url)  # Store new image

except KeyboardInterrupt:
    print("\nScript stopped by user.")

finally:
    driver.quit()
    print(f"✅ All image URLs saved in '{output_file}'.")
