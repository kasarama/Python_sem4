from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from datetime import date
import pandas as pd


base_url = "https://www.biltorvet.dk/"

fuel = ["Hybrid","El","Benzin", "Diesel"]


def connect():
    """opens page and clicks on the cookie button.
    Returns a webdriver"""
    profile = webdriver.FirefoxProfile()
    profile.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
    )

    # headless would be needed here if we did not have a GUI version of firefox
    options = Options()
    options.headless = True

    browser = webdriver.Firefox(options=options)

    browser.get(base_url)
    browser.implicitly_wait(3)

    try:
        cookie_button = browser.find_element_by_class_name("coi-banner__accept")
        try:
            cookie_button.click()
            sleep(3)
            return browser
        except Exception as ex:
            print(ex)
    except Exception as e:
        print("BUTTON EXCEPTION", e)
        raise e


try:
    browser = connect()
except TimeoutException as e:
    print("connection failed: ", e)


def select_make():
    # pase make to the input field
    browser.find_element_by_id("textSearch_input").send_keys("audi")
    browser.save_screenshot("../screenshots/select_make.png")
    print("Make set")
    sleep(3)


def select_price():

    price_p = browser.find_element_by_xpath("//p[contains(text(), 'Pris')]")
    price_div = price_p.find_element_by_xpath("../.")

    price_div.click()
    print("Price menu clicked")
    sleep(3)

    kontant_span = browser.find_element_by_xpath('//span[contains(text(), "Kontant")]')
    div_span = kontant_span.find_element_by_xpath("../../../.")
    div_span.click()
    browser.save_screenshot("../screenshots/select_price.png")

    price_div.click()
    print("Price set")


def select_fuel(fuel):
    fuel_p = browser.find_element_by_xpath("//p[contains(text(), 'Brændstof')]")
    fuel_button = fuel_p.find_element_by_xpath("../.")
    fuel_button.click()
    browser.save_screenshot("../screenshots/click_fuel_menu.png")

    fuel_span = browser.find_element_by_xpath(
        "//span[contains(text(), '" + fuel + "')]"
    )

    selected_fuel_div = fuel_span.find_element_by_xpath("../../../../.")
    selected_fuel_div.click()
    browser.save_screenshot("../screenshots/select_fuel.png")


def select_used():
    inner_div = browser.find_element_by_xpath("//div[contains(text(), 'Brugt')]")
    clickable_div = inner_div.find_element_by_xpath("../../.")
    clickable_div.click()
    browser.save_screenshot("../screenshots/click_brugt.png")


def load_all_results_on_one_page():

    try:
        no_results = browser.find_element_by_xpath(
            "//p[contains(text(), 'Ingen resultater blev fundet')]"
        )

        return
    except Exception as e:

        stop = 0
        count = 0
        while stop == 0:
            try:
                load_more = browser.find_element_by_class_name(
                    "search-results__button.button.button--highlight"
                )

                count += 1
                browser.find_element_by_tag_name("body").send_keys(Keys.END)

                print(count)
                load_more.click()
            except Exception as e:
                stop = 2
                print("Load  more exception: ", e)
                browser.save_screenshot("../data/load_more_exc.png")


def search():

    search = browser.find_element_by_class_name(
        "button.button--highlight.advanced-search__button"
    )
    search.click()
    print("search clicked")

    sleep(3)


def scrap_results(fuel):
    car_elements = browser.find_elements_by_class_name(
        "card-ad-results__result.card-ad-results__result--default-view"
    )

    print("in scrap_result")
    for element in list(car_elements):

        href = element.find_element_by_css_selector("a").get_attribute("href")
        # print("link: ", href)
        price = (
            element.find_element_by_css_selector(
                "p.card__price.card__text--lg.font-semibold"
            )
            .text.replace("kr.", "")
            .strip()
            .replace(".", "")
        )
        # print('price ',price)

        # model= element.find_element_by_css_selector ("div.card__text.card__text--sm.card__text--bounds.font-semibold").text
        # print("modl: ", model)
        # type=element.find_element_by_css_selector ("div.card__text.card__text--sm.card__text--bounds").text
        # print("type: ", type)
        model_type = element.find_elements_by_css_selector(
            "div.card__text.card__text--sm.card__text--bounds"
        )
        model = model_type[0].text
        type = model_type[1].text

        print(model, type)
        details = list(
            element.find_elements_by_css_selector(
                "div.card-details__text.card__text--sm"
            )
        )
        location = details[0].text
        # print("loc: ",location)
        km = details[1].text
        # print('km ',km)
        year = details[2].text.strip()[-1:-5:-1][-1:-5:-1]
        # print('yaer: ',year)

        car = {
            "model": model,
            "type": type,
            "price": price,
            "km": km,
            "location": location,
            "year": year,
            "link": href,
        }
        # print (car)
        df = pd.DataFrame([car])
        df.to_csv(
            path_or_buf="../data/torvet_" + fuel + ".csv",
            sep=";",
            mode="a",
            header=None,
            index=False,
        )


def scrap_by_fuel(fuel):

    browser = connect()
    print("connected")
    select_price()

    select_fuel(fuel)
    print("fule selected")
    select_make()
    print("make selected")
    select_used()
    print("brugt selected")
    search()
    print("searching")
    load_all_results_on_one_page()
    print("loaded all")
    scrap_results(fuel)
    browser.close()
    browser = None


def scrap_all_audis():
    for f in fuel:
        print("FUEL to scrap: ", f)
        scrap_by_fuel(f)
        print(f, " scrapped!")


#scrap_all_audis()

