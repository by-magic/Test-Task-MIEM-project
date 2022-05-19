import random
from array import *
from textwrap import wrap
from tkinter import messagebox
from tkinter import *
from random import randint
from io import BytesIO
from PIL import Image, ImageTk
import requests
import webbrowser

root = Tk()


def load_image(url, canvas_image):
    response_image = requests.get(url)
    label_image = Label(canvas_image)

    if response_image.status_code != 200:
        label_image['text'] = 'No image'
    else:
        pil_image = Image.open(BytesIO(response_image.content))
        # корректировка размера иозображения
        new_size = (200, 300)
        ratio = min(float(new_size[0]) / pil_image.size[0], float(new_size[1]) / pil_image.size[1])
        w = int(pil_image.size[0] * ratio)
        h = int(pil_image.size[1] * ratio)
        resized = pil_image.resize((w, h), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(resized)

        label_image.config(image=image, text='')
        # прикрепляем ссылку на изображение к объекту label,
        # чтобы изображение не удалил сборщик мусора
        label_image.image = image
        label_image.update()

        label_image.pack(side='right')


def line_break(root, label_2, art):
    root.update()
    width = label_2.winfo_width()
    print(width)
    if width > 100:
        char_width = width / len(art)
        wrapped_text = '\n'.join(wrap(art, int(100 / char_width)))
        label_2['text'] = wrapped_text


def btn_click():
    object_name = object_nameField.get()
    response = requests.get(
        f'https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&isOnView=true&q={object_name}')
    res_to_json = response.json()
    print(type(response))
    print(res_to_json)
    length = len(res_to_json['objectIDs'])
    print(length)
    try:
        id = randint(0, length - 1)
        print(id)
        ob_id = res_to_json['objectIDs'][id]
        print(res_to_json)
        print(ob_id)
        response1 = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(ob_id))
        res1_to_json = response1.json()
        print(response1.text)
    except KeyError:
        messagebox.showinfo(message='Error in id of object')
        print('Error in id of object')
    author_chb = ''
    title_chb = ''
    date_chb = 0
    try:
        if res1_to_json['objectID'] == ob_id:
            title_chb = res1_to_json['title']
    except KeyError:
        print('Error in id of object')
    if author_chb_value.get() == 1:
        try:
            for auth in res1_to_json['constituents']:
                author_chb = ', ' + auth['name']

        except TypeError:
            author_chb = ', No author'
            print("No author")

    if image_chb_value.get() == 1:
        try:
            url = res1_to_json['primaryImage']
            print('URL:', url)
            if url != '':
                load_image(url, canvas_image)  # создание изображения
            else:
                messagebox.showinfo(message='No image')
        except LookupError:
            print('No image')
    if year_chb_value.get() == 1:
        try:
            date_chb += res1_to_json['objectBeginDate']
        except TypeError:
            date_chb += ', no date'
            print("No begin date")
    print(date_chb)
    if url_chb_value.get() == 1:
        url_chb = res1_to_json['objectURL']
        label_link = Label(root, text=title_chb, fg="blue", cursor="hand2")
        label_link.bind("<Button-1>", webbrowser.open_new(url_chb))

    art_info = title_chb + author_chb + ' ' + str(date_chb)
    text_info.set(art_info)


# Описание главного экрана
root['bg'] = 'coral2'
root.title('The Metropolitan Museum of Art')
root.wm_attributes('-topmost', 0.7)
root.geometry('900x500')
#
root.resizable(width=False, height=False)
# создание иконки
icon = PhotoImage(file='met.png')
root.iconphoto(False, icon)
#
canvas_image = Canvas(root, height=300, width=100)
canvas_image.place(x=695, y=100)
#
frame = Frame(root, bg='papaya whip')
frame.place(anchor='nw', relwidth=0.35, relheight=0.7)
#
label_help = Label(root,
                   bg='coral1',
                   text='Enter a word to find an art for this word:',
                   font=(10)
                   )
label_help.place(x=340, y=15)

# Поле для ввода текста
object_nameField = Entry(root, bg='white', font=30)
object_nameField.place(x=380, y=50)

# Заголовок топа 5 арт объектов
label_1 = Label(frame, text='Top 5 arts of the day',
                font=('Times New Roman', 15, 'roman'),
                padx=20,
                relief=RAISED,
                bg='papaya whip'
                )
label_1.pack()

#
text_info = StringVar()
label_info = Label(root, bg='yellow', textvariable=text_info)
label_info.place(x=370, y=370)

# Создание и размещение кнопки
btn = Button(root, text='Find art!',
             bg='goldenrod',
             activebackground='white',
             command=btn_click)
btn.place(x=440, y=210)

# создание выборочного списка с галочками
author_chb_value = IntVar()
image_chb_value = IntVar()
year_chb_value = IntVar()
url_chb_value = IntVar()

author_chb = Checkbutton(root, text='show author', bg='goldenrod', font=10,
                         variable=author_chb_value,
                         offvalue=0,
                         onvalue=1)
image_chb = Checkbutton(root, text='show image', bg='goldenrod', font=10,
                        variable=image_chb_value,
                        offvalue=0,
                        onvalue=1
                        )
year_chb = Checkbutton(root, text='show year', bg='goldenrod', font=10,
                       variable=year_chb_value,
                       offvalue=0,
                       onvalue=1
                       )
url_chb = Checkbutton(root, text='open website in browser', bg='goldenrod', font=10,
                      variable=url_chb_value,
                      offvalue=0,
                      onvalue=1
                      )

author_chb.place(x=370, y=80)
image_chb.place(x=370, y=110)
year_chb.place(x=370, y=140)
url_chb.place(x=370, y=170)

response_test = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects')
response_test_to_json = response_test.json()

# Создаем массив со всеми id арт объектов музея
list_of_id = array('l', [])
for d in response_test_to_json['objectIDs']:
    list_of_id.append(d)

# Создание списка 5 случайно выбранных арт объектов
for i in range(1, 6):
    obj = random.choice(list_of_id)
    response_top_5 = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(obj))
    res5_to_json = response_top_5.json()
    title = ''
    author = ''
    date = 0
    if res5_to_json['objectID'] == obj:
        title += res5_to_json['title']
        try:
            date += res5_to_json['objectBeginDate']
        except TypeError:
            print("No begin date")
        try:
            for j in res5_to_json['constituents']:
                author += j['name']
        except TypeError:
            print("No author")

    art = title + ', ' + author + ' ' + str(date)
    label_2 = Label(frame,
                    bg='yellow',
                    font=('Times New Roman', 10, 'roman'),
                    padx=10,
                    pady=1
                    )
    label_2['text'] = ''
    label_2['text'] += art
    label_2.pack()

    # перенос строки на следующую, в случае невместимости в frame
    line_break(root, label_2, art)

root.mainloop()
