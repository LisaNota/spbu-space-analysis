import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import multiprocessing as mp
import os
import tkinter as tk
from tkinter import messagebox, filedialog


file_path = ""


def analysing(image, number, queue):
    image_with_objects = image.copy()
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image = cv2.filter2D(image, -1, kernel)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    _, binary_image = cv2.threshold(blurred_image, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    space_objects = []

    font = ImageFont.truetype("font/arial.ttf", 14)

    for contour in contours:

        area = cv2.contourArea(contour)
        x, y, width, height = cv2.boundingRect(contour)

        center_x = x + width / 2
        center_y = y + height / 2

        brightness = np.sum(gray_image[y:y + height, x:x + width])

        object_type = classified(area, brightness)
        space_object = {
            "x": center_x,
            "y": center_y,
            "brightness": brightness,
            "type": object_type,
            "size": width * height
        }

        space_objects.append(space_object)
        cv2.rectangle(image_with_objects, (x, y), (x + width, y + height), (0, 255, 0), 2)
        (text_width, text_height) = cv2.getTextSize(object_type, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, thickness=1)[
            0]
        cv2.rectangle(image_with_objects, (x, y - text_height - 5), (x + text_width // 2, y - 5), (0, 255, 0),
                      cv2.FILLED)

        pil_image = Image.fromarray(image_with_objects)
        draw = ImageDraw.Draw(pil_image)
        draw.text((x, y - text_height - 10), object_type, font=font, fill=(0, 0, 0))
        image_with_objects = np.array(pil_image)

    output_directory = f"image_result"
    os.makedirs(output_directory, exist_ok=True)
    output2_directory = f"image_crop"
    os.makedirs(output2_directory, exist_ok=True)
    cv2.imwrite(f"image_crop/{number}.tif", image_with_objects)

    with open(f"image_result/{number}.txt", "w", encoding="utf-8") as file:
        for object in space_objects:
            file.write(f"Координаты: ({object['x']}, {object['y']}); Яркость: {object['brightness']}; Размер: {object['size']}; Тип: {object['type']}\n")
    print(f"Выполнен процесс №{number}")
    queue.put((image_with_objects, number - 1))
    return

def classified(area, brightness):
    return {
        area < 10 and brightness > 100: "звезда",
        area < 10 and brightness > 50: "комета",
        area < 10 and brightness > 0: "планета",
        area > 10000 and brightness > 1000000: "галактика",
        area < 10000 and brightness > 1000000: "квазар",
        area >= 10 and brightness > 0: "звезда"
    }[True]

def split_image(image, num_parts):
    height, width, _ = image.shape
    part_width = (width // num_parts) + 1
    part_height = (height // num_parts) + 1
    parts = []
    for chunk_width in range(num_parts):
        for chunk_height in range(num_parts):
            part = image[chunk_height * part_height:min((chunk_height + 1) * part_height, len(image))]
            part = part[:, chunk_width * part_width:(chunk_width + 1) * part_width, :]
            parts.append(part)
    return parts


def parallel_processing(full_path_to_image):
    directory = r'C:\Users\sibfl\Images'

    queue = mp.Queue()
    # Загрузка изображения
    image = cv2.imread(full_path_to_image)
    num_parts = 4
    mp_parts = split_image(image, num_parts)

    Processes = []
    number = 0
    for mp_part in mp_parts:
        number += 1
        Process = mp.Process(target=analysing, args=(mp_part, number, queue))
        Process.start()
        Processes.append(Process)

    sum_finish = 0

    image_parts = [0] * len(mp_parts)

    while sum_finish != len(Processes):
        if not queue.empty():
            sum_finish += 1
            image_part = queue.get()
            image_parts[image_part[1]] = image_part[0].copy()

    image_vstack = [image_parts[i] for i in range(0, num_parts ** 2, num_parts)]

    k = 0
    for i in range(num_parts):
        for j in range(1, num_parts):
            image_vstack[i] = np.vstack([image_vstack[i], image_parts[j + k]])
        k += num_parts

    image_with_objects = np.hstack(image_vstack)

    new_directory = directory[:directory.rfind("/")]
    cv2.imwrite(f"{new_directory}/new_image.tif", image_with_objects)
    messagebox.showinfo("Готово", "Результат сохранен")


def select():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.tif;*.jpg;*.png")])
    messagebox.showinfo("Готово", "Изображение успешно загружено")


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Параллельная обработка космических изображений")
    root.geometry("500x300")

    lbl = tk.Label(root, text="Добро пожаловать! Перед началом работы, ознакомьтесь с инструкцией:", font=("Arial", 10))
    lbl.place(relx=0.01, rely=0.1)
    lbl = tk.Label(root, text="1. Выберите космическое изображение, содержащее необходимые объекты.")
    lbl.place(relx=0.01, rely=0.2)
    lbl = tk.Label(root, text="2. Загрузите изображение с помощью кнопки 'Загрузить'.")
    lbl.place(relx=0.01, rely=0.3)
    lbl = tk.Label(root, text="3. Нажмите на кнопку 'Провести анализ'.")
    lbl.place(relx=0.01, rely=0.4)
    lbl = tk.Label(root, text="4. После завершения всех процессов результат будет доступен в папке 'image_result'.")
    lbl.place(relx=0.01, rely=0.5)

    choose = tk.Button(root, text="Загрузить изображение", width=30, bg="#DDDDDD", command=select)
    choose.place(relx=0.03, rely=0.65)

    start = tk.Button(root, text="Провести анализ", width=30, bg="#DDDDDD", command=lambda: parallel_processing(file_path))
    start.place(relx=0.5, rely=0.65)

    root.mainloop()
