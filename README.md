# Query-Excecution-Process

python3.7
https://www.python.org/downloads/

PostgreSQL
https://www.postgresql.org/download/

Database Ensure that tpc-h data is loaded into the database. For this project we assume that user has uploaded tcp-h dataset to their local database.
http://tpc.org/tpc_documents_current_versions/download_programs/tools-download-request5.asp?bm_type=TPC-H&bm_vers=3.0.0&mode=CURRENT-ONLY

Download packages:
pip install -r /path/to/requirements.txt

To run interface:
On terminal navigate to this folder, run:  streamlit run project.py
The GUI will be displayed in your local url.

After accessing the GUI, specify database name, postgres server username, postgres server password, host, port, on the sidebar's white boxes according to the title.
By default, host and port is localhost and 5432 respectively if it is not specified.

If Authentication is successful "Connection successful" will shown the top of the GUI otherwise it will dsiplay "Unable to connect".

You can click the example buttons to run our preset queries, or type your own queries in the textbox. 

For all textbox that are to be filled up simply press enter and the input will be applied.


