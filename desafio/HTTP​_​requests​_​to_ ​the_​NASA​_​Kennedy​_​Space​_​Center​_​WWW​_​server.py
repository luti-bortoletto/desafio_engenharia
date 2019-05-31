#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark.sql import Row    
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import *
from pyspark.sql.types import *
import sys
import re


conf = SparkConf().setAppName("Log Analyzer SQL").setAll([('spark.executor.memory', '2g'), ('spark.executor.cores', '1'), ('spark.cores.max', '1'), ('spark.driver.memory','2g')])
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

def parse_apache_log_line(APACHE_ACCESS_LOG_PATTERN,logline):
   match = re.search(APACHE_ACCESS_LOG_PATTERN, logline)
   
    
   return match.group(1)+'$'+(match.group(4)).split(":", 1)[0]+'$'+(match.group(4)).split(":", 1)[1]+'$'+match.group(5)+'$'+match.group(6)+'$'+match.group(7)


APACHE_ACCESS_LOG_PATTERN = '^(\S+) (\S+) (\S+) \[([\w:/]+)\s[+\-]\S+\] "([\S ]+)" (\S+) (\S+)'

logFile = '/home/luciana/Downloads/logs/'

access_logs = sc.textFile(logFile).collect()


# In[3]:


correto=[]
for i in access_logs:
    result = re.match(APACHE_ACCESS_LOG_PATTERN, i)
    if result:
        cor=parse_apache_log_line(APACHE_ACCESS_LOG_PATTERN,i)
        correto.append(cor.split('$'))
    else:
        pass


# In[4]:


df = sc.parallelize(correto).toDF(["ip_address","date", "time", "protocol", "response_code", "content_size"])


# In[5]:


df.createOrReplaceTempView('logs')


# In[6]:


sqlContext.sql("SELECT * FROM logs").show()


# In[7]:

#1. Número​ ​de​ ​hosts​ ​únicos.
sqlContext.sql("SELECT count(distinct ip_address) FROM logs").show()


# In[8]:

#2. O​ ​total​ ​de​ ​erros​ ​404.
sqlContext.sql("SELECT count(*) FROM logs where response_code ='404'").show()


# In[9]:

#3. Os​ ​5​ ​URLs​ ​que​ ​mais​ ​causaram​ ​erro​ ​404.
sqlContext.sql("SELECT ip_address,count(*) as erros FROM logs where response_code ='404' group by ip_address order by count(*) desc limit 5").show()


# In[11]:

#4. Quantidade​ ​de​ ​erros​ ​404​ ​por​ ​dia.
sqlContext.sql("SELECT date,count(*) FROM logs where response_code ='404' group by date").show(40)


# In[12]:

#5. O​ ​total​ ​de​ ​bytes​ ​retornados.
sqlContext.sql("SELECT sum(content_size) FROM logs").show()


# In[ ]:




