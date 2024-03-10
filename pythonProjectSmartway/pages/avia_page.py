import sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pythonProjectSmartway.pages.date import date_flight
from pythonProjectSmartway.pages.locators import Locators
from selenium.webdriver.common.action_chains import ActionChains


class SmartwayLoginPage:
    def __init__(self, driver):
        self.driver = driver

    def open_smartway_url(self):
        self.driver.get("https://wp.rc.gospodaprogrammisty.ru")
        self.driver.maximize_window()

    def log_in(self, username, password):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(Locators.EMAIL)
        )
        email_link = self.driver.find_element(*Locators.EMAIL)
        email_link.send_keys(username)
        password_link = self.driver.find_element(*Locators.PASSWORD)
        password_link.send_keys(password)
        button_link = self.driver.find_element(*Locators.BUTTON_LINK)
        button_link.click()

    def check_balance(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.BALANCE)
            )
            balance = self.driver.find_element(*Locators.BALANCE)
            start_balance = float(balance.text.split(" ")[1].replace(" ", "").replace(",", "."))
            if start_balance > 0:
                print("Баланс положительный")
            else:
                print("Баланс равен 0")
                raise ValueError("Завершение теста. Необходимо пополнить баланс")

        except TimeoutException:
            print("Поля логин/пароль не загружены")


class Search_Avia:
    def __init__(self, driver):
        self.driver = driver

    def money(self):
        first_balance = self.driver.find_element(*Locators.BALANCE)
        return first_balance

    def search_flight(self, departure_city, arrival_city):
        avia_buttone = self.driver.find_element(*Locators.AVIA_BUTTON)
        avia_buttone.click()
        departure_city_elem = self.driver.find_element(*Locators.DEPARTURE_CITY)
        departure_city_elem.send_keys(departure_city)
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(Locators.CITY_FROM_FIRST_EL)
        )
        autocomplit_departure = self.driver.find_element(*Locators.CITY_FROM_FIRST_EL)
        autocomplit_departure.click()
        arrival_city_elem = self.driver.find_element(*Locators.ARRIVAL_CITY)
        arrival_city_elem.send_keys(arrival_city)
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(Locators.CITY_TO_FIRST_EL)
        )
        autocomplit_arrival = self.driver.find_element(*Locators.CITY_TO_FIRST_EL)
        autocomplit_arrival.click()

        input_date = self.driver.find_element(*Locators.INPUT_DATE)
        print("Дата вылета: ")
        input_date.send_keys(str(date_flight(12)))
        time.sleep(0.5)

        search_buttone = self.driver.find_element(*Locators.SEARCH_BUTTON)
        search_buttone.click()

        try:
            WebDriverWait(self.driver, 60).until(
                EC.visibility_of_element_located(Locators.REFUND_FILTER)
            )
            print("Выдача АБ успешно загружена")
        except TimeoutException:
            print("Выдача АБ не загружена за 60 секунд")


