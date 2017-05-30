#Set up
##The following views were created
###top_three_paths
####in psql interpreter, run the create statement below before running the python program report.py
```sql
CREATE VIEW top_three_paths AS
SELECT path, COUNT(path) as times
FROM log
GROUP BY path
HAVING path != '/'
ORDER BY times DESC
LIMIT 3;
```

#Run report after setup
## in terminal
```python
python report.py
```

##If you'd like to revert the news database to its original form, you can do that by dropping each of the tables, then re-importing the data from the newsdata.sql file.

In psql:

drop table log;
drop table articles;
drop table authors;
Then in the shell, re-import the data:

psql -d news -f newsdata.sql