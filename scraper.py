# Initializing the variables which we will need for collecting the information. Also we are creating a Class, in which we can store information about each individual flights.
cheapestFlightsArray = [];
bestFlightsArray = [];
quickestFlightsArray = [];

class Flight:
    def __init__(self, provider, price, goingDate, goingStartTime, goingEndTime, goingAirline, goingNoOfLayovers, totalGoingJourney, comingDate, comingStartTime, comingEndTime, comingAirline, comingNoOfLayovers, totalComingJourney):
        self.provider = provider;
        self.price = price;
        self.goingDate = goingDate;
        self.goingStartTime = goingStartTime;
        self.goingEndTime = goingEndTime;
        self.goingAirline = goingAirline;
        self.goingNoOfLayovers = goingNoOfLayovers;
        self.totalGoingJourney = totalGoingJourney;
        self.comingDate = comingDate;
        self.comingStartTime = comingStartTime;
        self.comingEndTime = comingEndTime;
        self.comingAirline = comingAirline;
        self.comingNoOfLayovers = comingNoOfLayovers;
        self.totalComingJourney = totalComingJourney;



# The function below closes the modal which pops-up after the redirection of the website within the browser.
def closeModal(delaySeconds):
    print('Waiting for the modal to load properly...');
    time.sleep(delaySeconds);

    # Getting a list of the close buttons that meet the XPath requirements.
    closeButtons = driver.find_elements_by_xpath('//button[contains(@id, "dialog-close") and contains (@class, "Button-No-Standard-Style close ")]');

    # Going through a few of the last buttons and clicking them to ensure that the modal is closed. If there is an error, it is ignored and we move onto the next button. This is done because we don't know the order of the buttons as they keep changing so we trying clicking on the last few within the list.
    try:
        closeButtons[7].click();
    except:
        pass;

    try:
        closeButtons[8].click();
    except:
        pass;

    try:
        closeButtons[9].click();
    except:
        pass;

    try:
        closeButtons[10].click();
    except:
        pass;

    print('The modal is closed!');
    print('---------------------------------------------------');



# The function below loads more results on our page.
def loadMore(delaySeconds):
    print('Loading more results...');
    time.sleep(delaySeconds);

    # We are removing the "Back To Top" div here which shows up due to scrolling down. The 'try and except' is used here because on the first attempt, the div may not be there so in this case, the error is ignored.
    try:
        backToTop = driver.find_element_by_xpath('//div[contains(@id, "backToTop") and contains(@class, "backToTop visible")]');
        driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", backToTop);
        elementOne = driver.find_element_by_xpath('//div[contains(@id, "dialog-viewport") and contains(@class, "viewport")]');
        driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", elementOne);
    except:
        pass;

    # Finding the 'Load More' button on the webpage.
    loadButton = driver.find_element_by_class_name('resultsPaginator');
    loadButton.click();

    print('New results loaded!')
    print('---------------------------------------------------');



# The function below actually does the scraping from the website, by finding the different elements on the browser. We go through each card for different flights and then append that to main array by creating class instances for each flight option for the user.
def collectResults(selectedArray):
    flights = driver.find_elements_by_class_name('resultInner');
    for flight in flights:
        leftContainer = flight.find_element_by_class_name('mainInfo');
        rightContainer = flight.find_element_by_class_name('booking');
        goingData = leftContainer.find_elements_by_class_name('flight')[0];
        goingTimesSection = goingData.find_element_by_class_name('times');
        comingData = leftContainer.find_elements_by_class_name('flight')[1];
        comingTimesSection = comingData.find_element_by_class_name('times');

        provider = rightContainer.find_element_by_class_name('providerName').text;
        price = rightContainer.find_element_by_class_name('price-text').text;

        goingDate = goingData.find_element_by_class_name('date').find_element_by_class_name('top').text;
        goingStartTime = goingTimesSection.find_element_by_class_name('depart-time').text;
        goingEndTime = goingTimesSection.find_element_by_class_name('arrival-time').text;
        goingAirline = goingTimesSection.find_element_by_class_name('bottom').text;
        goingNoOfLayovers = goingData.find_element_by_class_name('stops').find_element_by_class_name('top').text;
        totalGoingJourney = goingData.find_element_by_class_name('duration').find_element_by_class_name('top').text;

        comingDate = comingData.find_element_by_class_name('date').find_element_by_class_name('top').text;
        comingStartTime = comingTimesSection.find_element_by_class_name('depart-time').text;
        comingEndTime = comingTimesSection.find_element_by_class_name('arrival-time').text;
        comingAirline = comingTimesSection.find_element_by_class_name('bottom').text;
        comingNoOfLayovers = comingData.find_element_by_class_name('stops').find_element_by_class_name('top').text;
        totalComingJourney = comingData.find_element_by_class_name('duration').find_element_by_class_name('top').text;

        currentFlightDetails = Flight(provider, price, goingDate, goingStartTime, goingEndTime, goingAirline, goingNoOfLayovers, totalGoingJourney, comingDate, comingStartTime, comingEndTime, comingAirline, comingNoOfLayovers, totalComingJourney);

        selectedArray.append(currentFlightDetails);



