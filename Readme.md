# Logs Analysis Project

This project runs several queries on a news database and outputs answers to 3 questions on a txt file called report.txt. The questions answered are:
1. What are the most popular three articles of all time? 
2. Who are the most popular article authors of all time? 
3. On which days did more than 1% of requests lead to errors?

## Project Files ##
1. README.md
2. newsReports.py
3. newsdata.sql
4. report.txt

## Installation ##

1. You will need to install and run Linux-based virtual machine (VM)
2. Download all project files and store them in the vagrant directory
3. Log into VM using "vagrant ssh" command, change to vagrant directory
4. Type command "psql -d news -f newsdata.sql"
5. Type command "Create database newsdata.sql"
6. Type command "Create view badResponse as Select dateStamp, count(*) as badCount from (Select status::text as errorStamp, time::text::timestamp::date as dateStamp from log where status not like '%200%') as errorTable group by dateStamp order by dateStamp asc;"
7. Type command "Create view goodResponse as Select date2Stamp, count(*) as goodCount from (Select status::text as goodStamp, time::text::timestamp::date as date2Stamp from log where status like '%200%') as goodTable group by date2Stamp order by date2Stamp asc;"
8. Type "\q" to exit postgres command line
9. Run newsReports.py