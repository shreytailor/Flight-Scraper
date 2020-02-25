# Initializing the arrays that will later store the sorted results from the scrape.
cheapestFlightsArray = [];
bestFlightsArray = [];
quickestFlightsArray = [];

# Creating a class, and properties within to store each new record of a flight from the website.
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



# The function below takes in a single argument, which is the delay time before the process of closing the modal actually begins. This delay is added to make sure the modal has actually fully loaded - because there would be an error otherwise.
def closeModal(delaySeconds):
    time.sleep(delaySeconds);

    # Finding all the close buttons that match the XPath provided - there were around ten buttons found each time.
    closeButtons = driver.find_elements_by_xpath('//button[contains(@id, "dialog-close") and contains (@class, "Button-No-Standard-Style close ")]');

    # The button which we wanted to click to close the modal was one of the last ones in the array, hence we have used the 'try and except' feature to get rid of the errors which may come up. If there is an error, continue to click the next button.
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



# The function below can be used to load more results into the page, if needed. Once again, the only argument is to add a delay into our process.
def loadMore(delaySeconds):
    time.sleep(delaySeconds);

    # When the process was being tested, there were a couple of layovers (a div and a 'Back to Top' button) which were coming in the way, when trying to press the 'Load More' button so they have to be removed through a JavaScript execution. If for some reason, they do not exist this time, any errors would be ignored due to the 'try and except' block.
    try:
        backToTop = driver.find_element_by_xpath('//div[contains(@id, "backToTop") and contains(@class, "backToTop visible")]');
        driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", backToTop);
        elementOne = driver.find_element_by_xpath('//div[contains(@id, "dialog-viewport") and contains(@class, "viewport")]');
        driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", elementOne);
    except:
        pass;

    # Finding the 'Load More' button on the webpage and clicking on it.
    loadButton = driver.find_element_by_class_name('resultsPaginator');
    loadButton.click();



# The function below does the action of collectin all the results, by creating Class instances for each result and storing the results in one of the arrays creating at the beginning. It does take in one argument which is for the name of the array which we are wanting to store the results in. This depends on what kind of sorting has been done.
def collectResults(selectedArray):
    # Firstly, we are finding all the cards for every flight and storing those results in the variable 'flights'.
    flights = driver.find_elements_by_class_name('resultInner');

    # Then we loop through all of those results on the page.
    for flight in flights:
        # Here, all the data extraction is done from the current flight card.
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

        # After collecting all the information about the flight, we are now making a new instance of the 'Flight' Class and storing all the information in that.
        currentFlightDetails = Flight(provider, price, goingDate, goingStartTime, goingEndTime, goingAirline, goingNoOfLayovers, totalGoingJourney, comingDate, comingStartTime, comingEndTime, comingAirline, comingNoOfLayovers, totalComingJourney);

        # Appending the Class instance to the array selected.
        selectedArray.append(currentFlightDetails);



# The function below does the job of sending a summary email to yourself. The only argument it accepts, is your email.
def sendEmail(emailTo):
    # Using the smtplib to set up everything before we can go ahead and make the email string.
    server = smtplib.SMTP('smtp.gmail.com', 587);
    server.ehlo();
    server.starttls();

    # The login credentials for the person who is sending the email, comes from the 'config.py' file.
    server.login(config.EMAIL_ADDRESS, config.PASSWORD);

    # Creating the string for the Subject and the Body text.
    subject = 'Updated Ticket Prices';
    bodyMessage = 'The scrape for KAYAK has just been performed. Here are the updated ticket prices for {}-{}, from {} to {}\n\n\n\n\n'.format(origin, destination, startDate, endDate);

    # Under this, we are pretty much going through the top five results in each of the three arrays and sending them a summary of it, by formatting the collected data in a certain way so that it is readable.
    bodyMessage += 'Results sorted by Price (low to high) -\n'
    bodyMessage += '_______________________________________\n\n';
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

    bodyMessage += 'Results sorted by Best first -\n'
    bodyMessage += '______________________________\n\n';
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

    bodyMessage += 'Results sorted by Journey Time (low to high) -\n'
    bodyMessage += '______________________________________________\n\n';
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

    # Finally, we are now sending the email.
    message = 'Subject: {}\n\n{}'.format(subject, bodyMessage);
    server.sendmail(config.EMAIL_ADDRESS, emailTo, message);
    server.quit();
    print('The summary of the results is sent through email.');









# Importing the required modules for our application to perform as expected.
import time;
import smtplib;
# The file below contains the email credentials.
import config;
# Selenium is the module used to automate the browser interactions, while using the GeckoDriver as a link between Firefox and Selenium.
from selenium import webdriver;
from selenium.webdriver.firefox.options import Options;


# Initially, we are asking the user for the information about their trip.
print('---------------------------------------------------');
origin = input('Origin: ');
destination = input('Destination: ');
print('---------------------------------------------------');
print('Enter the dates in the following format, YYYY-MM-DD');
startDate = input('Leaving on: ');
endDate = input('Coming back on: ');
print('---------------------------------------------------');

# Set the 'headless' to true, to hide the browser when it is running.
headless = False;
if headless:
    options = Options();
    options.headless = True;
    driver = webdriver.Firefox(options = options);
else:
    driver = webdriver.Firefox();

# Creating the three URLs for each kind of sort.
cheapestSortURL = 'https://www.nz.kayak.com/flights/' + origin + '-' + destination + '/' + startDate + '-flexible/' + endDate +'-flexible?sort=price_a';
bestSortURL = 'https://www.nz.kayak.com/flights/' + origin + '-' + destination + '/' + startDate + '-flexible/' + endDate +'-flexible?sort=bestflight_a';
quickestSortURL = 'https://www.nz.kayak.com/flights/' + origin + '-' + destination + '/' + startDate + '-flexible/' + endDate +'-flexible?sort=duration_a';

# Using the functions above for each kind of sort.
driver.get(cheapestSortURL);
closeModal(10);
collectResults(cheapestFlightsArray);

driver.get(bestSortURL);
closeModal(10);
collectResults(bestFlightsArray);

driver.get(quickestSortURL);
closeModal(10);
collectResults(quickestFlightsArray);

# After all the collection is done, send them a summary email to finish off.
sendEmail("email where you want to send the summary");

# Quit the browser after everything is finished.
driver.quit();
