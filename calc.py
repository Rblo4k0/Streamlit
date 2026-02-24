import streamlit as st

st.set_page_config(layout="centered", page_title="Калькулятор")

st.title("Интерактивный калькулятор")

# --- Инициализация состояния ---
# st.session_state используется для хранения переменных между перезапусками скрипта
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'first_operand' not in st.session_state:
    st.session_state.first_operand = None
if 'operator' not in st.session_state:
    st.session_state.operator = None
if 'waiting_for_second_operand' not in st.session_state:
    st.session_state.waiting_for_second_operand = False

# --- Функции для логики калькулятора ---
def handle_digit(digit):
    """Обработка нажатия цифровой кнопки."""
    if st.session_state.waiting_for_second_operand:
        st.session_state.display = digit
        st.session_state.waiting_for_second_operand = False
    else:
        # Предотвращаем ввод нескольких нулей в начале
        st.session_state.display = st.session_state.display + digit if st.session_state.display != '0' else digit
    st.rerun()

def handle_operator(op):
    """Обработка нажатия кнопки операции."""
    # Если это второй оператор подряд (например, 5 + +), просто заменяем его
    if st.session_state.waiting_for_second_operand:
        # Это также позволяет продолжить вычисление после нажатия "="
        st.session_state.operator = op
        st.rerun()

    # Если есть первое число и оператор, вычисляем промежуточный результат (для цепочек типа 5+5+5)
    if st.session_state.first_operand is not None and st.session_state.operator is not None:
        result = calculate()
        st.session_state.display = result

    st.session_state.first_operand = float(st.session_state.display)
    st.session_state.operator = op
    st.session_state.waiting_for_second_operand = True
    st.rerun()

def calculate():
    """Выполнение вычисления."""
    second_operand = float(st.session_state.display)
    first_operand = st.session_state.first_operand
    op = st.session_state.operator

    if op == '+':
        result = first_operand + second_operand
    elif op == '-':
        result = first_operand - second_operand
    elif op == '×':
        result = first_operand * second_operand
    elif op == '÷':
        if second_operand == 0:
            return "Ошибка"
        result = first_operand / second_operand
    else:
        return st.session_state.display # Если оператора нет, ничего не делаем
    
    # Округляем для красивого вывода, если результат - целое число
    if result == int(result):
        return str(int(result))
    return f"{result:.9f}".rstrip('0').rstrip('.')

def clear_all():
    """Полный сброс калькулятора."""
    st.session_state.display = '0'
    st.session_state.first_operand = None
    st.session_state.operator = None
    st.session_state.waiting_for_second_operand = False
    st.rerun()

# --- Пользовательский интерфейс ---

# Дисплей калькулятора
st.text_input("Результат", st.session_state.display, disabled=True)

# Сетка кнопок
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("", use_container_width=True, key="7", shortcut="7"): handle_digit('7')
    if st.button("", use_container_width=True, key="4", shortcut="4"): handle_digit('4')
    if st.button("", use_container_width=True, key="1", shortcut="1"): handle_digit('1')
    if st.button("C", use_container_width=True, key="C", shortcut="backspace"): clear_all()


with col2:
    if st.button("", use_container_width=True, key="8", shortcut="8"): handle_digit('8')
    if st.button("", use_container_width=True, key="5", shortcut="5"): handle_digit('5')
    if st.button("", use_container_width=True, key="2", shortcut="2"): handle_digit('2')
    if st.button("", use_container_width=True, key="0", shortcut="0"): handle_digit('0')

with col3:
    if st.button("", use_container_width=True, key="9", shortcut="9"): handle_digit('9')
    if st.button("", use_container_width=True, key="6", shortcut="6"): handle_digit('6')
    if st.button("", use_container_width=True, key="3", shortcut="3"): handle_digit('3')
    if st.button(".", use_container_width=True, key="."):
        if '.' not in st.session_state.display:
            st.session_state.display += '.'
            st.rerun()

with col4:
    if st.button("÷", use_container_width=True, key="/"): handle_operator('÷')
    if st.button("×", use_container_width=True, key="*"): handle_operator('×')
    if st.button("\-", use_container_width=True, key="-"): handle_operator('-')
    if st.button("\+", use_container_width=True, key="+"): handle_operator('+')

if st.button("=", use_container_width=True, key="=", shortcut="enter"):
    if st.session_state.operator and st.session_state.first_operand is not None:
        result = calculate()
        st.session_state.display = result
        # Устанавливаем состояние так, чтобы можно было начать новую операцию с этим результатом
        st.session_state.first_operand = float(result) if result != "Ошибка" else None
        st.session_state.operator = None # Оператор сбрасывается, ждем новый
        st.session_state.waiting_for_second_operand = True # Готовы начать новый ввод
        st.rerun()