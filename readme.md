
# Autoplius.lt scraper with front-end.

This project is designed to scrape adverts from the "autoplius.lt" website and display them in a user-friendly front-end interface.




## Installation

1. Use pip to install the required packages listed in requirements.txt:
```bash
pip install -r requirements.txt
```

2. Add your database connection details to connectionsecret.py:
```bash
db_name = "postgresql://nickname:password@localhost:5432/databasename"

```

3. Add a secret key for security purposes to connectionsecret.py:
```bash
secret_key = "your_secret_key"
```

4. Create the necessary database tables by running the following command in your terminal:
```bash
uvicorn main:app --reload
```

5. Run the scraper to start collecting adverts:
```bash
python.exe scraper.py
```

6. Enter the autoplius.lt website link from which you want to scrape adverts. For example:
```bash
https://m.autoplius.lt/skelbimai/naudoti-automobiliai
```