# The function below goes through the three arrays which were created initially for storing all the results, and takes the top five results from each and then puts the content of that in the email so that the user gets a summary.
def sendEmail(emailTo):
    # Over here, we are setting up the login for the host account so that we can send emails.
    server = smtplib.SMTP('smtp.gmail.com', 587);
    server.ehlo();
    server.starttls();
    server.login(config.EMAIL_ADDRESS, config.PASSWORD);

    # The two important strings are created.
    subject = 'Updated Ticket Prices';
    bodyMessage = 'The scrape for KAYAK has just been performed and here are the updated ticket prices.\n\n\n\n\n';

    # Going through the data in the three arrays using FOR loops (through the first five results).
    bodyMessage += 'Here are the results sorted by Price (low to high) -'
    bodyMessage += '____________________________________________________________________________________\n\n';
    for counter in range(5):
        object = cheapestFlightsArray[counter];
        provider = object.provider;
        price = object.price;
        goingDate = object.goingDate;
        goingStartTime = object.goingStartTime;
        goingEndTime = object.goingEndTime;
        goingAirline = object.goingAirline;
        goingNoOfLayovers = object.goingNoOfLayovers;
        totalGoingJourney = object.totalGoingJourney;
        comingDate = object.comingDate;
        comingStartTime = object.comingStartTime;
        comingEndTime = object.comingEndTime;
        comingAirline = object.comingAirline;
        comingNoOfLayovers = object.comingNoOfLayovers;
        totalComingJourney = object.totalComingJourney;

        bodyMessage += '{}, {}\n'.format(provider, price);
        bodyMessage += '-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n';
        bodyMessage += '{} ~ {} - {}\n'.format(goingDate, goingStartTime, goingEndTime);
        bodyMessage += '{}, the total journey time is {}\n'.format(goingNoOfLayovers, totalGoingJourney);
        bodyMessage += '(The service is provided by {})\n'.format(goingAirline);
        bodyMessage += '-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n';
        bodyMessage += '{} ~ {} - {}\n'.format(comingDate, comingStartTime, comingEndTime);
        bodyMessage += '{}, the total journey time is {}\n'.format(comingNoOfLayovers, totalComingJourney);
        bodyMessage += '(The service is provided by {})\n\n\n'.format(comingAirline);
    bodyMessage += '\n\n\n';

    bodyMessage += 'Here are the results sorted by Best first -'
    bodyMessage += '____________________________________________________________________________________\n\n';
    for counter in range(5):
        object = bestFlightsArray[counter];
        provider = object.provider;
        price = object.price;
        goingDate = object.goingDate;
        goingStartTime = object.goingStartTime;
        goingEndTime = object.goingEndTime;
        goingAirline = object.goingAirline;
        goingNoOfLayovers = object.goingNoOfLayovers;
        totalGoingJourney = object.totalGoingJourney;
        comingDate = object.comingDate;
        comingStartTime = object.comingStartTime;
        comingEndTime = object.comingEndTime;
        comingAirline = object.comingAirline;
        comingNoOfLayovers = object.comingNoOfLayovers;
        totalComingJourney = object.totalComingJourney;

        bodyMessage += '{}, {}\n'.format(provider, price);
        bodyMessage += '-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n';
        bodyMessage += '{} ~ {} - {}\n'.format(goingDate, goingStartTime, goingEndTime);
        bodyMessage += '{}, the total journey time is {}\n'.format(goingNoOfLayovers, totalGoingJourney);
        bodyMessage += '(The service is provided by {})\n'.format(goingAirline);
        bodyMessage += '-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n';
        bodyMessage += '{} ~ {} - {}\n'.format(comingDate, comingStartTime, comingEndTime);
        bodyMessage += '{}, the total journey time is {}\n'.format(comingNoOfLayovers, totalComingJourney);
        bodyMessage += '(The service is provided by {})\n\n\n'.format(comingAirline);
    bodyMessage += '\n\n\n';

    bodyMessage += 'Here are the results sorted by Journey Time (low to high) -'
    bodyMessage += '____________________________________________________________________________________\n\n';
    for counter in range(5):
        object = quickestFlightsArray[counter];
        provider = object.provider;
        price = object.price;
        goingDate = object.goingDate;
        goingStartTime = object.goingStartTime;
        goingEndTime = object.goingEndTime;
        goingAirline = object.goingAirline;
        goingNoOfLayovers = object.goingNoOfLayovers;
        totalGoingJourney = object.totalGoingJourney;
        comingDate = object.comingDate;
        comingStartTime = object.comingStartTime;
        comingEndTime = object.comingEndTime;
        comingAirline = object.comingAirline;
        comingNoOfLayovers = object.comingNoOfLayovers;
        totalComingJourney = object.totalComingJourney;

        bodyMessage += '{}, {}\n'.format(provider, price);
        bodyMessage += '-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n';
        bodyMessage += '{} ~ {} - {}\n'.format(goingDate, goingStartTime, goingEndTime);
        bodyMessage += '{}, the total journey time is {}\n'.format(goingNoOfLayovers, totalGoingJourney);
        bodyMessage += '(The service is provided by {})\n'.format(goingAirline);
        bodyMessage += '-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n';
        bodyMessage += '{} ~ {} - {}\n'.format(comingDate, comingStartTime, comingEndTime);
        bodyMessage += '{}, the total journey time is {}\n'.format(comingNoOfLayovers, totalComingJourney);
        bodyMessage += '(The service is provided by {})\n\n\n'.format(comingAirline);
    bodyMessage += '\n\n\n';

    message = 'Subject: {}\n\n{}'.format(subject, bodyMessage);
    server.sendmail(config.EMAIL_ADDRESS, emailTo, message);
    server.quit();









