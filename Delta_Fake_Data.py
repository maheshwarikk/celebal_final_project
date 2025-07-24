# Databricks notebook source
# MAGIC %pip install faker

# COMMAND ----------

from faker import Faker
import pandas as pd

fake = Faker()
data = [{
    "Name": fake.name(),
    "Address": fake.address(),
    "Email": fake.email()
} for _ in range(10)]

df = pd.DataFrame(data)
df_spark = spark.createDataFrame(df)
df_spark.show()

# COMMAND ----------

delta_path = "/tmp/fake_data_delta"

# COMMAND ----------

# Save as a Delta Table (managed table)
df_spark.write.format("delta").mode("overwrite").saveAsTable("fake_data_delta")

# COMMAND ----------

from delta.tables import DeltaTable

delta_table = DeltaTable.forName(spark, "fake_data_delta")
delta_table.toDF().show(truncate=False)

# COMMAND ----------

df_spark.write.format("delta").mode("append").saveAsTable("fake_data_delta")

# COMMAND ----------

from delta.tables import DeltaTable

# Load the Delta Table
delta_table = DeltaTable.forName(spark, "fake_data_delta")

# Show latest contents
delta_table.toDF().show(truncate=False)

# COMMAND ----------

from faker import Faker
import pandas as pd
from datetime import datetime
from pyspark.sql.functions import current_timestamp

fake = Faker()

def append_fake_data(n_rows=5):
    data = [{
        "Name": fake.name(),
        "Address": fake.address(),
        "Email": fake.email()
    } for _ in range(n_rows)]

    df = pd.DataFrame(data)
    df_spark = spark.createDataFrame(df)

    # ✅ Safe way: Only add Inserted_Timestamp if not already present
    if "Inserted_Timestamp" not in df_spark.columns:
        df_spark = df_spark.withColumn("Inserted_Timestamp", current_timestamp())

    # Append to Delta Table
    df_spark.write.format("delta").mode("append").saveAsTable("fake_data_delta")
    print(f"{n_rows} fake rows appended at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# COMMAND ----------

# Show current Delta table schema
delta_table.toDF().printSchema()

# COMMAND ----------

from delta.tables import DeltaTable

delta_table = DeltaTable.forName(spark, "fake_data_delta")
delta_table.toDF().orderBy("Inserted_Timestamp", ascending=False).show(truncate=False)

# COMMAND ----------

spark.conf.set("spark.sql.session.timeZone", "Asia/Kolkata")

# COMMAND ----------

delta_table.history().select("version", "timestamp", "operation").show(truncate=False)

# COMMAND ----------

spark.read.format("delta").option("versionAsOf", 0).table("fake_data_delta").show(truncate=False)

# COMMAND ----------

delta_table.toDF().orderBy("Inserted_Timestamp", ascending=False).show(truncate=False)

# COMMAND ----------

# Step 1: Email config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "yamanrag.prakash@gmail.com"
receiver_email = "yamanrag.prakash@gmail.com"
app_password = "onux xfoi eklo thco"  # Gmail App Password

# Step 2: Email send function
def send_email(subject, html_table):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    body = f"""
    <html>
      <body>
        <h3>New Data Appended to Delta Table</h3>
        {html_table}
      </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("✅ Email sent!")
    except Exception as e:
        print("❌ Email failed:", e)

# Step 3: Get last 5 rows added & send email
new_rows = delta_table.toDF().orderBy("Inserted_Timestamp", ascending=False).limit(5)
html_table = new_rows.toPandas().to_html(index=False, escape=False)
send_email("Delta Append Notification", html_table)

# COMMAND ----------

from delta.tables import DeltaTable
delta_table = DeltaTable.forName(spark, "fake_data_delta")

# COMMAND ----------

# Show Delta Table version history
delta_table.history().show()

# COMMAND ----------

spark.conf.set("spark.sql.session.timeZone", "Asia/Kolkata")

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS fake_data_delta

# COMMAND ----------

from faker import Faker
import pandas as pd
from pyspark.sql.functions import current_timestamp

fake = Faker()

# Generate fake data
data = [{
    "Name": fake.name(),
    "Address": fake.address(),
    "Email": fake.email()
} for _ in range(5)]

df = pd.DataFrame(data)
df_spark = spark.createDataFrame(df)

# Add proper timestamp column
df_spark = df_spark.withColumn("Inserted_Timestamp", current_timestamp())

# Overwrite the table with correct schema
df_spark.write.format("delta").mode("overwrite").saveAsTable("fake_data_delta")

# COMMAND ----------

from datetime import datetime

def append_fake_data(n_rows=5):
    data = [{
        "Name": fake.name(),
        "Address": fake.address(),
        "Email": fake.email()
    } for _ in range(n_rows)]

    df = pd.DataFrame(data)
    df_spark = spark.createDataFrame(df)

    # Add timestamp only if not already present
    if "Inserted_Timestamp" not in df_spark.columns:
        df_spark = df_spark.withColumn("Inserted_Timestamp", current_timestamp())

    df_spark.write.format("delta").mode("append").saveAsTable("fake_data_delta")
    print(f"{n_rows} fake rows appended at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# COMMAND ----------

append_fake_data(5)

# COMMAND ----------

