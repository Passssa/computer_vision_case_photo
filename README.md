## Тестовое задание от Т-банка по компьютерному зрению для проектной смены в Университете Сириус

### Описание

Мной была выполнена задача по редактированию карточек товаров с маркетплейсов, которая включает в себя: сегментацию товара, удаление и замену фона на изображении. 

К коду написана документация в виде docstring с google-style. Также в коде есть поясняющие комментарии.


Дополнительно в рамках **Задания 1** был проведен research подходов для сегментации и удаления фона на изображении. Jupyter-notebook с ним я оставила в файле **research_segmentation.ipynb**.

Дополнительно в рамках **Задания 2** была реализована возможность выбора нового фона для карточки товара. Фон можно заменить на любое другое изображение, а также на другой цвет. По умолчанию (если не передавать в функцию цветов или фоновых изображений) фон будет просто удален. То есть сохранится новое изображения с "прозрачным" фоном.


### Research по выбору алгоритма сегментации
Были рассмотрены подходы:
- openCV с применением морфологии.
- метод SelfiSegmentation.removeBG из CVZone. Также нашла оптимальное значение гиперпараметра cutThreshold - порога сегментации. Оптимальным оказался 0.5.
- метод rembg.remove. В рамках этого метода пробовали рассмотреть предобученные модели разных архитектур НС: U2-Net, RCNN, DeepFillv2. Метрики оказались особо не отличающимися. За оптимальную взяли архитектуру U2-Net.


Дополнительно я взяла датасет с сегментированными изображениями из открытого источника. Так я смогу посчитать метрики качества сегментации для подходов.
Данные, которые были предоставлены к заданию изначально, я использовала как тестовые, но не применяла к ним оценку метрик. Я просто зрительно оценила качество удаления фона.

### Метрики для оценки качества сегментации:
- Основная метрика - IoU. Отражает долю перекрытия между целевой маской и нашим прогнозируемым результатом.

- Доп. метрика - Pixel Accuracy. Идейно она является аналогом известной метрики Accuracy в классических задачах классификации. В нашем случае она покажет процент пикселей на изображении, которые были правильно определены. То есть правильно ли модель сделала, что удалила/оставила соответствующую часть фона на изображении.

В результате рассмотрения подходов, получили следущие результаты:

|Подход|Значение метрики IoU|Значение метрики Pixel Accuracy|Сегментация изначальных данных из задания|Папка с сегментацией изначальных данных из задания|
|------|--------------------|-------------------------------|-----------------------------|-----------------------------|
|opencv| 0.317 | 0.571 | Алгоритм очень плохо понимает, где границы объекта. Сегментирование почти случайное |-|
|SelfiSegmentation| 0.894 | 0.763 | Выявила следующие проблемные кейсы: <br> - Если и товар, и фон достаточно светлые/белые, очень плохо его распознает.<br>- Когда товар - книга, то он распознает именно рисунок на книге. <br> Однако из плюсов данного метода можно отметить: <br> - Если товар надет на человека, то сегментирует достаточно хорошо. Не обрезаются важные части. | data/sirius_selfiseg |
|rembg.remove| 0.898 | 0.519 | Качественно сегментирует. Но оставляет очень тонкий миллиметровый контур рядом с границами объекта | с фоном-картинкой - data/sirius_rembg_with_img, с фоном-заливкой цветом - data/sirius_rembg_with_color|

### Запуск скрипта:
1. Установите завистимости из requirements: **pip install -r requirements.txt**
2. Запустите скрипт replace_background_for_ecommerce.py. 
При желании устрановить свой цвет фона или изображение, на которое будет заменен фон. Сделать это можно 2-мя способами:

2.1 При запуске кода указать через enter значения переменных background_color, background_img, input_img (цвета фона в формате tuple(r, g, b), путь до файла с изобрадением для фона и путь до карточки товара):

--------

<b><i>python goods_marketplace_repalce_bachground.py</i></b>

<b><i>(100, 200, 200)</i></b>

<b><i><просто enter, если не хочется подавать аргумент></i></b>

<b><i><путь до файла></i></b>

--------
Если ввести и путь до изображения, и цвет фона, приоритетным окажется фон из изображения.
Если для фона везде нажать enter, то установятся значения переменных по умолчанию (которые захардкожены в файле).


2.2 В "\_\_main\_\_" записать в переменные желаемые значения.


Результат будет сохранен в эту же директорию.


### Файлы в репозитории:
1. research_segmentation.ipynb - research с подходами для сегментации.
2. requirements.txt - необходимые зависимости для запуска скрипта.
3. README.md - описание к заданию.
4. goods_marketplace_repalce_bachground.py - скрипт для смены фона.
5. backgrounds_images - папка с изображениями для фона.
6. data/sirius_data - папка с изображениями, предложенными к заданию.
7. data/sirius_selfiseg - папка с изображениями, где фон удален с помощью SelfiSegmentation.
8. data/sirius_rembg - папка с изображениями, где фон удален с помощью rembg (итоговый подход). 
9. data/sirius_rembg_with_color - папка с изображениями, где фон удален с помощью rembg (итоговый подход) и заменен на однотонный цвет.
10. data/sirius_rembg_with_img - папка с изображениями, где фон удален с помощью rembg (итоговый подход) и заменен на другое изображение.








