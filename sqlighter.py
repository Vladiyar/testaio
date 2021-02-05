import sqlite3


class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    # def get_date(self, date):
    #     with self.connection:
    #         result = self.cursor.execute('SELECT `date` FROM `old`').fetchall()
    #         if
    def check_curr(self, usd):
        """comment"""
        with self.connection:
            result = self.cursor.execute('SELECT `usd` FROM `old`').fetchall()
            if float(result[-1][0]) == float(usd):
                return True
            else:
                return False

    def get_usd(self):
        with self.connection:
            result = self.cursor.execute('SELECT `usd` FROM `old`').fetchall()
            return result[-1][0]

    def get_eur(self):
        with self.connection:
            result = self.cursor.execute('SELECT `eur` FROM `old`').fetchall()
            return result[-1][0]

    def get_rub(self):
        with self.connection:
            result = self.cursor.execute('SELECT `rub` FROM `old`').fetchall()
            return result[-1][0]

    def get_btc(self):
        with self.connection:
            result = self.cursor.execute('SELECT `btc` FROM `old`').fetchall()
            return result[-1][0]

    def set_curr(self, usd, eur, rub, btc, date):
        with self.connection:
            return self.cursor.execute('INSERT INTO `old` (`usd`, `eur`, `rub`, `btc`, `date`) VALUES(?,?,?,?,?)',
                                       (usd, eur, rub, btc, date))

    def test(self):
        with self.connection:
            result = self.cursor.execute('SELECT `usd` FROM `old` ').fetchall()
            return result[-1][0]

    # def get_subscriptions(self, status=True):
    #     """Получаем всех активных подписчиков бота"""
    #     with self.connection:
    #         return self.cursor.execute("SELECT * FROM `old` WHERE `status` = ?", (status,)).fetchall()

    # def subscriber_exists(self, user_id):
    #     """Проверяем, есть ли уже юзер в базе"""
    #     with self.connection:
    #         result = self.cursor.execute('SELECT * FROM `old` WHERE `user_id` = ?', (user_id,)).fetchall()
    #         return bool(len(result))
    #
    # def add_subscriber(self, usd, eur, rub, btc, date):
    #     """Добавляем нового подписчика"""
    #     with self.connection:
    #         return self.cursor.execute("INSERT INTO `old` (`USD`, `EUR`, `RUB`, `BTC`, `Date`) VALUES(?,?,?,?)",
    #                                    (usd, eur, rub, btc, date))
    #
    # def update_subscription(self, user_id, status):
    #     """Обновляем статус подписки пользователя"""
    #     with self.connection:
    #         return self.cursor.execute("UPDATE `old` SET `status` = ? WHERE `user_id` = ?", (status, user_id))