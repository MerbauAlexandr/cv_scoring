import requests
from bs4 import BeautifulSoup

# Функция для получения HTML-страницы по URL
def get_html(url: str):
    return requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )

# Данные для генерации резюме вручную
def get_candidate_info(url: str):
    # Возвращаем заранее сгенерированные данные резюме
    return """
# Иван Иванов

**Возраст:** Мужчина, 29 лет

**Местоположение:** Москва, Россия

**Должность:** Менеджер по продажам B2B

**Статус:** Активно ищу работу

## Опыт работы

**Июнь 2021 — настоящее время (2 года и 4 месяца)**

*ООО "ТехноТорг"*

**Менеджер по продажам B2B**

Осуществлял поиск клиентов в сегменте B2B для продажи IT-услуг и программного обеспечения. Обрабатывал входящие заявки, выявлял потребности клиентов и предлагал решения, соответствующие их задачам. Проводил успешные встречи и переговоры с клиентами, заключал долгосрочные контракты.

**Январь 2019 — Май 2021 (2 года и 5 месяцев)**

*ООО "СервиТорг"*

**Менеджер по работе с клиентами**

Управлял отношениями с ключевыми клиентами компании в сегменте B2B. Выявлял потребности клиентов, разрабатывал индивидуальные предложения и стратегические планы взаимодействия. Проводил переговоры на уровне топ-менеджмента, что привело к заключению крупных контрактов.

## Ключевые навыки

- Продажи B2B
- Выявление потребностей клиентов
- Ведение переговоров
- Работа с возражениями
- Проведение презентаций и семинаров (онлайн/оффлайн)
- Анализ рынка и конкурентов
- Владение CRM-системами
"""

# Функция для получения описания вакансии
def get_job_description(url: str):
    # Получаем HTML-страницу вакансии
    response = get_html(url)
    # Извлекаем необходимые данные из вакансии
    return extract_vacancy_data(response.text)

# Функция для извлечения данных из вакансии
def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # Извлечение заголовка вакансии
    title = soup.find("h1", {"data-qa": "vacancy-title"})
    title = title.text.strip() if title else "Не указано"

    # Извлечение зарплаты
    salary = soup.find("span", {"data-qa": "vacancy-salary-compensation-type-net"})
    salary = salary.text.strip() if salary else "Не указано"

    # Извлечение опыта работы
    experience = soup.find("span", {"data-qa": "vacancy-experience"})
    experience = experience.text.strip() if experience else "Не указано"

    # Извлечение типа занятости и режима работы
    employment_mode = soup.find("p", {"data-qa": "vacancy-view-employment-mode"})
    employment_mode = employment_mode.text.strip() if employment_mode else "Не указано"

    # Извлечение компании
    company = soup.find("a", {"data-qa": "vacancy-company-name"})
    company = company.text.strip() if company else "Не указано"

    # Извлечение местополож
