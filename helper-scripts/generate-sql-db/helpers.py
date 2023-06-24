import psycopg2

def upsert_array(cur, arg_array, num_of_args, column_string, conflict_string, update_set_string):
    arg_interpolated_string = "(" + ",".join("%s" for _ in range(num_of_args)) + ")"
    insert = "INSERT INTO abilities{} VALUES".format(column_string)
    args_str = ",".join(cur.mogrify(arg_interpolated_string, x).decode('utf-8') for x in arg_array)
    upsert = "ON CONFLICT {} DO UPDATE SET {};".format(conflict_string, update_set_string)

    sql_command = " ".join([insert, args_str, upsert])

    print(sql_command)

    try:
        cur.execute(sql_command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_and_upsert_all(cur, data_array, prep_function, upsert_function):
    prepped_data = []

    for data in data_array:
        prepped_data.append(prep_function(data))

        if len(prepped_data) == 999:
            upsert_function(cur, prepped_data)
            prepped_data = []

    if len(prepped_data) != 0:
        upsert_function(cur, prepped_data)