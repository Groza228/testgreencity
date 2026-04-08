import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GreenCityTests(unittest.TestCase):

    def setUp(self):
        # Ініціалізація браузера
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        # Ініціалізація явного очікування
        self.wait = WebDriverWait(self.driver, 10)

        # Відкриття сторінки подій GreenCity
        self.driver.get("https://www.greencity.cx.ua/#/greenCity/events")

    def tearDown(self):
        # Закриття браузера після виконання тесту
        self.driver.quit()

    def test_user_registration(self):
        driver = self.driver
        wait = self.wait

        # Крок 1: Натискання кнопки "Sign in"
        sign_in_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Sign in')]"))
        )
        sign_in_btn.click()

        # Крок 2: Перехід до форми реєстрації "Sign up"
        sign_up_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Sign up')]"))
        )
        sign_up_tab.click()

        # Крок 3: Введення email
        email = wait.until(EC.visibility_of_element_located((By.NAME, "email")))

        # Крок 4: Введення інших полів форми
        username = driver.find_element(By.NAME, "name")
        password = driver.find_element(By.NAME, "password")
        confirm_password = driver.find_element(By.NAME, "confirmPassword")

        email.send_keys("testuser123@gmail.com")
        username.send_keys("testuser123")
        password.send_keys("Test12345!")
        confirm_password.send_keys("Test12345!")

        # Крок 5: Відправка форми реєстрації
        submit = driver.find_element(By.XPATH, "//button[contains(text(),'Sign up')]")
        submit.click()

        # Крок 6: Перевірка, що користувач перенаправлений після реєстрації
        self.assertIn("greencity", driver.current_url)

    def test_events_page(self):
        driver = self.driver
        wait = self.wait

        # Крок 1: Перевірка наявності списку подій
        events = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "event-card"))
        )
        self.assertTrue(len(events) > 0)

        # Крок 2: Відкриття першої події
        events[0].click()

        # Крок 3: Перевірка відображення деталей події
        details = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "event-title"))
        )
        self.assertTrue(details.is_displayed())

    def test_news_filter(self):
        driver = self.driver
        wait = self.wait

        # Крок 1: Перехід у розділ "Еко новини"
        news_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Еко новини')]"))
        )
        news_tab.click()

        # Крок 2: Застосування фільтрів
        filters = ["Новини", "Події", "Освіта", "Ініціативи", "Реклама"]

        for filter_name in filters:
            filter_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(),'{filter_name}')]"))
            )
            filter_btn.click()

        # Крок 3: Перевірка, що новини відображаються
        items = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "news-card"))
        )
        self.assertTrue(len(items) > 0)

        # Крок 4: Очищення фільтрів
        clear_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Очистити')]"))
        )
        clear_btn.click()

        # Крок 5: Перевірка, що список новин відновився
        items_after = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "news-card"))
        )
        self.assertTrue(len(items_after) > 0)


if __name__ == "__main__":
    unittest.main()
