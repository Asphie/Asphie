import sys
import sqlite3 as sq 
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout , QLineEdit,QRadioButton, QMessageBox
import time

employees=20
guests=5

current=[("Алексеев","Илья","Алексеевич","23-Apr-1994","директор по информатизации","+79993456785","aleksee45@mail.ru","NULL","NULL"),
("Аржанов","Владислав","Александрович","27-Jan-1995","начальние отдела кадров","+79063194556","arhjanov12@yandex.ru","NULL","NULL"),
("Белоцерковец ","Дмитрий","Александрович","12-Sep-1983","менеджер","+79773332123","belotserkovets@gmail.com","NULL","NULL"),
("Богушев","Арсений","Александрович","09-Dec-1973","директор","+79264444334","Bogushev@mail.ru","NULL","NULL"),
("Гундарова","Софья","Анатольевна","30-Nov-1995","менеджер","+79256789012","Gundarova@yandex.ru","NULL","NULL"),
("Долженков","Борис","Алексеевич","23-Jun-2002","курьер","+79003196748","Dolzhenkov@gmail.com","NULL","NULL"),
("Журавова","Ангелина","Сергеевна","17-Aug-2002","специалист по корреспонденции","+79836571245","Zhuravova@gmail.com","NULL","NULL"),
("Клевцова","Варвара","Андреевна","15-Oct-2002","секретарь","+79023672156","Klevtsova@gmail.com","NULL","NULL"),
("Коваленко","Вероника","Александровна","17-Jul-1997","менеджер","+79271285522","Kovalenko@gmail.com","NULL","NULL"),
("Королев","Платон","Валеорьевич","13-Mar-1993","главный бухгалтер","+79773045689","Korolev@gmail.com","NULL","NULL"),
("Кубышкин","Роман","Евгеньевич","10-Oct-1985","менеджер по технологии","+79013219045","Kubyshkin@gmail.com","NULL","NULL"),
("Макаренко","Константин","Викторович","11-Nov-1984","бизнес аналитик","+79992341289","Makarenko@gmail.com","NULL","NULL"),
("Мартиросов","Артемий","Артурович","01-Feb-1974","smm - менеджер","+79027893459","Martirosov@gmail.com","NULL","NULL"),
("Мелкумян","Роберт","Робертович","16-May-1993","маркетолог","+79982341290","Melkumyan@gmail.com","NULL","NULL"),
("Олейник","Ольга","Викторовна","18-Jun-1993","руководитель проекта","+79762349987","Oleinik@gmail.com","NULL","NULL"),
("Полюцкий","Александр","Сергеевич","19-Jan-1981","юрист-консультант","+79673421894","Polyutsky@gmail.com","NULL","NULL"),
("Рустамов","Иброхим","Рустамович","29-Oct-1982","зав.хозяйством","+79231782392","Rustamov@gmail.com","NULL","NULL"),
("Рябцева","Алена","Александровна","14-Nov-1982","бухгалтер","+79321743981","Ryabtseva@gmail.com","NULL","NULL"),
("Саберова","Динара","Равилевна","28-Dec-1994","главный юрист","+79992341084","Saberova@gmail.com","NULL","NULL"),
("Сафонова","Ирина","Ивановна","15-Jul-1983","делопроизводитель","+79253419861","Safonov@gmail.com","NULL","NULL"),
("Стронина","София","Евгеньевна","31-Mar-2002","секретарь","+79162381629","Stronina@gmail.com","NULL","NULL"),
("Тарасов","Степан","Павлович","06-Jun-1996","менеджер","+79152371823","Тарасов@gmail.com","NULL","NULL"),
("Чекменёв","Кирилл","Андреевич","02-Aug-1998","дизайнер","+79172361959","Chekmenev@gmail.com","NULL","NULL"),
("Чернов","Максим","Дмитриевич","23-Dec-1999","аналитик","+79293652732","Chernov@gmail.com","NULL","NULL"),
("Шарофидинова","Ирода","Отабек","21-Mar-1991","уборщица","+79002893276","Sharofidinov@gmail.com","NULL","NULL"),
("Шундрик","Егор","Максимович","07-Apr-1992","расчетчик","+79281123119","Shundrick@gmail.com","NULL","NULL"),
("Шушняев","Никита","Максимовна","09-Sep-1991","сметчик","+79031732861","Shushnyaev@gmail.com","NULL","NULL")]

local = time.ctime(time.time())