class Filter:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_refund_filter(self):
        time.sleep(1)
        try:
            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(Locators.REFUND_FILTER)
            )
        except TimeoutException:
            print("Нет фильтра 'Возвратный билет'")
            raise NoSuchElementException("Завершение теста")

    def click_refund_filter(self):
        refund = self.driver.find_element(*Locators.REFUND_FILTER)
        refund.click()

    def click_add_to_cart(self):
        add_to_cart = self.driver.find_element(*Locators.ADD_TO_CART_BUTTON)
        add_to_cart.click()

    def wait_for_notification_added(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(Locators.NOTIFICATION_AB_ADDED)
            )
            print("АБ добавлен в корзину")
        except TimeoutException:
            print("Оповещение о добавлении АБ в корзину не появилось")

    def click_notification_added(self):
        card_notification = self.driver.find_element(*Locators.NOTIFICATION_AB_ADDED)
        card_notification.click()

    def wait_for_cart_loaded(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(Locators.SELECT_EMPLOYEE)
            )
            print("Корзина с АБ успешно загружена")
        except TimeoutException:
            print("Корзина не открылась")


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def select_employee(self, employee_name):
        select_employee = self.driver.find_element(*Locators.SELECT_EMPLOYEE)
        select_employee.click()
        input_employee = self.driver.find_element(*Locators.INPUT_EMPLOYEE)
        input_employee.send_keys(employee_name)
        try:
            WebDriverWait(self.driver, 7).until(
                EC.visibility_of_element_located(Locators.SELECT_NAME)
            )
            print("Сотрудник найден в списке")
        except TimeoutException:
            print("Сотрудник не найден")
        select_name = self.driver.find_element(*Locators.SELECT_NAME)
        select_name.click()

    def check_fields_filled(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(Locators.PRICE_BUTTON)
            )
            print("Обязательные поля в АБ заполнены")
        except TimeoutException:
            print("Обязательные поля в АБ не заполнены")
        return True

    def proceed_to_payment(self):
        price_button = self.driver.find_element(*Locators.PRICE_BUTTON)
        price_button.click()

    def is_duplicate_in_cart(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(Locators.DUPLICATE_CARD)
            )
            print("Дубль АБ есть в корзине или в поездках")
        except TimeoutException:
            pass

    def close_duplicate_agreement(self):
        try:
            agreement = self.driver.find_element(*Locators.DUPLICATE_BUTTON_CLOSE)
            agreement.click()
        except NoSuchElementException:
            pass

    def finish_accept_rules(self):
        try:
            finish_accept = self.driver.find_element(*Locators.ACCEPT_RULES)
            finish_accept.click()
        except NoSuchElementException:
            print("Не хватает денег для покупки")
            raise ValueError("Завершение теста. Необходимо пополнить баланс")

    def is_agreement_double_correct(self):
        try:
            agreement_double = self.driver.find_element(*Locators.AGREEMENT)
            agreement_double.click()
        except NoSuchElementException:
            pass

    def click_buy_button(self):
        time.sleep(0.5)
        buy = self.driver.find_element(*Locators.FINISH_BUY)
        buy.click()

    def verify_payment_success(self):
        try:
            WebDriverWait(self.driver, 300).until(
                EC.visibility_of_element_located(Locators.PAY_DETAILS)
            )
            print("Процесс оплаты завершен")
        except TimeoutException:
            print("Ошибка бронирования")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.PAY_DETAILS)
            )
            print("Поездка создана")
        except TimeoutException:
            print("Поездка не создана")
        trip_detail = self.driver.find_element(*Locators.TRIP_DETAILS)
        trip_detail.click()


class RefundPage:
    def __init__(self, driver):
        self.driver = driver

    def open_trip(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(Locators.OPEN_TRIP)
            )
            print("Открылась поездка")
        except TimeoutException:
            print("Упали МД")
            raise ValueError("Завершение теста")
        refund_option = self.driver.find_element(*Locators.OPEN_TRIP)
        action = ActionChains(self.driver)
        action.move_to_element(refund_option).perform()

    def calculate_refund(self):
        try:
            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(Locators.CALCULATE_REFUND)
            )
            print("Рассчет возврата")
        except TimeoutException:
            print("Ошибка возврата АБ")
            self.driver.refresh()
        refund = self.driver.find_element(*Locators.CALCULATE_REFUND)
        refund.click()

    def wait_for_approval_element(self):
        try:
            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(Locators.APPROVAL)
            )
        except TimeoutException:
            print("Возврат невозможен")
            raise ValueError("Ошибка возврата")

    def click_approval(self):
        approval = self.driver.find_element(*Locators.APPROVAL)
        approval.click()

    def refund_ticket(self):
        refund_ticket = self.driver.find_element(*Locators.REFUND_TICKET)
        refund_ticket.click()

    def confirm_refund(self):
        confirmation = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(Locators.CONFIRM_REFUND)
        )
        confirmation.click()

    def wait_for_process_complete(self):
        try:
            WebDriverWait(self.driver, 20).until_not(EC.presence_of_element_located(Locators.WAIT_PROCESS_COMPLETE))
            print("Процесс возврата завершен")
        except TimeoutException:
            print("Процесс возврата не завершился за 20 секунд")

    def check_status(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Locators.CHECK_STATUS)
            )
            print('Проверка статуса АБ')
        except TimeoutException:
            print("Произошла ошибка при возврате")

        stat = self.driver.find_element(*Locators.CHECK_STATUS)
        text_status = stat.text
        time.sleep(2)
        if 'Отменена' in text_status:
            print("АБ успешно отменен")
        else:
            print("Ошибка отмены")


class Check:
    def __init__(self, driver, search_avia_object):
        self.driver = driver
        self.search_avia_object = search_avia_object

    def check_delta_balance(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Locators.BALANCE)
            )
            print('Проверка баланса')
        except TimeoutException:
            print("Произошла ошибка при проверке баланса")

        first_balance = self.search_avia_object.money()

        balance = self.driver.find_element(*Locators.BALANCE)
        end_balance_text = balance.text

        if first_balance.text == end_balance_text:
            print("Деньги возвращены в полном объеме")
            sys.exit()
        elif first_balance.text > end_balance_text:
            print("Был совершен возврат со штрафом")
            sys.exit()
        else:
            print("Произошла неисследованная ошибка")
            sys.exit()

