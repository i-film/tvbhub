import MySQLdb

db = MySQLdb.connect('159.138.130.245', 'yc', 'wai25789', 'youtube')
cursor = db.cursor()

dns = {
    'vip.kuyun99.com': 'vip.let-kuyun.com',
    'video.fjhps.com': 'video.kkyun-iqiyi.com',
    'videos.fjhps.com': 'videos.kkyun-iqiyi.com'
}
select = 'SELECT * FROM VIDEOS WHERE LINK like "%{}%"'
update = 'UPDATE VIDEOS SET LINK = "{0}" WHERE ID = {1}'

for key in dns.keys():
    sql = select.format(key)
    cursor.execute(sql)
    # get all records in list
    results = cursor.fetchall()
    for row in results:
        movie_id = row[0]
        link = row[6]
        new_link = link.replace(key, dns.get(key))
        sql = update.format(new_link, movie_id)
        cursor.execute(sql)
        db.commit()

db.close()
