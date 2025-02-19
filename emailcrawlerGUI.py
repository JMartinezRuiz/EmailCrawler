import undetected_chromedriver as uc
import time
import re
import os
import threading
from difflib import SequenceMatcher
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from selenium.webdriver.common.by import By

# ================================
# Global default advanced options
# ================================
DEFAULT_CONTACT_SUFFIXES = "/contact,/contact-us,/contactus,/contact-info,/careers,/send-us-a-message,/get-in-touch"
DEFAULT_EXCLUDED_EMAILS = "@sentry-next.wixpress.com,@sentry.io,@sentry.wixpress.com,@example.com"


def extract_emails_from_source(source, exclude_list=None):
    """Extract emails using regex and filter out those ending in .jpg, .png or matching any pattern in exclude_list."""
    if exclude_list is None:
        exclude_list = [x.strip().lower() for x in DEFAULT_EXCLUDED_EMAILS.split(",")]
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", source)
    # Filtrar direcciones que terminen en .jpg o .png
    emails = {email for email in emails if not email.lower().endswith((".jpg", ".png"))}
    # Filtrar direcciones que contengan alguno de los patrones excluidos
    emails = {email for email in emails if not any(excl in email.lower() for excl in exclude_list)}
    return emails


def try_url(driver, url, wait_time=5, exclude_list=None):
    """Attempt to load a URL, wait, and extract emails from the page source."""
    try:
        driver.get(url)
        time.sleep(wait_time)
        return extract_emails_from_source(driver.page_source, exclude_list)
    except Exception:
        return set()


def click_contact_link(driver, wait_time=5, exclude_list=None):
    """Look for links containing the text 'contact', click on the first one, and extract emails."""
    try:
        links = driver.find_elements(
            By.XPATH,
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact')]"
        )
        for link in links:
            href = link.get_attribute("href")
            if href:
                try:
                    link.click()
                    time.sleep(wait_time)
                    return extract_emails_from_source(driver.page_source, exclude_list)
                except Exception:
                    continue
    except Exception:
        pass
    return set()


def get_domain(website):
    """Extract the domain from a given URL."""
    try:
        domain = website.split("//")[-1].split("/")[0]
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return website


def google_search_email(driver, website, wait_time=5, exclude_list=None):
    """Perform a Google search for '"domain" email' and extract emails from the results."""
    domain = get_domain(website)
    query = f'"{domain}" email'
    google_url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    try:
        driver.get(google_url)
        time.sleep(wait_time)
        return extract_emails_from_source(driver.page_source, exclude_list)
    except Exception:
        return set()


def extract_emails_for_website(driver, website, show_all=False, contact_suffixes=None, exclude_list=None):
    """
    Attempts several strategies to extract emails for a given website.
    Returns either:
      - A list of (email, source) if show_all = True,
      - A single (best_email, source) if show_all = False
    """
    candidate_emails = []  # List of tuples (email, source)

    # Strategy 1: Main page
    emails = try_url(driver, website, exclude_list=exclude_list)
    if emails:
        candidate_emails.extend([(email, "web") for email in emails])

    # Strategy 2: Contact URL variants
    if not candidate_emails:
        if contact_suffixes is None:
            contact_suffixes = [s.strip() for s in DEFAULT_CONTACT_SUFFIXES.split(",")]
        for suffix in contact_suffixes:
            url_contact = website.rstrip("/") + suffix
            emails = try_url(driver, url_contact, exclude_list=exclude_list)
            if emails:
                candidate_emails.extend([(email, "web") for email in emails])
                break

    # Strategy 3: Click on contact link from main page
    if not candidate_emails:
        emails = click_contact_link(driver, exclude_list=exclude_list)
        if emails:
            candidate_emails.extend([(email, "web") for email in emails])

    # Strategy 3.5: Alternative contact link (href)
    if not candidate_emails:
        try:
            domain = get_domain(website)
            xpath_expr = f"//a[contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact') and contains(@href, '{domain}')]"
            links = driver.find_elements(By.XPATH, xpath_expr)
            for link in links:
                href = link.get_attribute("href")
                if href:
                    link.click()
                    time.sleep(5)
                    emails = extract_emails_from_source(driver.page_source, exclude_list)
                    if emails:
                        candidate_emails.extend([(email, "web") for email in emails])
                        break
        except Exception:
            pass

    # Strategy 4: About page variants
    if not candidate_emails:
        for suffix in ["/about", "/about-us"]:
            url_about = website.rstrip("/") + suffix
            emails = try_url(driver, url_about, exclude_list=exclude_list)
            if emails:
                candidate_emails.extend([(email, "web") for email in emails])
                break

    # Strategy 5: Look for mailto: links
    if not candidate_emails:
        try:
            mailto_links = driver.find_elements(By.XPATH, "//a[starts-with(@href, 'mailto:')]")
            for ml in mailto_links:
                href = ml.get_attribute("href")
                if href:
                    email = href.split("mailto:")[-1]
                    candidate_emails.append((email, "web"))
        except Exception:
            pass

    # Strategy 6: Facebook page
    if not candidate_emails:
        try:
            domain = get_domain(website)
            domain_clean = domain.lower().replace("www.", "")
            base_name = domain_clean.split('.')[0]
            fb_url = f"https://www.facebook.com/{base_name}"
            emails = try_url(driver, fb_url, wait_time=7, exclude_list=exclude_list)
            if emails:
                candidate_emails.extend([(email, "facebook") for email in emails])
        except Exception:
            pass

    # Strategy 7: Google search
    if not candidate_emails:
        emails = google_search_email(driver, website, exclude_list=exclude_list)
        if emails:
            candidate_emails.extend([(email, "google") for email in emails])

    if not candidate_emails:
        return None

    if show_all:
        return candidate_emails

    # Single best candidate
    domain = get_domain(website).lower().replace("www.", "")
    from difflib import SequenceMatcher
    def similarity(email):
        local = email.split("@")[0].lower()
        return SequenceMatcher(None, domain, local).ratio()

    source_priority = {"web": 3, "facebook": 2, "google": 1}
    max_priority = max(source_priority.get(src, 0) for (_, src) in candidate_emails)
    best_candidates = [(email, src) for (email, src) in candidate_emails if source_priority.get(src, 0) == max_priority]
    best_candidate = max(best_candidates, key=lambda tup: similarity(tup[0]))
    mark_star = "*" if len(best_candidates) > 1 else ""
    return (best_candidate[0] + mark_star, best_candidate[1])


