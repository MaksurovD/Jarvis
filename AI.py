from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import words
import openai
from num2words import num2words
#Настраиваемые параметры
#Виды моделей формирования ответов 'davinci_003', "GPT3_5Turbo"

class AIAPI:
    def __init__(self,model='davinci_003'):
        # Формирование модели взаимодействия
        self.vectorizer = CountVectorizer()

        self.vectors = self.vectorizer.fit_transform(
            list(words.data_set.keys()))  # Обработка key данных для тренировки нейронной сети

        self.clf = LogisticRegression()
        self.clf.fit(self.vectors, list(words.data_set.values()))  # Тренировка модели LogisticRegression

        del words.data_set  # Освобождение памяти от датасета


        #Настройка Разговорной модели

        openai.api_key = words.APIKey
        self.model = model
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # Функция формирования ответа
    def response(self, data):
        text_vector = self.vectorizer.transform([data]).toarray()[0]  # Подготовка вектора из распознанной строки
        answer = self.clf.predict([text_vector])[0]  # Формирование Ответа, возвращает из ответов words самый большой по вероятности
        return answer

    def __respGPT3_5_Turbo(self,promt):
        self.messages.append({"role": "user", "content": promt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0.4,
            presence_penalty=0.0,
            messages=self.messages,
        )
        response = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": response})
        return response

    def __respDavinci_003(self,promt):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=promt,
            temperature=0.9,
            max_tokens=700,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
        )
        response = response["choices"][0]["text"]
        return response


    #виды моделей формирования ответов 'davinci_003', "GPT3_5Turbo"
    def responseGPT(self,promt):
        if self.model == "davinci_003":
            response = self.__respDavinci_003(promt)
        elif self.model == "GPT3_5Turbo":
            response = self.__respGPT3_5_Turbo(promt)

        words = []
        for word in response.translate({ord('-'): ' ', ord('('): ' ', ord(')'): ' ', ord(','): ' ', ord('+'): ' ', ord('°'): ' градусов'}).split():
            if word.isdigit():
                words.append(num2words(int(word), lang='ru'))
            else:
                words.append(word)

        result = " ".join(words)
        return result
