import os
import openai
import streamlit as st
import toml
from parse_hh import get_candidate_info, get_job_description  # Импортируем нужные функции

# Загрузка ключей из файла secrets.toml
secrets = toml.load("Streamlit/secrets.toml")

OPENAI_API_KEY = secrets.get("OPENAI_API_KEY")
ORGANIZATION_ID = secrets.get("ORGANIZATION_ID")

# Инициализация клиента OpenAI
client = openai.Client(api_key=OPENAI_API_KEY, organization=ORGANIZATION_ID)

SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу
Потом представь результат в виде оценки от 1 до 10.
""".strip()


def request_gpt(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1000,
        temperature=0,
    )
    return response.choices[0].message.content


st.title("CV Scoring App")

# Поля для ввода ссылки на описание вакансии и резюме
job_description_url = st.text_area("Enter the job description URL")
cv_url = st.text_area("Enter the CV URL")

if st.button("Score CV"):
    with st.spinner("Scoring CV..."):
        # Получаем описание вакансии с помощью существующей функции
        job_description = get_job_description(job_description_url)

        # Получаем сгенерированные данные резюме из функции в файле parse_hh.py
        cv = get_candidate_info(cv_url)

        st.write("Job description:")
        st.write(job_description)
        st.write("CV:")
        st.write(cv)

        # Формируем запрос для GPT на основе вакансии и резюме
        user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}"
        response = request_gpt(SYSTEM_PROMPT, user_prompt)

    st.write(response)
