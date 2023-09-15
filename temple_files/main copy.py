import cv2
# import numpy as np
# from tensorflow.keras.applications import MobileNetV2
# from tensorflow.keras.layers import Input
# from tensorflow.keras.models import Model
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# from tensorflow.keras.preprocessing import image


def load_and_compare_images(image_path, template_path):
    # Загрузите изображение стеллажа
    shelf_image = cv2.imread(image_path)

    # cv2.imshow('shelf_image', shelf_image)
    # cv2.waitKey(0)

    # Загрузите шаблон изображения товара
    template_image = cv2.imread(template_path)

#     cv2.imshow('template_image', template_image)
#     cv2.waitKey(0)
# #

    # Проверьте, что оба изображения были успешно загружены
    if shelf_image is None or template_image is None:
        return "Не удалось загрузить одно или оба изображения."

    # Преобразование шаблона и стеллажа в черно-белое изображение
    gray_shelf = cv2.cvtColor(shelf_image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    # cv2.imshow('gray_shelf', gray_shelf)
    # cv2.waitKey(0)
    # cv2.imshow('gray_template', gray_template)
    # cv2.waitKey(0)
#

    # Найдите совпадения шаблона в изображении стеллажа
    result = cv2.matchTemplate(gray_shelf, gray_template, cv2.TM_CCOEFF_NORMED)

    # cv2.imshow('result', result)
    # cv2.waitKey(0)

    # Установите порог для совпадений
    threshold = 0.8

    # Получите позицию максимального совпадения
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Если максимальное совпадение больше порога, то товар найден
    if max_val >= threshold:
        return "Товар найден на стеллаже."
    else:
        return "Товар не найден на стеллаже."


# Путь к изображению стеллажа
shelf_image_path = "images/part2.jpg"

# Путь к шаблону изображения товара
template_path = "templates/sample.jpg"

# Вызов функции для загрузки и сравнения изображений
result = load_and_compare_images(shelf_image_path, template_path)

# Вывод результата
print(result)











# import cv2

# img = cv2.imread('templates/sample.jpg')
# cv2.imshow('result', img)

# # print(img.shape)

# # img = cv2.resize(img(img.shape[1]//2, img.shape[0]//2))

# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# img = cv2.Canny(img, 50, 50)
# cv2.imshow('result', img)

# #

# cv2.waitKey(0)
# #

# cap = cv2.VideoCapture(0)
# cap.set(3, 500)
# cap.set(4, 300)

# while True:
#     success, img = cap.read()
#     cv2.imshow('Result', img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
