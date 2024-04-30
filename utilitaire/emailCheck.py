from utilitaire import connect as Uconn

def test_mail(mail):
    connect = Uconn.connect_func()
    cursor = connect.cursor()
    sql = "SELECT email FROM users WHERE email = %s"
    cursor.execute(sql,(mail,))
    result = cursor.fetchone()
    if(result):
        return True
    else: 
        return False