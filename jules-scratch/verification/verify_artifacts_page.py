from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Navigate to the artifacts page
        page.goto("http://localhost:3000/artifacts")

        # Wait for a key element to be visible to ensure the page is loaded
        expect(page.get_by_role("heading", name="Artifact Repository")).to_be_visible(timeout=10000)

        # Give the page a moment to settle, especially for the mock data to populate
        page.wait_for_timeout(1000)

        # Take a screenshot of the entire page
        page.screenshot(path="jules-scratch/verification/artifacts_page.png")

        print("Screenshot taken successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Take a screenshot even on error to help with debugging
        page.screenshot(path="jules-scratch/verification/error_screenshot.png")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
