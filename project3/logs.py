#!/usr/bin/env python3
import psycopg2

# Query for finding the most popular three articles of all time
query1_text = ("1. Most popular three articles of all time:")
query1 = ("""
select articles.title, count(*) as views
from articles, log where log.status ='200 OK'
and log.path like '%' || articles.slug || '%'
group by articles.title
order by views desc limit 3
""")

# Query for inding the most popular article authors of all time
query2_text = ("2. Most popular article authors of all time:")
query2 = ("""
select authors.name, count(*) as views
from articles, authors, log
where log.status ='200 OK'
and articles.author = authors.id
and log.path like '%' || articles.slug || '%'
group by authors.name
order by views desc
""")

# Query for finidng which days did more than 1% of requests lead to errors
query3_text = ("3. Days did more than 1% of requests lead to errors:")
query3 = ("""
select oviews.day, round((oviews.stat / (nviews.stat + oviews.stat) *100.0)2)
from nviews, oviews
where (oviews.stat / (nviews.stat + oviews.stat) *100.0) >1.0
and oviews.day= nviews.day;
""")


# Function cnonnects to the news database
def connect():
    try:
        db = psycopg2.connect(dbname="news")
        cursor = db.cursor()
        return db, cursor
    except:
        print ("Can't connect to the database")


# Fucntion send the query to the database to excute it and get the results
def get(query):
    db, cursor = connect()
    results = cursor.execute(query)
    db.close()
    return results


# Function prints the results of the three quries
def printr(results, text, text1):
    print(text)
    if text1 == "articles" or text1 == "authors":
        for index in results:
            print(str(index[0]) + ' --- ' + str(index[1]) + ' views')
    else:
        for index in results:
            print(str(index[0]) + ' --- ' + str(index[1]) + ' %')


# Function main from where the program starts
def main():
    printr(get(query1), query1_text, "articles")
    printr(get(query2), query2_text, "authors")
    printr(get(query3), query3_text, "errors")


main()