# The 'selenium.webdriver' is a module which brings real user interactions with a simulated browser. It is an interface which takes in a set of instructions, and we are able to run those on many different browsers.
from selenium import webdriver;
# This default Python module is required to add some delay between the commands.
import time;
# The module below is needed to send an email from Python, and we must also import the 'config' file to import the login credentials for your email account.
import smtplib;
import config;

# Asking the end-user for the travel information.
print('---------------------------------------------------');
origin = input('Origin: ');
destination = input('Destination: ');
print('---------------------------------------------------');
print('Enter the dates in the following format, YYYY-MM-DD');
startDate = input('Leaving on: ');
endDate = input('Coming back on: ');
print('---------------------------------------------------');

# The 'GeckoDriver' which is developed by Mozilla has been placed within '/usr/local/bin' and is added to the PATHS so that it can be accessed from here. It is a linkage between the Selenium module and Firefox.
driver = webdriver.Firefox();

# We are constructing the Kayak links, from the input of the user from above.
cheapestSortURL = 'https://www.nz.kayak.com/flights/' + origin + '-' + destination + '/' + startDate + '-flexible/' + endDate +'-flexible?sort=price_a';
bestSortURL = 'https://www.nz.kayak.com/flights/' + origin + '-' + destination + '/' + startDate + '-flexible/' + endDate +'-flexible?sort=bestflight_a';
quickestSortURL = 'https://www.nz.kayak.com/flights/' + origin + '-' + destination + '/' + startDate + '-flexible/' + endDate +'-flexible?sort=duration_a';

# Redirecting the browser to the link created above. We are scraping the results off the website for all the types of sorts.
driver.get(cheapestSortURL);
closeModal(5);
loadMore(3);
collectResults(cheapestFlightsArray);

driver.get(bestSortURL);
closeModal(5);
loadMore(3);
collectResults(bestFlightsArray);

driver.get(quickestSortURL);
closeModal(5);
loadMore(3);
collectResults(quickestFlightsArray);

sendEmail('shreym.tailor@gmail.com');
driver.quit();
