import psycopg2


def creat_bd(conn):
    # 1. Создание структуры БД
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS client_data(
            client_id INTEGER UNIQUE PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            surname VARCHAR(30) NOT NULL,
            email VARCHAR(30) NOT NULL);
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES client_data(client_id),
            phones INTEGER CHECK (phones between 0 and 9999999999));
        ''')
        conn.commit()
        print('Создание структуры БД..."ВЫПОЛНЕНО"')


def client_add(conn, client_id, name, surname, email, phones=None):
    # 2. Функция, позволяющая добавить нового клиента
    with conn.cursor() as cur:
        cur.execute('''
            INSERT INTO client_data(client_id, name, surname, email)
            VALUES(%s, %s, %s, %s); 
                    ''', (client_id, name, surname, email))
        conn.commit()
    if phones is not None:
        for phone in phones:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO phones(client_id, phones)
                    VALUES(%s, %s);
                            ''', (client_id, phone))
                conn.commit()
    print(f'Клиент: {name}, добавлен')


def phone_add(conn, client_id, phones):
    # 3. Функция, позволяющая добавить телефон для существующего клиента
    for phone in phones:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO phones(client_id, phones)
                VALUES(%s, %s);
                        ''', (client_id, phone))
            conn.commit()
    print('Номер добавлен')


def change_client(conn, client_id, name=None, surname=None, email=None, phones=None):
    # 4. Функция, позволяющая изменить данные о клиенте
    with conn.cursor() as cur:
        cur.execute('''
            SELECT * from client_data
            WHERE client_id = %s
                    ''', (client_id,))
        temp = cur.fetchone()
        if name is None:
            name = temp[1]
        if surname is None:
            surname = temp[2]
        if email is None:
            email = temp[3]

        cur.execute('''
            UPDATE client_data SET name = %s, surname = %s, email =%s
            WHERE client_id = %s
            ''', (name, surname, email, client_id))
        cur.execute('''
                    SELECT * from client_data
                    WHERE client_id = %s
                            ''', (client_id,))
        conn.commit()
        print('Данные о клиенте изменены')



def delete_phone(conn, client_id, phones):
    # 5. Функция, позволяющая удалить телефон для существующего клиента
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM phones
            WHERE phones = %s and client_id = %s
            ''', (phones, client_id))
        conn.commit()
        print(f'Номер телефона "{phones}" удален')


def delete_client(conn, client_id):
    # 6. Функция, позволяющая удалить существующего клиента
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM phones
            WHERE client_id = %s
                    ''', (client_id,))
        cur.execute('''
            DELETE FROM client_data
            WHERE client_id = %s
                    ''', (client_id,))
        conn.commit()
        print('Клиент удален!')


def find_client(conn, name=None, surname=None, email=None, phones=None):
    # 7.Функция, позволяющая найти клиента по его данным(имени, фамилии, email-у или телефону)
    if phones is not None:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT cd.client_id FROM client_data cd
                JOIN phones p ON p.client_id = cd.client_id
                WHERE p.phones=%s;
                        ''', (phones,))
            print(f'Клиент с id = {cur.fetchone()[0]}')
    else:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT client_id FROM client_data 
                WHERE name=%s OR surname=%s OR email=%s;
                        ''', (name, surname, email))
        print(f'Клиент с id = {cur.fetchone()[0]}')


if __name__ == '__main__':
    with psycopg2.connect(database='py-homeworks-db', user='postgres', password='postgres') as conn:
        # creat_bd(conn)
        # client_add(conn, 1, 'Dima', 'Sol', 'asd@mas.ru')
        # client_add(conn, 2, 'Mila', 'Ssd', 'assdd@mas.ru')
        # client_add(conn, 3, 'Aima', 'kj', 'asasdad@mas.cru')
        # client_add(conn, 4, 'Alima', 'Hsj', 'asasdad@mas.cru', [45, 555555])
        # phone_add(conn, 1, [45])
        # change_client(conn, 1, 'Misha')
        # delete_phone(conn, 1, 45)
        # delete_client(conn, 3)
        # find_client(conn, phones=45)

    conn.close()

