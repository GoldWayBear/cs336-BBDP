
import mysql.connector

import json
import time
import ssl
import sy


Create Assertion NoRipoffBars Check(
  Not Exists(
    Select bar From Sells
    Group By bar
    Having 5.00 < avg(Price)
  )
)
