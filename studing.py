import streamlit as st
import time

st.title('st.progress')

with st.expander('About this app'):
     st.write('You can now display the progress of your calculations in a Streamlit app with the `st.progress` command.')

st.subheader("Пример: обработка списка задач")

# Список задач для выполнения
tasks = ['Загрузка данных', 'Обработка данных', 'Обучение модели', 'Оценка результатов', 'Сохранение отчета']
total_tasks = len(tasks)

# Создаем прогресс-бар и текстовый элемент для статуса
progress_text = "Операция запускается. Пожалуйста, подождите."
my_bar = st.progress(0, text=progress_text)

for i, task in enumerate(tasks):
    # Имитируем работу
    time.sleep(0.7)
    
    # Обновляем прогресс-бар и текст
    progress_text = f"Шаг {i+1}/{total_tasks}: {task}..."
    my_bar.progress((i + 1) / total_tasks, text=progress_text)

st.success("Все задачи успешно выполнены!")
st.balloons()