with sq.connect("employees.db") as base:
    sql = base.cursor()
    sql.execute('DROP TABLE IF EXISTS employees')
    sql.execute("""CREATE TABLE IF NOT EXISTS employees(
        firstname TEXT,
        name TEXT,
        lastname TEXT,
        birth TEXT,
        job TEXT,
        phone TEXT,
        email TEXT,
        enter TEXT ,
        exit TEXT 
        );
        """)
    sql.executemany("INSERT INTO employees VALUES(?, ? , ?, ?, ? , ?, ? , ?,?)",current)
base.commit()

with sq.connect("guests.db") as base2:
    sql2 = base2.cursor()
    sql2.execute('DROP TABLE IF EXISTS guests')
    sql2.execute("""CREATE TABLE IF NOT EXISTS guests(
        firstname TEXT,
        name TEXT,
        lastname TEXT,
        birth TEXT,
        phone TEXT,
        email TEXT,
        enter INt,
        exit INT 
        );
        """)
base2.commit()

class PassControlApp(QWidget):
    def __init__(self):
        super().__init__()
        global sql
        global base
        global employees
        global guests
        self.sql = 0
        self.car = 0
        
        self.RadioButton=QRadioButton("Вам нужно парковочное место?")

        self.issue_pass_button2 = QPushButton('Меню гостя')
        self.issue_pass_button = QPushButton('Вход')
        self.issue_pass_button3 = QPushButton('Выход')
      
        self.issue_pass_button.clicked.connect(self.ENTER)
        self.issue_pass_button3.clicked.connect(self.EXIT)
        self.issue_pass_button2.clicked.connect(self.GST_ENTRY)
        
        self.RadioButton.toggled.connect(self.update)

        self.name = QLineEdit(self,placeholderText="Ведите идентификатор...")
        
        self.passv = QLineEdit(self,placeholderText="Ведите ваше Имя...")

        layout = QVBoxLayout()
        layout.addWidget(self.name)
        layout.addWidget(self.passv)
        layout.addWidget(self.RadioButton)
        layout.addWidget(self.issue_pass_button2)
        layout.addWidget(self.issue_pass_button)
        layout.addWidget(self.issue_pass_button3)

        self.setLayout(layout)
        self.setWindowTitle('Терминал Охраны')

    def GST_ENTRY(self):
        pass1.show()

    def ENTER(self):
        global guests
        global employees
        self.adc=self.name.text().find("@")
        self.dfe = self.name.text()

        self.local_time = time.ctime(time.time())
        if self.car == 1 :

            if employees!=0:
                if employees<5 and guests>0:
                    employees=employees-1
                    guests=guests-1
                else:
                    employees=employees-1
                    print ("Добро, пожаловать, есть свободные парковочные места")
                sql.execute(f"""UPDATE employees SET enter = ? where email = ? """,[self.local_time,self.dfe])
                sql.execute('SELECT email FROM employees')
                self.rows = sql.fetchall()
                if self.rows.count((self.name.text(),)) :
                    print("Сотрудник",self.dfe,"Вошёл на территорию предприятия")
                else:
                    print("Идентификатор не найден")
                base.commit()
              
            else:
                print("Извините, парковочных мест нет")
        elif self.car == 0 :
            sql.execute(f"""UPDATE employees SET enter = ? where email = ? """,[self.local_time,self.dfe])
            base.commit()
            sql.execute('SELECT email FROM employees')
            self.rows = sql.fetchall()
            if self.rows.count((self.name.text(),)):
                print("Сотрудник",self.dfe,"Вошёл на территорию предприятия")
            else:
                print("Идентификатор не найден")

    def EXIT(self):
        global guests
        global employees
        self.dfe = self.name.text()
        if self.car == 1:
            if employees<5 and guests<5 :
                employees=employees+1
                guests=guests+1
            employees=employees+1
        self.local_time = time.ctime(time.time())
        sql.execute(f"""UPDATE employees SET exit = ? where email = ? AND enter != 'NULL' """,[self.local_time,self.dfe])
        sql.execute('SELECT email FROM employees')
        self.rows = sql.fetchall()
        if self.rows.count((self.name.text(),)) :
            print("Сотрудник",self.dfe,"Вышел с территории предприятия")
        else:
            print("Идентификатор не найден")
        base.commit()
    base.commit()

    def update(self):
        if self.car == 0:
            self.car = 1
        else:
            self.car = 0
        print(self.car)


