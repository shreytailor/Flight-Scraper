# Flight Scraper
Did you know that the time at which you book your tickets, actually matters? Friday, at around 3am, is the most expensive time to book tickets because of the way some companies manage their sales - there is usually a spike in the prices before the next week starts off.
This tool which is primarily built with Python, let's you track the prices at certain intervals before you finally make your decision to book the most cheapest and convenient option for you.

There is even a belief that flying on a Wednesday is significantly cheaper, and coming back on a Sunday is more expensive than the other days. To solve this issue, there is an option of using the *'flexible'* option which is pretty much searching within ± 3 days of your selected dates, and looking if the tickets can become even cheaper.

This is my first Python project so along with its vanilla features, I have made the use of the following modules -
- **Selenium** - for automating the browser interactions with KAYAK.com
- **GeckoDriver** - a module/driver which is a linkage between Firefox and the interactions that are given to Selenium so they can be executed successfully.
- **smtplib** - a vanilla python module for sending emails regarding the latest scrape which is performed.

The whole process uses the KAYAK.com website to get the results but none of our actions are violating their [terms and conditions](https://www.nz.kayak.com/terms-of-use) as none of the data extracted from the automation is being used for any commercial purposes. As long as the frequency for scraping isn't high, you won't be loading their servers and causing any trouble.

## Installation
1. Let's first install the dependency required, using the package manager.
```python
pip install selenium
```
2. A driver is also required for your preferred browser. Download the files for your operating system from below -
  - ChromeDriver (Google Chrome) - https://chromedriver.chromium.org/downloads
  - GeckoDriver (Mozilla Firefox) - https://github.com/mozilla/geckodriver/releases

  For Windows, after downloading your required file, just place the executable within your working directory of your project and link it with the 'scraper.py' file by doing the followinhg.
  ```python
  # Find this particular line within the code.
  driver = webdriver.Firefox();

  # ... and replace with the following.
  driver = webdriver.Firefox(full_path_of_driver);
  driver = webdriver.Chrome(full_path_of_driver);
  ```

  For Macintosh, there is a different process because we have to add the driver to the PATH file. For that, use the following [guide](https://www.kenst.com/2015/03/including-the-chromedriver-location-in-macos-system-path/). The same process applied for GeckoDriver too.

3. In order for the email functionality to work properly, we have to authenticate our email account. However, when the application is tested, Google will think someone else is trying to access your account, so first head to this [link](https://myaccount.google.com/security) and enable the 'Less Secure App Access'.
