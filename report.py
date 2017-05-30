#! /usr/bin/env python
import psycopg2
import calendar


class Report(object):
    """Report of db"""
    dbname = "news"

    def get_top_three_articles(self):
        """show the top three articles"""
        query = """
            SELECT title, top_three_paths.times as times_requested
            FROM top_three_paths, articles
            WHERE path like '%' || slug || '%'
            ORDER BY times_requested desc;
        """
        conn = psycopg2.connect(database=self.dbname)
        cur = conn.cursor()
        cur.execute(query)
        for record in cur:
            print "%s -- %s views" % (record[0], record[1])
        cur.close()
        conn.close()
        return

    def get_most_popular_author(self):
        """Return the authors sorted by times they were viewed according to the log table"""
        query = """
            SELECT name, COUNT(path) as number_of_requests
            FROM articles, authors, log
            WHERE articles.author = authors.id and
            log.path = ('/article/' || articles.slug)
            GROUP BY name
            ORDER BY number_of_requests desc;
        """
        conn = psycopg2.connect(database=self.dbname)
        cur = conn.cursor()
        cur.execute(query)
        for record in cur:
            print "%s -- %s views" % (record[0], record[1])
        cur.close()
        conn.close()
        return

    def get_error_date(self):
        """Return dates when more than 1% of requests lead to errors"""
        query = """
            select to_char(date, 'FMMonth FMDD, YYYY'), err/total as ratio
            from (select time::date as date,
                        count(*) as total,
                        sum((status != '200 OK')::int)::float as err
                        from log
                        group by date) as errors
            where err/total > 0.01;
       """
        conn = psycopg2.connect(database=self.dbname)
        cur = conn.cursor()
        cur.execute(query)
        for record in cur:
            print "%s -- %.2f%% errors" % (record[0], record[1] * 100)
        cur.close()
        conn.close()
        return

report = Report()
print "###### Pringint top three articles ########"
report.get_top_three_articles()
print "###### Printing top authors ###############"
report.get_most_popular_author()
print "###### Printing days with more than 1% requests resulted in 404 Not Found Status"""
report.get_error_date()
