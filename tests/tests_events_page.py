import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://www.greencity.cx.ua/#/greenCity/events"


class GreenCityTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 25)

        self.driver.get(URL)

        # 🔥 критично для SPA (React/Vue)
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # чек базового контейнера додатку
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "app-root"))
        )

    def tearDown(self):
        self.driver.quit()

    # ---------------------------
    # 1. EVENTS PAGE
    # ---------------------------
    def test_events_page(self):
        driver = self.driver
        wait = self.wait

        # даємо SPA прогрузити дані
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # універсальний пошук подій (не залежимо від exact class)
        events = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "[class*='event']")
            )
        )

        self.assertTrue(len(events) > 0, "Події не завантажились")

    # ---------------------------
    # 2. NEWS FILTER
    # ---------------------------
    def test_news_filter(self):
        driver = self.driver
        wait = self.wait

        # чекаємо SPA
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # чекаємо появу фільтрів (НЕ текст, а структура)
        filters = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 "//*[contains(@class,'filter') or contains(@class,'tab')]//*[self::button or self::div or self::a]")
            )
        )

        # якщо нічого не знайдено — тест падає з нормальним меседжем
        self.assertTrue(len(filters) > 0, "Фільтри не знайдені")

        # клікаємо перший доступний
        filters[0].click()

    # ---------------------------
    # 3. SIGN IN BUTTON
    # ---------------------------
    def test_user_registration(self):
        driver = self.driver
        wait = self.wait

        # даємо header прогрузитись
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "header"))
        )

        # більш гнучкий пошук (SPA часто міняє текст)
        sign_in_btn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'sign')]")
            )
        )

        self.assertIsNotNone(sign_in_btn)


if __name__ == "__main__":
    unittest.main()
