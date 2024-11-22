import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import scapy.all as scapy
import tkinter as tk
from tkinter import messagebox


# Function to initialize the Selenium WebDriver
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Function to scrape website content using BeautifulSoup and Selenium
def scrape_website(url):
    driver = init_driver()
    driver.get(url)
    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    return soup

# Function to check for common web vulnerabilities (SQL Injection, XSS)
def check_vulnerabilities(url):
    vulnerabilities = []

    # Simple SQL Injection test
    sql_test = url + "'"
    sql_response = requests.get(sql_test)
    if "error" in sql_response.text or "warning" in sql_response.text:
        vulnerabilities.append("Potential SQL Injection Vulnerability")

    # Simple XSS test (looking for script tags in the page)
    soup = scrape_website(url)
    for script in soup.find_all("script"):
        if script.get("src"):
            vulnerabilities.append("Potential XSS Vulnerability (External script found)")
        if "<script>" in str(script) and "</script>" in str(script):
            vulnerabilities.append("Potential XSS Vulnerability (Inline script found)")

    # Check for insecure HTTP headers (Content-Security-Policy, X-Content-Type-Options)
    headers = requests.head(url).headers
    if "Content-Security-Policy" not in headers:
        vulnerabilities.append("Missing Content-Security-Policy header")
    if "X-Content-Type-Options" not in headers:
        vulnerabilities.append("Missing X-Content-Type-Options header")

    return vulnerabilities

# Function to analyze network traffic (Simulated)
def analyze_traffic():
    print("Simulating Network Traffic Analysis...")
    # Here you could add Scapy code for network traffic capture
    # Below is just a simple packet capture simulation
    scapy.sniff(count=10, prn=lambda x: x.show())

# Function to display results in a Tkinter GUI
def display_results(vulnerabilities):
    # Initialize Tkinter GUI
    root = tk.Tk()
    root.title("Cybersecurity Web Scraper Results")
    
    # Check if vulnerabilities were found
    if vulnerabilities:
        results = "\n".join(vulnerabilities)
    else:
        results = "No vulnerabilities found!"
    
    label = tk.Label(root, text="Scan Results:", font=('Helvetica', 14))
    label.pack(pady=10)

    result_text = tk.Label(root, text=results, font=('Helvetica', 12))
    result_text.pack(pady=10)
    
    def close_window():
        root.quit()

    close_button = tk.Button(root, text="Close", command=close_window)
    close_button.pack(pady=10)
    
    root.mainloop()

# Main function to control the scraper
def main():
    url = input("Enter the URL to scan (e.g., https://example.com): ")
    
    print(f"Scanning {url} for vulnerabilities...")
    
    vulnerabilities = check_vulnerabilities(url)
    
    # Display results in a Tkinter GUI
    display_results(vulnerabilities)

    # Optionally analyze network traffic
    analyze_traffic()


if __name__ == "__main__":
    main()
