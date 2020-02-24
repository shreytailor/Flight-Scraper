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


def closeModal(delaySeconds):
    time.sleep(delaySeconds);

    closeButtons = driver.find_elements_by_xpath('//button[contains(@id, "dialog-close") and contains (@class, "Button-No-Standard-Style close ")]');

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



def loadMore(delaySeconds):
    print('Loading more results...');
    time.sleep(delaySeconds);

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



def sendEmail(emailTo):
    server = smtplib.SMTP('smtp.gmail.com', 587);
    server.ehlo();
    server.starttls();
    server.login(config.EMAIL_ADDRESS, config.PASSWORD);

    subject = 'Updated Ticket Prices';
    bodyMessage = 'The scrape for KAYAK has just been performed. Here are the updated ticket prices for {}-{}, from {} to {}\n\n\n\n\n'.format(origin, destination, startDate, endDate);

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

    message = 'Subject: {}\n\n{}'.format(subject, bodyMessage);
    server.sendmail(config.EMAIL_ADDRESS, emailTo, message);
    server.quit();
    print('The summary of the results is sent through email.');









import time;
import smtplib;
import config;
from selenium import webdriver;
from selenium.webdriver.firefox.options import Options;


print('---------------------------------------------------');
origin = input('Origin: ');
destination = input('Destination: ');
print('---------------------------------------------------');
print('Enter the dates in the following format, YYYY-MM-DD');
startDate = input('Leaving on: ');
endDate = input('Coming back on: ');
print('---------------------------------------------------');

headless = True;
if headless:
    options = Options();
    options.headless = True;
    driver = webdriver.Firefox(options = options);
else:
    driver = webdriver.Firefox();

cheapestSortURL = 'https://www.nz.kayak.com/flights/' + origin + '-' + destination + '/' + startDate + '-flexible/' + endDate +'-flexible?sort=price_a';
bestSortURL = 'https://www.nz.kayak.com/flights/' + origin + '-' + destination + '/' + startDate + '-flexible/' + endDate +'-flexible?sort=bestflight_a';
quickestSortURL = 'https://www.nz.kayak.com/flights/' + origin + '-' + destination + '/' + startDate + '-flexible/' + endDate +'-flexible?sort=duration_a';

driver.get(cheapestSortURL);
closeModal(5);
collectResults(cheapestFlightsArray);

driver.get(bestSortURL);
closeModal(5);
collectResults(bestFlightsArray);

driver.get(quickestSortURL);
closeModal(5);
collectResults(quickestFlightsArray);

sendEmail("shreym.tailor@gmail.com");
driver.quit();
