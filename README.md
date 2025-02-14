# Email Crawler GUI

This is a simple, user-friendly GUI application (written in Python) for collecting email addresses from a list of websites. It employs multiple strategies (checking main pages, `/contact` pages, etc.) and displays:

- A progress bar
- An animated spinner
- Colored output based on the source of discovered emails (web, Facebook, Google)

---

## Key Features

1. **Paste or Enter Multiple Websites**  
   - Provide a list of websites (one per line) in a text box.

2. **Advanced Options**  
   - **Contact URL Suffixes**: Define custom suffixes (e.g. `/contact`, `/contact-us`, etc.)  
   - **Excluded Email Patterns**: Patterns like `@example.com` to ignore unwanted emails.

3. **Settings**  
   - **Show All Addresses**: Whether to list every email found, or just the single best match.  
   - **Headless Mode**: Run Chrome invisibly (no browser window).

4. **Progress & Animation**  
   - Progress bar shows the overall completion.  
   - A spinner (`| / - \`) indicates the crawler is busy.

5. **Colored Output**  
   - **Green**: Emails found on the site (web)  
   - **Blue**: Emails discovered via Facebook  
   - **Orange**: Emails obtained via Google

6. **Final Summaries**  
   - A list of processed websites, one per line.  
   - All emails found, color-coded.

---

## Quick Start

1. **Download/Clone**  
   - Place `email_crawler_gui.py` and `requirements.txt` in the same folder.

2. **Install Python Packages**  
   - Open a terminal/cmd in that folder:
     ```bash
     pip install -r requirements.txt
     ```
   - Ensure you have Python 3.7+ and Chrome installed.

3. **Run the GUI**  
   ```bash
   python email_crawler_gui.py
