import mysql.connector
import pandas as pd
from time import ctime
import smtplib
from email.message import EmailMessage
import random


while True:
    try:
        mydb = mysql.connector.connect(host='localhost',user='root',password='',database='test1')
        break
    except:
        print("Check Your Connection")
        continue


def email_settings(message,subject,email_rev):

    sen_email = "Put Sender Email Address Here"
    rev_email = email_rev
    pw = "Put Sender Email Password Here"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sen_email, str(pw))

    email = EmailMessage()
    email['From'] = sen_email
    email['To'] = rev_email
    email['Subject'] = str(subject)
    email.set_content(message)

    server.send_message(email)

    #server.sendmail(sen_email,rev_email,str(message))


def database():

    try:

        global db_id, db_username, db_age, db_pw, db_amount

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM customers")

        myresult = mycursor.fetchall()
        x = pd.DataFrame(myresult)

        db_id = x[[0]]
        db_username = x[[1]]
        db_age = x[[2]]
        db_pw = x[[3]]
        db_amount = x[[4]]

    except:

        db_id = []
        db_username = []
        db_age = []
        db_pw = []
        db_amount = []

#PASSWORD GENERATE FUNCTION
def password_generate():
    global password_gen

    x = [1,2,3,4]
    y = [5,6,7,8]
    z = ["A","B","C","D","E"]
    w = ["!","@","#","$","%","^"]
    v = ["F","G","H","I","J"]
    u = ["&","*","+","=","-","_"]
    T = ["a","b","c","d","e"]

    password_gen = str(random.choice(x)) + str(random.choice(v)) + random.choice(z) + random.choice(u) + str(random.choice(y)) + random.choice(v) + random.choice(T)

def get_currrent_id():

    try:
        mydb = mysql.connector.connect(host='localhost',user='root',password='',database='test1')

        mycursor_5 = mydb.cursor()
        select_2 = "SELECT MAX(id) FROM customers"


        mycursor_5.execute(select_2)

        mybalance = mycursor_5.fetchall()

        cu_id_df = pd.DataFrame(mybalance)
        global cu_id
        cu_id = cu_id_df[0][0]
        cu_id = int(cu_id)

    except:
        cu_id = 0



def admin_login():

    while True:

        print("ADMIN MENUE\n----------------------")
        print("1-----> CREATE NEW CUSTOMER\n"
              "2-----> BACK\n"
              "-----------------------------------")

        admin_ans = input("Select a option : ")

        if admin_ans == "1":
            database()


            while True:
                password_generate()

                if password_gen in str(db_pw):
                    password_generate()
                    continue
                else:
                    break

            print("* special note : minamum deposit value is RS.500/= *")

            get_currrent_id()
            us_id =  str(int(cu_id) + 1)
            us_name = input("Enter name : ")
            us_password = password_gen
            us_age = input("Enter Age : ")
            us_dep_amount = int(input("Enter Deposit Amount : "))
            us_email = input('Enter Valid Email Adddress : ')

            mycursor_5 = mydb.cursor()

            insert_1 = "INSERT INTO customers (id, name, age, password, amount, email) VALUES(%s, %s, %s, %s, %s, %s)"
            ins_values = (us_id,us_name,us_age,us_password,us_dep_amount,us_email,)

            mycursor_5.execute(insert_1, ins_values)
            mydb.commit()

            if mycursor_5.rowcount == 1:

                email_text =  "Account Created Successfully. " + "ACC NO : " + us_id + "  Password : " + us_password
                email_settings(email_text,"New Account Details",us_email)

                database()
                print("Customer Created Succuesfully ( Email Sent )\n------------------------------------")

        elif admin_ans == "2":
            break

        else:
            print("please select valid Option")