class gst_term(QWidget):
    def __init__(self):

        super().__init__()
        self.car = 0
        global sql2
        global base2
        global employees
        global guests

        self.issue_pass_button2 = QPushButton('Выход')
        self.issue_pass_button = QPushButton('Вход')
        self.RadioButton=QRadioButton("Вам нужно парковочное место?")

        self.issue_pass_button.clicked.connect(self.interance)
        self.issue_pass_button2.clicked.connect(self.gostevoy)
        self.RadioButton.toggled.connect(self.update)

        self.exit= QLineEdit(self,placeholderText="Ведите идентификатор для выхода...")

        self.firstname = QLineEdit(self,placeholderText="Фамилия")
        self.name = QLineEdit(self,placeholderText="Имя")
        self.lastname = QLineEdit(self,placeholderText="Отчество")
        self.birth = QLineEdit(self,placeholderText="Дата Рождения")
        self.phone = QLineEdit(self,placeholderText="Номер Телефона")
        self.email = QLineEdit(self,placeholderText="Идентификатор")

        layout = QVBoxLayout()

        layout.addWidget(self.firstname)
        layout.addWidget(self.name)
        layout.addWidget(self.lastname)
        layout.addWidget(self.birth)
        layout.addWidget(self.phone)
        layout.addWidget(self.email)

        layout.addWidget(self.RadioButton)
        layout.addWidget(self.issue_pass_button)
        layout.addWidget(self.exit)
        layout.addWidget(self.issue_pass_button2)

        self.setLayout(layout)
        self.setWindowTitle('Гостевой Терминал')

    def update(self):
        if self.car == 0:
            self.car = 1
        else:
            self.car = 0
        if guests ==0:
            print("Места Закончились")

    def gostevoy(self):
        global guests
        global employees
        if self.car == 1:
            employees = employees + 1
            guests = guests + 1
        self.exi = self.exit.text()
        self.time = time.time()
        self.local_time = time.ctime(time.time())
        sql2.execute(f"""UPDATE guests SET exit = ? where email = ? """,[self.time,self.exi])
        sql2.execute('SELECT email FROM guests')
        self.rows = sql2.fetchall()
        if self.rows.count((self.exit.text(),)) :
            print("Гость",self.exi,"Вышел c территории предприятия")
            sql2.execute('SELECT enter , exit FROM guests WHERE email = ? ', (self.pochtat,))
            self.rows2 = sql2.fetchall()
            self.tkk = self.rows2[0]
            self.tk,self.tx = self.tkk
            if self.tx-self.tk>10:
                print(f"Гость {self.exi} - вы превысили допустимое время на :{round((self.tx)-(self.tk)-10)} сек, 'необходимо обратиться к начальству'")
            if self.tx-self.tk<10:
                print(f"Гость {self.exi} вы пробыли : {round((self.tx)-(self.tk))} ")
        else:
            print("Идентификатор не найден")

    def interance(self):
        global guests
        global employees
        if self.car == 1:
            if guests ==0:
                print("Места Закончились")
            else:
                employees = employees - 1
                guests = guests - 1
                self.time = time.time()
                self.familt=self.firstname.text()
                self.namet=self.name.text()
                self.otcht=self.lastname.text()
                self.datet=self.birth.text()
                self.nomert=self.phone.text()
                self.pochtat=self.email.text()
                self.CORT=[(self.familt,self.namet,self.otcht,self.datet,self.nomert,self.pochtat,self.time,0)]
                    
                sql2.execute('SELECT email FROM guests')
                self.rows = sql2.fetchall()
                if self.rows.count((self.email.text(),)) :
                    print("Идентификатор уже используется")
                else:
                    print("Гость",self.pochtat,"Вошёл на территорию предприятия")
                    sql2.executemany("INSERT INTO guests VALUES( ?, ? , ? , ? , ? , ? , ? , ? )",self.CORT)
                    base2.commit()
        else:
            self.time = time.time()
            self.familt=self.firstname.text()
            self.namet=self.name.text()
            self.otcht=self.lastname.text()
            self.datet=self.phone.text()
            self.nomert=self.phone.text()
            self.pochtat=self.email.text()
            self.CORT=[(self.familt,self.namet,self.otcht,self.datet,self.nomert,self.pochtat,self.time,0)]
            sql2.execute('SELECT email FROM guests')
            self.rows = sql2.fetchall()
            if self.rows.count((self.email.text(),)) :
                print("Идентификатор уже используется")
            else:
                print("Гость",self.pochtat,"Вошёл на территорию предприятия")
                sql2.executemany("INSERT INTO guests VALUES( ?, ? , ? , ? , ? , ? , ? , ? )",self.CORT)
                base2.commit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pass_control = PassControlApp()
    pass1 = gst_term()
    pass_control.show()
    sys.exit(app.exec())