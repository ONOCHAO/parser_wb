import requests

class Mystat:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.token = None

    def get_auth(self):
        """Авторизация и получение токена"""
        url = "https://mapi.itstep.org/v1/mystat/auth/login"
        headers = {"Accept": "application/json"}
        data = {"login": self.login, "password": self.password}

        response = requests.post(url, headers=headers, json=data)
        print(f"Статус-код: {response.status_code}")  

        if response.status_code == 200:
            try:
                json_data = response.text
                self.token = json_data
                return True
            except requests.exceptions.JSONDecodeError:
                print("Ошибка: сервер вернул не JSON-данные.")
                print("Ответ сервера:", response.text)  
                return None
        else:
            print("Ошибка входа.")
            return None
    
    def get_marks(self):
        """Получение оценок и нормализация данных"""
        if not self.token:
            success = self.get_auth()
            if not success:
                return None

        url = "https://mapi.itstep.org/v1/mystat/aqtobe/statistic/marks"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)
        print(f"Статус-код: {response.status_code}")  

        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Полученные данные (JSON): {data}")  

                if isinstance(data, list) and len(data) > 0:
                    marks = [{"Дата": entry.get("mark_date", "Нет даты"), "Оценка": entry.get("mark", "Нет оценки")} for entry in data]
                    return marks  
                elif isinstance(data, dict):
                    return {"Дата": data.get("mark_date", "Нет даты"), "Оценка": data.get("mark", "Нет оценки")}
                else:
                    return "Нет данных"

            except requests.exceptions.JSONDecodeError:
                print("Ошибка: сервер вернул не JSON-данные.")
                print("Ответ сервера:", response.text)  
                return None  

        print("Ошибка при получении оценок.")
        return None  

    def get_schedule(self, schedule_type="month", date_filter="2025-06-04"):
        """Получение расписания (неделя или месяц)"""
        if not self.token:
            success = self.get_auth()
            if not success:
                return None

        if schedule_type == "week":
            url = f"https://mapi.itstep.org/v1/mystat/aqtobe/schedule/get-month?type=week&date_filter={date_filter}"
        else:
            url = f"https://mapi.itstep.org/v1/mystat/aqtobe/schedule/get-month?type=month&date_filter={date_filter}"

        headers = {"Authorization": f"Bearer {self.token}"}
        
        print(f"Используемый URL: {url}")  

        try:
            response = requests.get(url, headers=headers)
            print(f"Статус-код: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"Полученные данные (JSON): {data}")

                if "data" in data and isinstance(data["data"], list):
                    for i in data["data"]:
                        print(f"{i['date']}, {i['teacher_name']}")  

                    return data 
                else:
                    return "Нет данных"
            else:
                print("Ошибка при получении расписания. Код:", response.status_code)
                return None

        except requests.exceptions.JSONDecodeError:
            print("Ошибка: сервер вернул не JSON-данные.")
            print("Ответ сервера:", response.text)
            return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети: {e}")
            return None

         


    def calculate_average(self):
        """Вычисление средней оценки"""
        marks = self.get_marks()
        if not marks:
            return "Нет оценок для расчета"

        try:
            total_marks = sum(int(entry["Оценка"]) for entry in marks if entry["Оценка"].isdigit())
            count = len(marks)
            average = total_marks / count  
            return f"Средняя оценка: {average:.2f}"  
        except (KeyError, ValueError):
            return "Ошибка: неверный формат данных"