def login():

    global login_status , current_user_id , currrent_user_email

    login_status = False
    current_user_id = ""

    print("LOGIN MENUE\n--------------------------------")

    while True:

        get_user_name = input("Enter User Name Here : ")
        get_pw = input("Enter Password Here : ")

        if get_user_name in str(db_username) and get_pw in str(db_pw):
            print("----------------------------")
            print( get_user_name.upper(),"LOGGED IN SUCCESSFULY" )
            print("-----------------------------")

            mycursor_2 = mydb.cursor()
            search_1 = "SELECT id, email FROM customers WHERE name = %s AND password = %s"
            value_1 = (get_user_name,get_pw)

            mycursor_2.execute(search_1,value_1)

            result_2 = mycursor_2.fetchall()
            result_2_df = pd.DataFrame(result_2)

            df_values = []

            for i in result_2_df.values:
                df_values.append(i)


            result_2_df_id = str(df_values[0][0])
            result_2_df_email = str(df_values[0][1])

            login_status = True
            current_user_id = result_2_df_id
            currrent_user_email = result_2_df_email



            break

        else:
            print("------------------\nUSER NOT FOUND\n----------------------")


def deposits(user_id_d):

    while True:
        user_id_d = str(user_id_d)
        mycursor_3 = mydb.cursor()

        dep_amount = input("Enter Amount To Deposit :")
        if dep_amount.isdigit():
            dep_amount = int(dep_amount)

            update_1 = "UPDATE customers SET amount = amount + %s WHERE id = %s"
            dep_values = (dep_amount,user_id_d)

            mycursor_3.execute(update_1,dep_values)
            mydb.commit()

            if mycursor_3.rowcount == 1:

                message_dep = str(dep_amount) + "/= RS. Amount Deposited Successfully " + " At " + str(ctime())
                email_settings(message_dep,"Cash Deposited",currrent_user_email)
                print("Amount Deposited Succesfully ( Email Sent )")
                break

            else:
                print("Process Not Complete")
                continue
        else:
            print("Please Enter Valid Amount")


def withdrawals(user_id_w):

    while True:
        user_id_w = str(user_id_w)
        mycursor_4 = mydb.cursor()

        with_amount = input("Enter Amount To Withdraw :")
        if with_amount.isdigit():
            with_amount = int(with_amount)

            update_2 = "UPDATE customers SET amount = amount - %s WHERE id = %s"
            with_values = (with_amount,user_id_w)

            mycursor_4.execute(update_2,with_values)
            mydb.commit()

            if mycursor_4.rowcount == 1:

                message_with = str(with_amount) + "/= RS. Amount Withdrawed Successfully " + " At " + str(ctime())
                email_settings(message_with,"Cash Withdrawed",currrent_user_email)
                print("Amount Withdrawed Successfully ( Email Sent )")
                break

            else:
                print("Process Not Complete")
                continue
        else:
            print("Please Enter Valid Amount")


def balance(user_id_b):

    user_id_b = str(user_id_b)

    mycursor_5 = mydb.cursor()
    select_2 = "SELECT amount FROM customers WHERE id = %s"
    balance_val = (user_id_b,)

    mycursor_5.execute(select_2,balance_val)

    mybalance = mycursor_5.fetchall()

    balance_df = pd.DataFrame(mybalance)

    print("Your Balance Is : ",balance_df[0][0], "RS","at" , ctime())

def main():
    database()

    while True:

        print("WELCOME TO CENTRAL BANK SYSTEM\n--------------------------------")
        print("1--------> Admin\n"
              "2--------> Customer\n"
              "3--------> Exit")

        while True:
            main_log = input("Select Section : ")

            if main_log == "1":
                admin_login()
                break

            elif main_log == "2":
                login()
                if login_status == True:

                    while True:

                        print("MAIN MENUE\n--------------------------------")
                        print(" 1-------> Deposits\n",
                              "2-------> Withdrawls\n",
                              "3-------> Check Blance\n",
                              "4-------> Log Out\n",
                              "--------------------------------")

                        answer_main_m = input("Select a Option : ")
                        if answer_main_m == "1":
                            deposits(current_user_id)


                        elif answer_main_m == "2":
                            withdrawals(current_user_id)


                        elif answer_main_m == "3":
                            balance(current_user_id)

                        elif answer_main_m == "4":
                            print("USER LOGGED OUT SUCCESFULLY.\n----------------------------")
                            main()

            elif main_log == "3":
                exit()
            else:
                print("Select valid option")



main()







