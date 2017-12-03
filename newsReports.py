#!/usr/bin/python3

import psycopg2

DBNAME = 'news'
fileWriter = open('report.txt', 'w')


def firstQuestion():
    db = psycopg2.connect(dbname=DBNAME)

    c = db.cursor()

    firstQuery = ("select articles.title, count(*)"
                  " as num from articles inner"
                  " join log on log.path like"
                  " concat('%', articles.slug, '%')  where"
                  " log.status like '%200%' group by"
                  " articles.title, log.path order by"
                  " num desc limit 3")

    c.execute(firstQuery)

    results_table = c.fetchall()

    answer = ''

    for result in results_table:
        views = repr(result[1])
        str_views = views[:-1]
        answer += '"' + result[0] + '"' + '  --' + str_views + ' views\n'

    fileWriter.write("What are the most popular three articles of all time?\n")
    fileWriter.writelines(answer)

    # close connection
    db.close()


def secondQuestion():
    db = psycopg2.connect(dbname=DBNAME)

    c = db.cursor()

    secondQuery = ("Select authorName, CAST (SUM(num) AS FLOAT)"
                   " from (Select authors.name as authorName,"
                   " num from articles, authors,"
                   " (Select articles.slug as sluggy,"
                   " count(*) as num from articles"
                   " inner join log on log.path like"
                   " concat('%', articles.slug, '%')"
                   " where log.status like '%200%' group"
                   " by articles.slug, log.path order by"
                   " num desc) as foo where"
                   " articles.author=authors.id and"
                   " foo.sluggy = articles.slug) as"
                   " authorViews group by authorName"
                   " order by sum desc")

    c.execute(secondQuery)

    secondResults = c.fetchall()

    answer = ''

    for result in secondResults:
        strViews = repr(result[1])
        formatViews = strViews[:-2]
        answer += result[0] + '  --' + formatViews + ' views\n'

    # Print to text file
    fileWriter.write("\nWho are the"
                     " most popular article"
                     " authors of all time?\n")
    fileWriter.writelines(answer)

    # close connection
    db.close()


def thirdQuestion():
    db = psycopg2.connect(dbname=DBNAME)

    c = db.cursor()

    # query uses views goodResponse and badResponse
    # see Readme file for view create commands
    thirdQuery = ("Select dateStamp,"
                  " ((cast(badCount as float)"
                  " / cast(goodCount as float))*100)"
                  " as percentBad from goodResponse"
                  " inner join badResponse on"
                  " dateStamp=date2Stamp order"
                  " by percentBad desc")

    c.execute(thirdQuery)

    thirdResults = c.fetchone()

    answerDate = "{:%b %d, %Y}".format(thirdResults[0])

    answer = answerDate + " --" + '%.2f' % thirdResults[1] + '%% errors'

    fileWriter.write("\nOn which days did"
                     " more than 1% of requests"
                     " lead to errors?\n")
    fileWriter.writelines(answer)
    fileWriter.close()


# call to functions
firstQuestion()
secondQuestion()
thirdQuestion()
