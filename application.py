from flask import Flask, jsonify
import pyodbc
app = Flask(__name__)
# Azure SQL Server connection details
server = 'ib-azure-sql.database.windows.net'
database = 'ImperialBrands'
username = 'sqladmin'
password = 'Admin#123'
driver = 'ODBC Driver 17 for SQL Server'

# API endpoint for executing the SQL query
@app.route('/query', methods=['GET'])
def execute_query():
    try:
        print("Testing 1")
        query = 'Select sf.sales_force_person_name, sf.sales_force_person_id,sf.outlet_id,dt.sales_line_info, dt.area_code, dt.customer_address,ff.outlet_address, ff.customer_number, ff.area_code from dbo.sales_force_outlet_mapping_en sf, dbo.ff_dashboard_outlet_mapping_en ff, dbo.distribution_tracking_en dt where sf.outlet_id = ff.outlet_ID and sf.outlet_id = dt.outlet_ID and  sf.sales_force_person_id =10001 group by sf.outlet_id, sf.sales_force_person_id, sf.sales_force_person_name, dt.sales_line_info, dt.area_code, dt.customer_address,ff.outlet_address, ff.customer_number, ff.area_code' 
        # Establish the database connection
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        print("Testing 2")
        cursor = conn.cursor()

        # Execute the SQL query
        print("Testing 3")
        cursor.execute(query)

        # Fetch all rows from the query result
        rows = cursor.fetchall()

        # Convert the rows to a list of dictionaries
        print("Testing 4")
        result = []
        columns = [column[0] for column in cursor.description]  # Get column names
        for row in rows:
            result.append(dict(zip(columns, row)))

        # Close the database connection
        print(result)
        cursor.close()
        conn.close()

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True,port=8888,use_reloader=False)

