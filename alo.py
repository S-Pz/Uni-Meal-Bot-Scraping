
To update existing rows in a table instead of inserting new rows every time, you'll need to modify your `insert_data` functions to check if a record with a matching key (like a unique identifier or primary key) already exists. If it does, update the existing record; if not, insert a new record.

Here’s a general approach on how you can modify your `insert_data` functions to achieve this:

### Step-by-Step Approach:

1. **Identify Unique Key**: Determine which column(s) or field(s) uniquely identify each record in your table. This is typically the primary key (`id` in your case).

2. **Modify SQL Statements**:
   - Use SQLite's `INSERT OR REPLACE` or `INSERT OR IGNORE` statements to handle insertion and updating in a single statement.
   - Construct SQL statements to check if a record with the same primary key exists (`WHERE id = ?`).
   - Depending on whether the record exists or not, perform an `INSERT` or `UPDATE` operation.

3. **Adjust Data Handling**:
   - Iterate through your DataFrame (`dF` in your functions).
   - For each record, construct parameters (`data`) for insertion or updating.
   - Execute the SQL statement accordingly.

Here's an example modification for one of your `insert_data` functions (`insert_data_CTAN`):

```python
def insert_data_CTAN(conn: sqlite3.Connection, dF: pd.DataFrame):
    c = conn.cursor()

    try:
        for index in dF.index:
            DATA = dF.loc[index, 'DATA']
            HORARIO = dF.loc[index, 'HORARIO']
            PRATOPRINCIPAL = dF.loc[index, 'PRATOPRINCIPAL']
            OVOS = dF.loc[index, 'OVOS']
            VEGETARIANO = dF.loc[index, 'VEGETARIANO']
            GUARNICAO = dF.loc[index, 'GUARNICAO']
            ARROZ = dF.loc[index, 'ARROZ']
            FEIJAO = dF.loc[index, 'FEIJAO']
            SALADA1 = dF.loc[index, 'SALADA1']
            SALADA2 = dF.loc[index, 'SALADA2']
            SUCO = dF.loc[index, 'SUCO']
            SOBREMESA = dF.loc[index, 'SOBREMESA']

            # Check if record exists based on a unique key (e.g., data and horario)
            c.execute("""
                SELECT id FROM CTAN WHERE data = ? AND horario = ?
            """, (DATA, HORARIO))
            existing_record = c.fetchone()

            if existing_record:
                # Update existing record
                c.execute("""
                    UPDATE CTAN SET pratoprincipal = ?, ovos = ?, vegetariano = ?,
                    guarnicao = ?, arroz = ?, feijao = ?, salada1 = ?, salada2 = ?,
                    suco = ?, sobremesa = ?
                    WHERE id = ?
                """, (PRATOPRINCIPAL, OVOS, VEGETARIANO, GUARNICAO, ARROZ, FEIJAO,
                      SALADA1, SALADA2, SUCO, SOBREMESA, existing_record[0]))
            else:
                # Insert new record
                c.execute("""
                    INSERT INTO CTAN (data, horario, pratoprincipal, ovos, vegetariano,
                    guarnicao, arroz, feijao, salada1, salada2, suco, sobremesa)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (DATA, HORARIO, PRATOPRINCIPAL, OVOS, VEGETARIANO, GUARNICAO,
                      ARROZ, FEIJAO, SALADA1, SALADA2, SUCO, SOBREMESA))

            conn.commit()

    except sqlite3.OperationalError as error:
        print("Error inserting or updating data in CTAN table:", error)

    finally:
        c.close()
```

### Explanation:

- **SQL Statements**: 
  - `SELECT`: Checks if a record with the same `data` and `horario` already exists.
  - `UPDATE`: If a record exists (`existing_record` is not `None`), update the existing record with new values.
  - `INSERT`: If no record exists (`existing_record` is `None`), insert a new record.

- **Handling Data**: 
  - Fetch values from `dF` DataFrame for each iteration.
  - Construct `data` tuple for SQL execution.

- **Error Handling**: 
  - Catch and print any `OperationalError` that occurs during SQL execution.

### Usage:

You would modify the other `insert_data` functions (`insert_data_CSA`, `insert_data_CSL`, etc.) similarly, adjusting table names and columns as necessary.

This approach ensures that your tables are updated with new data when available, and existing data is appropriately updated rather than duplicated. Adjust the unique key (`WHERE` clause in `SELECT` statement) based on your specific database schema and requirements.