def iniciar_driver(headless=False):
    options = uc.ChromeOptions()
    # Se eliminan los argumentos de perfil y directorio de usuario para que funcione en cualquier equipo
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--log-level=3")
    options.add_argument("--silent")

    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36")
    options.add_argument(f"--user-agent={user_agent}")

    if headless:
        options.add_argument("--headless=new")

    driver = uc.Chrome(options=options, version_main=132)
    driver.implicitly_wait(10)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        }
    )
    return driver


class EmailCrawlerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Email Crawler")
        self.geometry("900x700")
        self.resizable(False, False)

        self.input_font = ("Courier New", 10)
        self.output_font = ("Courier New", 10)
        self.output_bg = "black"
        self.output_fg = "white"

        self.show_all = tk.BooleanVar(value=False)
        self.headless_mode = tk.BooleanVar(value=False)
        self.contact_suffixes_str = tk.StringVar(value=DEFAULT_CONTACT_SUFFIXES)
        self.excluded_emails_str = tk.StringVar(value=DEFAULT_EXCLUDED_EMAILS)

        self.create_widgets()

    def create_widgets(self):
        # Websites input area
        input_frame = tk.LabelFrame(self, text="Website List (one per line)", font=("Arial", 12))
        input_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=False)

        self.input_text = scrolledtext.ScrolledText(
            input_frame, wrap=tk.WORD, width=80, height=8, font=self.input_font
        )
        self.input_text.pack(padx=5, pady=5)
        self.input_text.insert(tk.END, "http://www.example.com/\n")

        # Advanced Options: always visible
        adv_frame = tk.LabelFrame(self, text="Advanced Options", font=("Arial", 12))
        adv_frame.pack(fill=tk.X, padx=10, pady=5)

        suffix_frame = tk.Frame(adv_frame)
        suffix_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(suffix_frame, text="Contact URL Suffixes (comma-separated):", font=("Arial", 10)).pack(side=tk.LEFT)
        self.suffix_entry = tk.Entry(suffix_frame, textvariable=self.contact_suffixes_str, font=("Arial", 10), width=60)
        self.suffix_entry.pack(side=tk.LEFT, padx=5)

        excl_frame = tk.Frame(adv_frame)
        excl_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(excl_frame, text="Excluded Email Patterns (comma-separated):", font=("Arial", 10)).pack(side=tk.LEFT)
        self.excluded_entry = tk.Entry(excl_frame, textvariable=self.excluded_emails_str, font=("Arial", 10), width=60)
        self.excluded_entry.pack(side=tk.LEFT, padx=5)

        # Checkbuttons for Show All + Headless
        opts_frame = tk.Frame(self)
        opts_frame.pack(fill=tk.X, padx=10, pady=2)
        tk.Checkbutton(opts_frame, text="Show all addresses", variable=self.show_all, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(opts_frame, text="Headless mode (no browser window)", variable=self.headless_mode, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        # Progress Bar
        progress_frame = tk.Frame(self)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(progress_frame, text="Progress:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=400, mode="determinate")
        self.progress_bar.pack(side=tk.LEFT, padx=5)
        self.progress_label = tk.Label(progress_frame, text="0%", font=("Arial", 10))
        self.progress_label.pack(side=tk.LEFT, padx=5)

        # Animation label
        self.anim_label = tk.Label(self, text="", font=("Arial", 12, "bold"))
        self.anim_label.pack(pady=5)

        # Start Button
        self.start_button = tk.Button(self, text="Start Crawler", command=self.start_crawler, font=("Arial", 12, "bold"))
        self.start_button.pack(pady=5)

        # Output Log
        output_frame = tk.LabelFrame(self, text="Output Log", font=("Arial", 12))
        output_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=self.output_font,
                                                     bg=self.output_bg, fg=self.output_fg)
        self.output_text.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        # Color tags
        self.output_text.tag_config("web", foreground="green")
        self.output_text.tag_config("facebook", foreground="blue")
        self.output_text.tag_config("google", foreground="orange")

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

    def start_crawler(self):
        self.clear_output()
        websites_raw = self.input_text.get(1.0, tk.END).strip().splitlines()
        self.websites = [w.strip() for w in websites_raw if w.strip()]
        if not self.websites:
            messagebox.showwarning("No websites", "Please enter at least one website.")
            return

        contact_suffixes = [s.strip() for s in self.contact_suffixes_str.get().split(",") if s.strip()]
        excluded_emails = [s.strip().lower() for s in self.excluded_emails_str.get().split(",") if s.strip()]

        self.show_all_setting = self.show_all.get()
        self.headless_setting = self.headless_mode.get()

        self.start_button.config(state=tk.DISABLED)
        self.anim_running = True
        self.animate_spinner()
        threading.Thread(
            target=self.run_crawler_gui,
            args=(
                self.headless_setting,
                contact_suffixes,
                excluded_emails,
                self.show_all_setting
            ),
            daemon=True
        ).start()

    def animate_spinner(self):
        spinner_chars = ["|", "/", "-", "\\"]
        def update_spinner(i=0):
            if self.anim_running:
                self.anim_label.config(text=spinner_chars[i % len(spinner_chars)] + " Processing...")
                self.after(200, update_spinner, i+1)
            else:
                self.anim_label.config(text="")
        update_spinner()

    def run_crawler_gui(self, headless, contact_suffixes, excluded_emails, show_all):
        results = {}
        try:
            driver = iniciar_driver(headless=headless)
        except Exception:
            self.output_text.insert(tk.END, f"Error initializing driver.\n")
            self.start_button.config(state=tk.NORMAL)
            self.anim_running = False
            return

        total = len(self.websites)
        for idx, website in enumerate(self.websites, start=1):
            self.output_text.insert(tk.END, f"Processing {website}\n")
            self.output_text.see(tk.END)
            try:
                result = extract_emails_for_website(
                    driver, website,
                    show_all=show_all,
                    contact_suffixes=contact_suffixes,
                    exclude_list=excluded_emails
                )
                results[website] = result
                driver.delete_all_cookies()
                if result:
                    if show_all:
                        # result is a list of (email, src)
                        for email, src in result:
                            self.output_text.insert(tk.END, f"{website} -> ", "normal")
                            self.output_text.insert(tk.END, f"{email} ({src})\n", src)
                    else:
                        email, src = result
                        self.output_text.insert(tk.END, f"{website} -> ", "normal")
                        self.output_text.insert(tk.END, f"{email} ({src})\n", src)
                else:
                    self.output_text.insert(tk.END, f"{website} -> No emails found\n")
            except Exception:
                self.output_text.insert(tk.END, f"{website} -> Error\n")

            percent = int((idx / total) * 100)
            self.progress_bar['value'] = percent
            self.progress_label.config(text=f"{percent}%")
            self.update_idletasks()

        driver.quit()
        self.anim_running = False
        self.output_text.insert(tk.END, "\nCrawler finished.\n")

        # 1) Show final list of all webs
        self.output_text.insert(tk.END, "WEBS PROCESSED (one per line):\n")
        for web in self.websites:
            self.output_text.insert(tk.END, f"{web}\n")

        # 2) Show final list of all emails, in color
        #    We'll combine all addresses into a single list and print them with
        #    the appropriate color tag.
        all_emails = []
        for web, result in results.items():
            if result:
                if show_all:
                    # result is list of tuples
                    for (email, src) in result:
                        all_emails.append((email, src))
                else:
                    # single tuple
                    email, src = result
                    all_emails.append((email, src))

        if all_emails:
            self.output_text.insert(tk.END, "\nEMAILS:\n")
            for (email, src) in all_emails:
                self.output_text.insert(tk.END, email + "\n", src)
        self.start_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = EmailCrawlerGUI()
    app.mainloop()
