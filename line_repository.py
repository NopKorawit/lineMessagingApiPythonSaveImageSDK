from db.maria import create_connection

class TabLineRepository:
    def __init__(self):
        self.connection = create_connection()

    def select_all_line_oa(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"SELECT uuid,base_id,channel_secret,channel_access_token FROM tab_line_oa_secret")
        result = cursor.fetchall()
        cursor.close()
        return result