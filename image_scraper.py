from playwright.sync_api import sync_playwright
def generate(prompt, save="generated.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page(
            accept_downloads=True
        )

        page.goto(
            "https://freegen.app/",
            wait_until="domcontentloaded",
            timeout=120000
        )

        page.locator("#prompt").wait_for()

        with open("script.txt", "r", encoding="utf-8") as f:
                print(f"Generating image...")

                page.locator("#prompt").fill(prompt)
                page.locator("#generateBtn").click()

                # Wait for the download button to appear
                download_button = page.locator('a[download="generated_image.jpg"]').last
                download_button.wait_for(state="visible", timeout=0)

                # Download the image
                with page.expect_download() as download_info:
                    download_button.click()

                download = download_info.value
                download.save_as(save)


    browser.close()