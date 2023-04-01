import pyodbc

conn = pyodbc.connect("DRIVER={SQLite3 ODBC Driver};SERVER=localhost;DATABASE=coffee.db;Trusted_connection=yes")
cursor = conn.cursor()


def join_coffee_and_cart():
    return cursor.execute("""
    SELECT coffee_t.id, coffee_t.name, coffee_t.country, cart_t.quantity, cart_t.amount 
    FROM cart_t
    JOIN coffee_t ON cart_t.coffee_id = coffee_t.id;
    """)


class CoffeeT:

    def get_coffee_ls(self) -> list:
        ls = cursor.execute('select * from coffee_t;')
        return [c for c in ls]

    def get_coffee_name_by_id(self, id):
        res = cursor.execute(f'select name from coffee_t where id={id};')
        return res.fetchone()[0]

    def remove_value_from_db(self, quantity, cid):
        command = """
        UPDATE coffee_t
        SET  quantity = quantity - ?
        WHERE id = ?;
        """
        cursor.execute(command, quantity, cid)
        conn.commit()


class CartT:
    def get_cart_ls(self) -> list:
        res = join_coffee_and_cart()
        return [c for c in res]

    def add_to_cart(self, data: dict):
        ins_command = """
           INSERT INTO cart_t (coffee_id, quantity, amount) VALUES (?, ?, ?)
           """
        upd_command = """UPDATE cart_t SET quantity = ?, amount = ? WHERE coffee_id = ?;"""
        for k, v in data.items():
            # {3: {'price': 18.0, 'quantity': 2.0}, 5: {'price': 18.0, 'quantity': 2.0}})
            id_count = cursor.execute(f"SELECT COUNT(*) FROM cart_t WHERE coffee_id = {k};")
            if id_count.fetchone()[0] > 0:

                cursor.execute(upd_command, v['quantity'], v['price'], k)
            else:
                cursor.execute(ins_command, k, v['quantity'], v['price'])
        conn.commit()

    def clear_cart(self):
        cursor.execute("DELETE FROM cart_t")
        conn.commit()


coffee_obj = CoffeeT()
cart_obj = CartT()


def close_con():
    return conn.close()
