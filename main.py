import tkinter as tk
from tkinter import ttk
import sqlite3


# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
##############################################################################

    # Создание и работа с главным окном
    def init_main(self):
        # Создаем панель инструментов
        toolbar = tk.Frame(bg='#d7d7d7', bd = 2)
        # упаковка
        toolbar.pack(side=tk.TOP, fill=tk.X)
############################################################################## СОЗДАНИЕ КНОПОК

        # ДОБАВИТЬ
        self.img_add = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, text = 'Добавить', bg='#d7d7d7',
                            bd=0, image=self.img_add, command=self.open_child)
        btn_add.pack(side = tk.LEFT)

        # ИЗМЕНИТЬ
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit = tk.Button(toolbar, text = 'Изменить', bg='#d7d7d7',
                            bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit.pack(side = tk.LEFT)

        # УДАЛИТЬ
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_edit = tk.Button(toolbar, text = 'Изменить', bg='#d7d7d7',
                            bd=0, image=self.delete_img, command=self.delete_records)
        btn_edit.pack(side = tk.LEFT)

        # ПОИСК
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, text = 'Изменить', bg='#d7d7d7',
                            bd=0, image=self.search_img, command=self.open_search)
        btn_search.pack(side = tk.LEFT)

        # ОБНОВИТЬ
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, text = 'Изменить', bg='#d7d7d7',
                            bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side = tk.LEFT)

############################################################################## Таблица с данными
        # Добавляем столбцы
        self.tree = ttk.Treeview(self, 
                                 columns=('ID', 'name', 'phone', 'email'),
                                 height=45, 
                                 show='headings')
        
        # Устанавливаем размеры столбцов и выравниваем по центру
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        # Задаем именна 
        self.tree.heading('ID', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')

        self.tree.pack(side=tk.LEFT)

        # Ползунок
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
############################################################################## ОСНОВНЫЕ МЕТОДЫ

    # Метод добавления данных
    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()


    # Обновление (изменение ) данных
    def update_record(self, name, phone, email):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute(''' UPDATE users SET name=?, phone=?, email=? WHERE ID=?''', 
                            (name, phone, email, id))
        self.db.conn.commit()
        self.view_records()

    
    # Вывод данных в виджет таблицы
    def view_records (self):
        self.db.cur.execute('''SELECT * FROM users ''')

        # Удалить все из виджета
        [self.tree.delete(i) for i in self.tree.get_children()]
        # Добавляем в таблицу все данные из БД
        [self.tree.insert('','end', values=row)
         for row in self.db.cur.fetchall()]

    # УДАЛЕНИЕ ЗАПИСЕЙ
    def delete_records(self):
        #Цикл по выделенным записям
        for selecetion_item in self.tree.selection():
            #удаляем из БД
            self.db.cur.execute('''DELETE FROM users WHERE ID=?''',
                                (self.tree.set(selecetion_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # ПОИСК ЗАПИСИ
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute(
            '''SELECT * FROM users WHERE name LIKE ?''', (name, ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end', values=row)
         for row in self.db.cur.fetchall()]
        
##############################################################################
    # Метод вызывающий дочернее окна
    def open_child(self):
        Child()

    # Метод вызывающий окно изменения данных
    def open_update_dialog(self):
        Update()

    # Метод вызывающий окно поиска
    def open_search(self):
        Search()

##############################################################################
# Создание окна ДОБАВЛЕНИЯ
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

     # инициализация виджетов дочернего окна
    def init_child(self):
        # заголовок окна
        self.title('Добавление контакта')
        # размер окна
        self.geometry('400x220')
        # ограничение изменения размеров окна
        self.resizable(False, False)
        # перехватываем все события происходящие в приложении
        self.grab_set()
        # захватываем фокус
        self.focus_set()
##############################################################################
        # Текст
        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон: ')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail: ')
        label_email.place(x=50, y=110)
        # Виджеты ввода
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
##############################################################################

        # кнопка закрытия дочернего окна
        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=200, y=150)

        # кнопка добавления
        self.btn_add = tk.Button(self, text='Добавить')
        self.btn_add.place(x=265, y=150)
        self.btn_add.bind('<Button-1>', lambda event:
                    self.view.records(self.entry_name.get(),
                                       self.entry_phone.get(),
                                       self.entry_email.get()))
##############################################################################

# РЕДАКТИРОВАНИЕ КОНТАКТОВ
class Update(Child):
        
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title ('Редактировать позицию')
        self.btn_add.destroy()

        self.btn_edit = ttk.Button(self, text="Редактировать")
        self.btn_edit.place(x=265, y=150)
        self.btn_edit.bind('<Button-1>', lambda event:
                    self.view.update_record(self.entry_name.get(),
                                            self.entry_phone.get(),
                                            self.entry_email.get()))
        self.btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute(''' SELECT * FROM users WHERE ID=?''', (id, ))
        # Получем доступ к первой записи из выборки
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
##############################################################################

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Поиск по контактам')
        self.geometry('300x100')
        self.resizable(False,False)
        self.grab_set()
        self.focus_set()
##############################################################################
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=20, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=70, y=20)
##############################################################################

        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=200, y=70)

        self.btn_add = tk.Button(self, text='Найти')
        self.btn_add.place(x=150, y=70)
        self.btn_add.bind('<Button-1>', lambda event: self.view.search_records(self.entry_name.get()))



##############################################################################

# Класс БД
class DB:
    def __init__(self):
        # Создаем соединение с БД
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                phone TEXT,
                                email TEXT) """)
        self.conn.commit()

    def insert_data(self, name, phone, email):
        self.cur.execute(""" INSERT INTO users (name, phone, email)
                             VALUES(?, ?, ?)""", (name, phone, email))
        self.conn.commit()
##############################################################################


# При запуске программы
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('645x450')
    root.configure(bg ='white')
    root.resizable(False, False)
    root.mainloop()

# Коммит


