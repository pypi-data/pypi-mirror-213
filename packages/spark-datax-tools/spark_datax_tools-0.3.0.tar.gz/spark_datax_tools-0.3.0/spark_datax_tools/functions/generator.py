def read_fields_datum(spark=None, path=None, table_name=None, storage_zone=None):
    from pyspark.sql import functions as func

    if str(storage_zone).upper() in ('RAW', 'RAWDATA'):
        storage_zone = 'RAWDATA'
    elif str(storage_zone).upper() in ('MASTER', 'MASTERDATA'):
        storage_zone = 'MASTERDATA'
    else:
        raise Exception(f'required var storage_zone in : "raw,rawdata,master, masterdata"')

    df = spark.read.csv(path, sep=';', header=True)
    df = df.select(*[func.col(c).alias(c.upper().replace(' ', '_').strip()) for c in df.columns]) \
        .dropDuplicates(["FIELD_ID"])
    df = df.select("FIELD_ID", "PHYSICAL_NAME_OBJECT", "PHYSICAL_NAME_FIELD", "SOURCE_FIELD",
                   "DATA_TYPE", "KEY", "FORMAT", "LOGICAL_FORMAT", "SECURITY_CLASS", "SECURITY_LABEL",
                   "MANDATORY", "FIELD_POSITION_IN_THE_OBJECT", "STORAGE_TYPE", "STORAGE_ZONE",
                   "NAME_DATA_SYSTEM", "PARTITION_COLUMN_IND")
    df = df.withColumn('FIELD_POSITION_IN_THE_OBJECT',
                       func.format_string("%03d", func.col('FIELD_POSITION_IN_THE_OBJECT').cast('int')))
    df = df[df["STORAGE_ZONE"].isin([storage_zone])]
    df = df[df["PHYSICAL_NAME_OBJECT"] == f"{table_name}"]

    df = df.orderBy(func.col("FIELD_POSITION_IN_THE_OBJECT").asc())
    return df


def read_ns(uuaa=None, is_dev=None):
    import pandas as pd
    import os
    from spark_datax_tools.utils import BASE_DIR
    from spark_datax_tools.utils.color import get_color_b

    ns_code = "dev" if is_dev else "pro"
    uuaa = str(uuaa).upper()
    dir_ns = os.path.join(BASE_DIR, "utils", "files", "ns.csv")
    df = pd.read_csv(dir_ns, sep="|")
    df2 = df[df["UUAA"] == f"{uuaa}"]
    if df2.shape[0] == 0:
        print(get_color_b("No existe uuaa registrada agregar manualmente el NS"))
        return None
    else:
        ns = df2.iloc[0]['NS']
        ns = f"pe-{uuaa.lower()}.app-id-{ns}.{ns_code}"
        return ns


def datax_list_adapters(output=True):
    """
    List Adapter Enabled
    :param output: Boolean
    :return:
    """

    from prettytable import PrettyTable
    from spark_datax_tools.utils.color import get_color_b

    list_adapter = ["ADAPTER_HDFS_OUTSTAGING",
                    "ADAPTER_HDFS_STAGING",
                    "ADAPTER_HDFS_MASTER",
                    "ADAPTER_GCS_LAUNCHPAD",
                    "ADAPTER_XCOM_OFICINAS",
                    "ADAPTER_CONNECTDIRECT_HOST",
                    "ADAPTER_CONNECTDIRECT_OPENPAY",
                    "ADAPTER_CONNECTDIRECT_SPECTRUM",
                    "ADAPTER_CONNECTDIRECT_PIC",
                    "ADAPTER_ORACLE_PERU"
                    ]

    if output:
        t = PrettyTable()
        t.field_names = ["LIST ADAPTER", "PARAMETERS"]
        t.add_row([get_color_b("ADAPTER_ID"), ""])
        t.add_row(["------------", ""])
        t.add_row(["ADAPTER_HDFS_OUTSTAGING", '{"uuaa":""}'])
        t.add_row(["ADAPTER_HDFS_STAGING", '{"uuaa":""}'])
        t.add_row(["ADAPTER_HDFS_MASTER", '{"uuaa":""}'])
        t.add_row(["ADAPTER_GCS_LAUNCHPAD", '{"uuaa":""}'])
        t.add_row(["ADAPTER_XCOM_OFICINAS", '{"uuaa":"","nro_oficina":""}'])
        t.add_row(["ADAPTER_CONNECTDIRECT_HOST", '{"uuaa":""}'])
        t.add_row(["ADAPTER_CONNECTDIRECT_OPENPAY", '{"uuaa":""}'])
        t.add_row(["ADAPTER_CONNECTDIRECT_SPECTRUM", '{"uuaa":""}'])
        t.add_row(["ADAPTER_CONNECTDIRECT_PIC", '{"uuaa":""}'])
        t.add_row(["ADAPTER_ORACLE_PERU", '{"uuaa":"","schema_oracle":""}'])
        print(t)
    else:
        return list_adapter


def generated_structure_ticket(origen=None, params=None, is_dev=True):
    from prettytable import PrettyTable
    from spark_datax_tools.utils.color import get_color_b, get_color_g

    env = "dev" if is_dev else "pro"

    if origen == "HDFS":
        uuaa = params.get("uuaa", "")
        adapter_id = params.get("adapter_id", "")
        ns = params.get("ns", "")
        connection_id = params.get("connection_id", "")
        adapter_description = params.get("adapter_description", "")
        tenant = params.get("tenant", "")
        basepath = params.get("basepath", "")

        t = PrettyTable()
        t.field_names = [get_color_b(f"{adapter_id}"), ""]
        t.add_row(["NS", f'{ns}'])
        t.add_row(["Adapter ID", f'{adapter_id}'])
        t.add_row(["Connection ID", f'{connection_id}'])
        t.add_row(["Adapter Description", f'{adapter_description}'])
        t.add_row(["Tenant", f'{tenant}'])
        t.add_row(["BasePath", f'{basepath}'])
        print(t)

        print("\n")
        print(get_color_g(f"########### TICKET JIRA DATAX {env.upper()} #############"))
        print(get_color_g("TITLE:"),
              get_color_b(f"[SD-XXXXXX] Creación de Adaptador en entorno {env.upper()} - {uuaa.upper()}"))
        print(get_color_g("DESCRIPTION:"))
        ticket = get_color_b("""
        ----
        Se solicita la creación del adaptador en DataX

        {color:#0747a6}*UUAA:*{color}  {key_uuaa}
        {color:#0747a6}*NS:*{color}  {key_ns}
        * {color:#0747a6}*Adapter ID:*{color}  {key_adapter_id}
        * {color:#0747a6}*Connection ID:*{color}   {key_connection_id}
        * {color:#0747a6}*Adapter description:*{color}  {key_adapter_description}
        * {color:#0747a6}*Datos de conexión:*{color}
        ** {color:#0747a6}*BasePath:*{color}  {key_basepath}
        ** {color:#0747a6}*Tenant:*{color}  {key_tenant}

        ----
        """)
        ticket = ticket.replace('{key_uuaa}', uuaa) \
            .replace('{key_ns}', ns) \
            .replace('{key_adapter_id}', adapter_id) \
            .replace('{key_connection_id}', connection_id) \
            .replace('{key_adapter_description}', adapter_description) \
            .replace('{key_basepath}', basepath) \
            .replace('{key_tenant}', tenant)
        print(ticket)

    elif origen == "GCS":
        uuaa = params.get("uuaa", "")
        ns = params.get("ns", "")
        connection_id = params.get("connection_id", "")
        adapter_id = params.get("adapter_id", "")
        adapter_description = params.get("adapter_description", "")
        bucket = params.get("bucket", "")
        project_id = params.get("project_id", "")

        t = PrettyTable()
        t.field_names = [get_color_b(f"{adapter_id}"), ""]
        t.add_row(["NS", f'{ns}'])
        t.add_row(["Adapter ID", f'{adapter_id}'])
        t.add_row(["Connection ID", f'{connection_id}'])
        t.add_row(["Adapter Description", f'{adapter_description}'])
        t.add_row(["Bucket", f'{bucket}'])
        t.add_row(["Project_ID", f'{project_id}'])
        print(t)

        print("\n")
        print(get_color_g(f"########### TICKET JIRA DATAX {env.upper()} #############"))
        print(get_color_g("TITLE:"),
              get_color_b(f"[SD-XXXXXX] Creación de Adaptador en entorno {env.upper()} - {uuaa.upper()}"))
        print(get_color_g("DESCRIPTION:"))
        ticket = get_color_b("""
        ----
        Se solicita la creación del adaptador en DataX

        {color:#0747a6}*UUAA:*{color}  {key_uuaa}
        {color:#0747a6}*NS:*{color}  {key_ns}
        * {color:#0747a6}*Adapter ID:*{color}  {key_adapter_id}
        * {color:#0747a6}*Connection ID:*{color}  {key_connection_id}
        * {color:#0747a6}*Adapter description:*{color}  {key_adapter_description}
        * {color:#0747a6}*Datos de conexión:*{color}
        ** {color:#0747a6}*Bucket:*{color}  {key_bucket}
        ** {color:#0747a6}*Project_ID:*{color}  {key_project_id}

        ----
        """)
        ticket = ticket.replace('{key_uuaa}', uuaa) \
            .replace('{key_ns}', ns) \
            .replace('{key_adapter_id}', adapter_id) \
            .replace('{key_connection_id}', connection_id) \
            .replace('{key_adapter_description}', adapter_description) \
            .replace('{key_bucket}', bucket) \
            .replace('{key_project_id}', project_id)
        print(ticket)

    elif origen == "XCOM":
        uuaa = params.get("uuaa", "")
        ns = params.get("ns", "")
        connection_id = params.get("connection_id", "")
        adapter_id = params.get("adapter_id", "")
        adapter_description = params.get("adapter_description", "")
        basepath = params.get("basepath", "")
        snode = params.get("snode", "")
        operating_system = params.get("operating_system", "")
        sport = params.get("sport", "")

        t = PrettyTable()
        t.field_names = [get_color_b(f"{adapter_id}"), ""]
        t.add_row(["NS", f'{ns}'])
        t.add_row(["Adapter ID", f'{adapter_id}'])
        t.add_row(["Connection ID", f'{connection_id}'])
        t.add_row(["Adapter Description", f'{adapter_description}'])
        t.add_row(["Basepath", f'{basepath}'])
        t.add_row(["Snode", f'{snode}'])
        t.add_row(["OperatingSystem", f'{operating_system}'])
        t.add_row(["Sport", f'{sport}'])
        t.add_row(["", ""])
        t.add_row([get_color_b("CREDENCIALES"), ""])
        t.add_row(["------------", f""])
        t.add_row(["user", 'Credencial lo agrega Team IPA'])
        t.add_row(["pass", 'Credencial lo agrega Team IPA'])
        print(t)

        print("\n")
        print(get_color_g(f"########### TICKET JIRA DATAX {env.upper()} #############"))
        print(get_color_g("TITLE:"),
              get_color_b(f"[SD-XXXXXX] Creación de Adaptador en entorno {env.upper()} - {uuaa.upper()}"))
        print(get_color_g("DESCRIPTION:"))
        ticket = get_color_b("""
        ----
        Se solicita la creación del adaptador en DataX

        {color:#0747a6}*UUAA:*{color}  {key_uuaa}
        {color:#0747a6}*NS:*{color}  {key_ns}
        * {color:#0747a6}*Adapter ID:*{color}  {key_adapter_id}
        * {color:#0747a6}*Connection ID:*{color}  {key_connection_id}
        * {color:#0747a6}*Adapter description:*{color}  {key_adapter_description}
        * {color:#0747a6}*Datos de conexión:*{color}
        ** {color:#0747a6}*Basepath:*{color}  {key_basepath}
        ** {color:#0747a6}*Snode:*{color}  {key_snode}
        ** {color:#0747a6}*OperatingSystem :*{color}  {key_operating_system}
        ** {color:#0747a6}*Sport:*{color}  {key_sport}

        * {color:#0747a6}*Credenciales:*{color}
        ** {color:#0747a6}*user:*{color}  "Credencial lo agrega Team IPA"
        ** {color:#0747a6}*pass:*{color}  "Credencial lo agrega Team IPA"

        ----
        """)
        ticket = ticket.replace('{key_uuaa}', uuaa) \
            .replace('{key_ns}', ns) \
            .replace('{key_adapter_id}', adapter_id) \
            .replace('{key_connection_id}', connection_id) \
            .replace('{key_adapter_description}', adapter_description) \
            .replace('{key_basepath}', basepath) \
            .replace('{key_snode}', snode) \
            .replace('{key_operating_system}', operating_system) \
            .replace('{key_sport}', sport)
        print(ticket)

    elif origen == "CONNECTDIRECT":
        uuaa = params.get("uuaa", "")
        ns = params.get("ns", "")
        connection_id = params.get("connection_id", "")
        adapter_id = params.get("adapter_id", "")
        adapter_description = params.get("adapter_description", "")
        basepath = params.get("basepath", "")
        snode = params.get("snode", "")
        operating_system = params.get("operating_system", "")
        sport = params.get("sport", "")
        user = params.get("user", "")
        password = params.get("password", "")

        t = PrettyTable()
        t.field_names = [get_color_b(f"{adapter_id}"), ""]
        t.add_row(["NS", f'{ns}'])
        t.add_row(["Adapter ID", f'{adapter_id}'])
        t.add_row(["Connection ID", f'{connection_id}'])
        t.add_row(["Adapter Description", f'{adapter_description}'])
        t.add_row(["Basepath", f'{basepath}'])
        t.add_row(["Snode", f'{snode}'])
        t.add_row(["OperatingSystem", f'{operating_system}'])
        t.add_row(["Sport", f'{sport}'])
        t.add_row(["", ""])
        t.add_row([get_color_b("CREDENCIALES"), ""])
        t.add_row(["------------", f""])
        t.add_row(["user", f'{user}'])
        t.add_row(["pass", f'{password}'])
        print(t)

        print("\n")
        print(get_color_g(f"########### TICKET JIRA DATAX {env.upper()} #############"))
        print(get_color_g("TITLE:"),
              get_color_b(f"[SD-XXXXXX] Creación de Adaptador en entorno {env.upper()} - {uuaa.upper()}"))
        print(get_color_g("DESCRIPTION:"))
        ticket = get_color_b("""
        ----
        Se solicita la creación del adaptador en DataX

        {color:#0747a6}*UUAA:*{color}  {key_uuaa}
        {color:#0747a6}*NS:*{color}  {key_ns}
        * {color:#0747a6}*Adapter ID:*{color}  {key_adapter_id}
        * {color:#0747a6}*Connection ID:*{color}  {key_connection_id}
        * {color:#0747a6}*Adapter description:*{color}  {key_adapter_description}
        * {color:#0747a6}*Datos de conexión:*{color}
        ** {color:#0747a6}*Basepath:*{color}  {key_basepath}
        ** {color:#0747a6}*Snode:*{color}  {key_snode}
        ** {color:#0747a6}*OperatingSystem :*{color}  {key_operating_system}
        ** {color:#0747a6}*Sport:*{color}  {key_sport}

        * {color:#0747a6}*Credenciales:*{color}
        ** {color:#0747a6}*user:*{color}  {key_user}
        ** {color:#0747a6}*pass:*{color}  {key_password}

        ----
        """)
        ticket = ticket.replace('{key_uuaa}', uuaa) \
            .replace('{key_ns}', ns) \
            .replace('{key_adapter_id}', adapter_id) \
            .replace('{key_connection_id}', connection_id) \
            .replace('{key_adapter_description}', adapter_description) \
            .replace('{key_basepath}', basepath) \
            .replace('{key_snode}', snode) \
            .replace('{key_operating_system}', operating_system) \
            .replace('{key_sport}', sport) \
            .replace('{key_user}', user) \
            .replace('{key_password}', password)
        print(ticket)

    elif origen == "ORACLE":
        uuaa = params.get("uuaa", "")
        ns = params.get("ns", "")
        connection_id = params.get("connection_id", "")
        adapter_id = params.get("adapter_id", "")
        adapter_description = params.get("adapter_description", "")
        host = params.get("host", "")
        port = params.get("port", "")
        service = params.get("service", "")
        user = params.get("user", "")
        password = params.get("password", "")

        t = PrettyTable()
        t.field_names = [get_color_b(f"{adapter_id}"), ""]
        t.add_row(["NS", f'{ns}'])
        t.add_row(["Adapter ID", f'{adapter_id}'])
        t.add_row(["Connection ID", f'{connection_id}'])
        t.add_row(["Adapter Description", f'{adapter_description}'])
        t.add_row(["Host", f'{host}'])
        t.add_row(["Port", f'{port}'])
        t.add_row(["Service", f'{service}'])
        t.add_row(["", ""])
        t.add_row([get_color_b("CREDENCIALES"), ""])
        t.add_row(["------------", f""])
        t.add_row(["user", f'{user}'])
        t.add_row(["pass", f'{password}'])
        print(t)

        print("\n")
        print(get_color_g(f"########### TICKET JIRA DATAX {env.upper()} #############"))
        print(get_color_g("TITLE:"),
              get_color_b(f"[SD-XXXXXX] Creación de Adaptador en entorno {env.upper()} - {uuaa.upper()}"))
        print(get_color_g("DESCRIPTION:"))
        ticket = get_color_b("""
        ----
        Se solicita la creación del adaptador en DataX

        {color:#0747a6}*UUAA:*{color}  {key_uuaa}
        {color:#0747a6}*NS:*{color}  {key_ns}
        * {color:#0747a6}*Adapter ID:*{color}  {key_adapter_id}
        * {color:#0747a6}*Connection ID:*{color}  {key_connection_id}
        * {color:#0747a6}*Adapter description:*{color}  {key_adapter_description}
        * {color:#0747a6}*Datos de conexión:*{color}
        ** {color:#0747a6}*Host:*{color}  {key_host}
        ** {color:#0747a6}*Port:*{color}  {key_port}
        ** {color:#0747a6}*Service :*{color}  {key_service}

        * {color:#0747a6}*Credenciales:*{color}
        ** {color:#0747a6}*user:*{color}  {key_user}
        ** {color:#0747a6}*pass:*{color}  {key_password}

        ----
        """)
        ticket = ticket.replace('{key_uuaa}', uuaa) \
            .replace('{key_ns}', ns) \
            .replace('{key_adapter_id}', adapter_id) \
            .replace('{key_connection_id}', connection_id) \
            .replace('{key_adapter_description}', adapter_description) \
            .replace('{key_host}', host) \
            .replace('{key_port}', port) \
            .replace('{key_service}', service) \
            .replace('{key_user}', user) \
            .replace('{key_password}', password)
        print(ticket)

    elif origen == "TRANSFER":

        table_name = params.get("table_name", "")
        origen = params.get("origen", "")
        destination = params.get("destination", "")
        folder = params.get("folder", "")
        job_name = params.get("job_name", "")
        periodicity = params.get("periodicity", "")
        hour = params.get("hour", "")
        weight = params.get("weight", "")
        crq = params.get("crq", "")
        uuaa = str(table_name.split("_")[1]).upper().strip()
        ns = read_ns(uuaa=uuaa, is_dev=is_dev)

        nomenclature = datax_generated_nomenclature(
            table_name=table_name, origen=origen, destination=destination, output=False)
        schema_in_id = nomenclature.get("schema_in_id")
        schema_out_id = nomenclature.get("schema_out_id")
        do_read_id = nomenclature.get("do_read_id")
        do_write_id = nomenclature.get("do_write_id")
        transfer_id = nomenclature.get("transfer_id")

        t = PrettyTable()
        t.field_names = [get_color_b(f"{transfer_id}"), ""]
        t.add_row(["NS", f'{ns}'])
        t.add_row(["", ""])
        t.add_row([get_color_b("SCHEMA"), ""])
        t.add_row(["------------", f""])
        t.add_row(["SCHEMA IN ID", f'{schema_in_id}'])
        t.add_row(["SCHEMA OUT ID", f'{schema_out_id}'])
        t.add_row(["", ""])
        t.add_row([get_color_b("DATA-OBJECT"), ""])
        t.add_row(["------------", f""])
        t.add_row(["DO Read ID", f'{do_read_id}'])
        t.add_row(["DO Write ID", f'{do_write_id}'])
        t.add_row(["", ""])
        t.add_row([get_color_b("TRANSFER"), ""])
        t.add_row(["------------", f""])
        t.add_row(["Transfer ID", f'{transfer_id}'])
        t.add_row(["", ""])
        t.add_row(["Folder", f'{folder}'])
        t.add_row(["Job Name", f'{job_name}'])
        t.add_row(["Periodicity", f'{periodicity}'])
        t.add_row(["Hora", f'{hour}'])
        t.add_row(["Peso", f'{weight}'])
        t.add_row(["CRQ", f'{crq}'])
        print(t)

        print("\n")
        print(get_color_g(f"########### TICKET JIRA DATAX {env.upper()} #############"))
        print(get_color_g("TITLE:"),
              get_color_b(f"[SD-XXXXXX] Creación de Promoción en entorno {env.upper()} - {uuaa.upper()}"))
        print(get_color_g("DESCRIPTION:"))
        ticket = get_color_b("""
            ----
            Se solicita el despliegue en Live de los siguientes componentes de DataX

            {color:#0747a6}*UUAA:*{color} {key_uuaa}
            {color:#0747a6}*NS:*{color}  {key_ns}
            * {color:#0747a6}*Schema_ID:*{color}
            ** {color:#0747a6}{key_schema_in}{color}
            ** {color:#0747a6}{key_schema_out}{color}

            * {color:#0747a6}*DO_ID:*{color} 
            ** {color:#0747a6}{key_do_in}{color}
            ** {color:#0747a6}{key_do_out}{color}

            * {color:#0747a6}*Transfer_ID:*{color}  {key_transfer_id}
            ** {color:#0747a6}*Folder Control-M:*{color} {key_folder}
            ** {color:#0747a6}*JOB:*{color}  {key_job}
            ** {color:#0747a6}*PERIODICIDAD:*{color}  {key_periodicity}
            ** {color:#0747a6}*HORA:*{color}  {key_hour}
            ** {color:#0747a6}*PESO:*{color}  {key_Weight}
            ** {color:#0747a6}*ORIGEN:*{color}  {key_origen}
            ** {color:#0747a6}*DESTINO:*{color}  {key_destination}
            ** {color:#0747a6}*CRQ:*{color}  {key_crq}

            {color:#0747a6}*Motivo modificación:*{color}  Promoción de transferencia
            ----
            """)
        ticket = ticket.replace('{key_uuaa}', uuaa) \
            .replace('{key_schema_in}', schema_in_id) \
            .replace('{key_schema_out}', schema_out_id) \
            .replace('{key_do_in}', do_read_id) \
            .replace('{key_do_out}', do_write_id) \
            .replace('{key_transfer_id}', transfer_id) \
            .replace('{key_folder}', folder) \
            .replace('{key_job}', job_name) \
            .replace('{key_periodicity}', periodicity) \
            .replace('{key_hour}', hour) \
            .replace('{key_weight}', weight) \
            .replace('{key_origen}', origen) \
            .replace('{key_destination}', destination) \
            .replace('{key_crq}', crq)
        print(ticket)


def generated_schema_in_out(df=None,
                            table_name=None,
                            schema_name=None,
                            convert_string=False):
    import os
    import json
    from spark_datax_tools.utils.utils import get_reformat_dtype

    uuaa = str(table_name.split("_")[1]).upper().strip()
    rs_dict = dict()
    for row in df.collect():
        table = str(row['PHYSICAL_NAME_OBJECT']).lower().strip()
        naming = str(row['PHYSICAL_NAME_FIELD']).lower().strip()
        _format = row['LOGICAL_FORMAT']
        _mandatory = True if str(row['MANDATORY']).upper() == "YES" else False
        _format, _mask, _locale, _type, _schema_type = get_reformat_dtype(
            columns=naming, format=_format, convert_string=convert_string)

        if table not in rs_dict.keys():
            rs_dict[table] = dict(_id="", description="", fields=list())
        rs_dict[table]["_id"] = schema_name
        rs_dict[table]["description"] = ""
        fields_dict = dict()
        fields_dict["name"] = naming
        fields_dict["logicalFormat"] = _format
        fields_dict["deleted"] = False
        fields_dict["metadata"] = False
        fields_dict["default"] = ""
        fields_dict["mask"] = _mask
        fields_dict["locale"] = _locale
        fields_dict["mandatory"] = _mandatory
        rs_dict[table]["fields"].append(fields_dict)

    path_directory = os.path.join('schema_datax', uuaa, table_name)
    path_filename = os.path.join(path_directory, f"{schema_name}.json")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    with open(path_filename, 'w') as f:
        json.dump(rs_dict[f"{table_name}"], f, indent=4)
    print(f'create file for schema: {schema_name}.json')


def datax_generated_nomenclature(table_name, origen, destination, output=True):
    """
    Create the datax nomenclatures
    :param table_name: String
    :param origen: String
    :param destination: String
    :param output: Boolean
    :return:
    """
    from prettytable import PrettyTable
    from spark_datax_tools.utils.color import get_color_b

    if table_name in ("", None):
        raise Exception(f'required variable table_name')
    if origen in ("", None):
        raise Exception(f'required variable origen')
    if destination in ("", None):
        raise Exception(f'required variable destination')
    if output in ("", None):
        raise Exception(f'required variable output value True or False')

    uuaa = str(str(table_name).lower().split("_")[1])
    table_short = "".join(table_name.split("_")[2:])

    transfer_id = "p{uuaa}_{origen}{destination}{table_short}_0".format(
        uuaa=uuaa, origen=origen, destination=destination, table_short=table_short)
    schema_in_id = "x_schema_{origen}{table_short}_in_0".format(
        origen=origen, table_short=table_short)
    schema_out_id = "x_schema_{destination}{table_short}_out_0".format(
        destination=destination, table_short=table_short)
    do_read_id = "x_read{origen}{table_short}_0".format(
        origen=origen, table_short=table_short)
    do_write_id = "x_write{destination}{table_short}_0".format(
        destination=destination, table_short=table_short)

    if output:
        t = PrettyTable()
        t.field_names = [f"GENERATED NOMENCLATURE", "", ]
        t.add_row([get_color_b("TRANSFER"), ""])
        t.add_row(["------------", f""])
        t.add_row([get_color_b("Transfer ID"), f"{transfer_id}"])
        t.add_row(["", ""])
        t.add_row(["", ""])
        t.add_row([get_color_b("DATA-OBJECT "), ""])
        t.add_row(["------------", f""])
        t.add_row([get_color_b("DataObject Read ID"), f"{do_read_id}"])
        t.add_row([get_color_b("DataObject Write ID"), f"{do_write_id}"])
        t.add_row(["", ""])
        t.add_row(["", ""])
        t.add_row(["------------", f""])
        t.add_row([get_color_b("SCHEMA"), ""])
        t.add_row(["------------", f""])
        t.add_row([get_color_b("Schema IN"), f"{schema_in_id}"])
        t.add_row([get_color_b("Schema OUT"), f"{schema_out_id}"])
        t.add_row(["------------", f""])
        print(t)
    else:
        result = dict(transfer_id=transfer_id,
                      schema_in_id=schema_in_id,
                      schema_out_id=schema_out_id,
                      do_read_id=do_read_id,
                      do_write_id=do_write_id)
        return result


def datax_generated_schema_datum(spark=None,
                                 path=None,
                                 table_name=None,
                                 origen=None,
                                 destination=None,
                                 storage_zone=None,
                                 convert_string=False):
    """
    Generated schema datum
    :param spark: Object Spark
    :param path: String
    :param table_name: String
    :param origen: String
    :param destination: String
    :param storage_zone: String
    :param convert_string: Boolean
    :return:
    """

    from spark_datax_tools.utils.color import get_color_b

    if spark in ("", None):
        raise Exception(f'required variable spark')
    if path in ("", None):
        raise Exception(f'required variable path')
    if table_name in ("", None):
        raise Exception(f'required variable table_name')
    if origen in ("", None):
        raise Exception(f'required variable origen  value is hdfs,host,gcs,xcom')
    if destination in ("", None):
        raise Exception(f'required variable destination  value is hdfs,host,gcs,xcom')
    if storage_zone in ("", None):
        raise Exception(f'required variable storage_zone  value is raw or master')
    if convert_string in ("", None):
        raise Exception(f'required variable convert_string  value is True or False')

    table_name = str(table_name).lower()
    origen = str(origen).lower()
    destination = str(destination).lower()
    storage_zone = str(storage_zone).upper()

    df = read_fields_datum(
        spark=spark, path=path, table_name=table_name, storage_zone=storage_zone)
    if df.rdd.isEmpty():
        print(get_color_b(f'There are no values for this table: {table_name}'))
    else:
        print(get_color_b(f'GENERATED NOMENCLATURE: {table_name}'))
        nomenclature = datax_generated_nomenclature(
            table_name=table_name, origen=origen, destination=destination, output=False)
        schema_in = nomenclature.get("schema_in_id")
        schema_out = nomenclature.get("schema_out_id")

        print(get_color_b(f'GENERATED SCHEMA: {table_name}'))
        generated_schema_in_out(df=df,
                                table_name=table_name,
                                schema_name=schema_in,
                                convert_string=convert_string)

        generated_schema_in_out(df=df,
                                table_name=table_name,
                                schema_name=schema_out,
                                convert_string=convert_string)


def datax_generated_schema_artifactory(path_json=None,
                                       is_schema_origen_in=True,
                                       schema_type=None,
                                       convert_string=False):
    """
    Generated schema artifactory
    :param path_json: String
    :param is_schema_origen_in: Boolean
    :param schema_type: String
    :param convert_string: Boolean
    :return:
    """
    import json
    import os
    from spark_datax_tools.utils.utils import get_reformat_dtype
    from spark_datax_tools.utils.color import get_color_b

    if path_json in ("", None):
        raise Exception(f'required variable path_json')
    if is_schema_origen_in in ("", None):
        raise Exception(f'required variable is_schema_origen_in value is True or False')
    if schema_type in ("", None):
        raise Exception(f'required variable schema_type value is hdfs,host,gcs,xcom')
    if convert_string in ("", None):
        raise Exception(f'required variable convert_string value is hdfs,host,gcs,xcom')

    schema_type = str(schema_type).lower()

    dataset_json = path_json
    with open(dataset_json) as f:
        datax = json.load(f)
    table_name = table = datax.get("name", "")
    uuaa = str(table_name.split("_")[1]).upper().strip()
    table_short = "".join(table_name.split("_")[2:])
    description = datax.get("description", "")

    if is_schema_origen_in:
        schema_name = "x_schema_{schema_type}{table_short}_in_0".format(
            schema_type=schema_type, table_short=table_short)
    else:
        schema_name = "x_schema_{schema_type}{table_short}_out_0".format(
            schema_type=schema_type, table_short=table_short)

    rs_dict = dict()
    for field in datax["fields"]:
        naming = field.get("name", "")
        _format = field.get("logicalFormat", "")
        _format, _mask, _locale, _type, _schema_type = get_reformat_dtype(
            columns=naming, format=_format, convert_string=convert_string)
        if table not in rs_dict.keys():
            rs_dict[table] = dict(_id="", description="", fields=list())
        rs_dict[table]["_id"] = schema_name
        rs_dict[table]["description"] = description
        fields_dict = dict()
        fields_dict["name"] = naming
        fields_dict["logicalFormat"] = _format
        fields_dict["deleted"] = False
        fields_dict["metadata"] = False
        fields_dict["default"] = ""
        fields_dict["mask"] = _mask
        fields_dict["locale"] = _locale
        fields_dict["mandatory"] = False
        rs_dict[table]["fields"].append(fields_dict)

    path_directory = os.path.join('schema_artifactory', uuaa, table_name)
    path_filename = os.path.join(path_directory, f"{schema_name}.json")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    with open(path_filename, 'w') as f:
        json.dump(rs_dict[f"{table_name}"], f, indent=4)
    print(get_color_b(f'GENERATED SCHEMA: {table_name}'))
    print(f'create file for schema: {schema_name}.json')


def datax_generated_ticket_transfer(table_name=None, folder=None, job_name=None,
                                    crq=None, periodicity=None, hour=None, weight=None,
                                    origen=None, destination=None, is_dev=None):
    """
     Generated a Ticket Transfer
     :param table_name: String
     :param folder: String
     :param job_name: String
     :param crq: String
     :param periodicity: String
     :param hour: String
     :param weight: String
     :param origen: String
     :param destination: String
     :param is_dev: Boolean
     :return:
     """

    if table_name in ("", None):
        raise Exception(f'required variable table_name')
    if folder in ("", None):
        raise Exception(f'required variable folder')
    if job_name in ("", None):
        raise Exception(f'required variable job_name')
    if crq in ("", None):
        raise Exception(f'required variable crq')
    if periodicity in ("", None):
        raise Exception(f'required variable periodicity')
    if hour in ("", None):
        raise Exception(f'required variable hour')
    if weight in ("", None):
        raise Exception(f'required variable weight')
    if origen in ("", None):
        raise Exception(f'required variable origen value is hdfs,host,gcs,xcom')
    if destination in ("", None):
        raise Exception(f'required variable destination value is hdfs,host,gcs,xcom')
    if is_dev in ("", None):
        raise Exception(f'required variable is_dev value is True or False')

    params = dict(table_name=table_name,
                  folder=folder,
                  job_name=job_name,
                  crq=crq,
                  periodicity=periodicity,
                  hour=hour,
                  weight=weight,
                  origen=origen,
                  destination=destination
                  )
    generated_structure_ticket(origen="TRANSFER", params=params, is_dev=is_dev)


def datax_generated_ticket_adapter(adapter_id=None, parameter={}, is_dev=True):
    """
    Generated a Ticket Adapter
    :param adapter_id: String
    :param parameter: dict
    :param is_dev: Boolean
    :return:
    """

    from spark_datax_tools.utils.color import get_color_b

    if adapter_id in ("", None):
        raise Exception(f'required variable adapter_id')
    if parameter in ("", None):
        raise Exception(f'required variable parameter')
    if is_dev in ("", None):
        raise Exception(f'required variable is_dev value is True or False')

    list_adapter = datax_list_adapters(output=False)
    if adapter_id not in list_adapter:
        print(get_color_b("The adapter_id not exist"))
    else:
        type_adapter = str(adapter_id.split("_")[1]).lower()
        name_adapter = str(adapter_id.split("_")[2]).lower()

        if type_adapter.upper() == "HDFS":
            if 'uuaa' not in parameter.keys():
                print(get_color_b("required parameters uuaa"))
            else:
                env = "dev" if is_dev else "pro"
                uuaa = parameter.get("uuaa")
                ns = read_ns(uuaa=uuaa, is_dev=is_dev)
                adapter_id = f"adapter-hdfs{name_adapter}-{uuaa.lower()}"
                connection_id = f"con-pe-adapter-hdfs{name_adapter}-{uuaa.lower()}-{env}"
                tenant = "PE"
                basepath = ""
                adapter_description = ""
                if name_adapter.upper() == "OUTSTAGING":
                    basepath = f"/out/staging/ratransmit/{uuaa.lower()}"
                    adapter_description = f"Adapter HDFS in UUAA {uuaa.upper()} OutStaging Zone in {env}"
                elif name_adapter.upper() == "STAGING":
                    basepath = f"/in/staging/datax/{uuaa.lower()}"
                    adapter_description = f"Adapter HDFS in UUAA {uuaa.upper()} Staging Zone in {env}"
                elif name_adapter.upper() == "MASTER":
                    basepath = f"/data/master/{uuaa.lower()}/data"
                    adapter_description = f"Adapter HDFS in UUAA {uuaa.upper()} Master Zone in {env}"

                params = dict(uuaa=uuaa, ns=ns, adapter_id=adapter_id,
                              connection_id=connection_id,
                              adapter_description=adapter_description,
                              tenant=tenant, basepath=basepath)
                generated_structure_ticket(origen="HDFS", params=params, is_dev=is_dev)

        elif type_adapter.upper() == "GCS":
            if 'uuaa' not in parameter.keys():
                print(get_color_b("required parameters uuaa"))
            else:
                env = "dev" if is_dev else "pro"
                uuaa = parameter.get("uuaa")
                ns = read_ns(uuaa=uuaa, is_dev=is_dev)
                adapter_id = f"adapter-gcslaunchpad-{uuaa.lower()}"
                connection_id = f"con-pe-adapter-gcslaunchpad-{uuaa.lower()}-{env}"
                adapter_description = f"Adapter GCS in UUAA {uuaa.upper()} in {env}"
                bucket = "dev-bbva-launchpad-sp-out_per" if is_dev else "bbva-launchpad-sp-out_per"
                project_id = "dev-bbva-launchpad-sp" if is_dev else "bbva-launchpad-sp"

                parameters = dict(uuaa=uuaa, ns=ns, adapter_id=adapter_id,
                                  connection_id=connection_id,
                                  adapter_description=adapter_description,
                                  bucket=bucket, project_id=project_id)
                generated_structure_ticket(origen="GCS", params=parameters, is_dev=is_dev)

        elif type_adapter.upper() == "XCOM":
            if 'uuaa' not in parameter.keys():
                print(get_color_b("required parameters uuaa"))
            if 'nro_oficina' not in parameter.keys():
                print(get_color_b("required parameters nro_oficina"))
            else:
                env = "dev" if is_dev else "pro"
                uuaa = parameter.get("uuaa")
                nro_oficina = parameter.get("nro_oficina")
                ns = read_ns(uuaa=uuaa, is_dev=is_dev)
                adapter_id = f"adapter-xcom-{uuaa.lower()}of{nro_oficina.lower()}"
                connection_id = f"con-pe-adapter-xcom-{uuaa.lower()}of{nro_oficina.lower()}-{env}"
                adapter_description = f"Adapter to access OF{nro_oficina.upper()} xcom files in {env}"
                basepath = f"/BBVA/S7729600VM/xcomntip/OF_{nro_oficina.upper()}"
                snode = "118.180.60.121"
                operating_system = "Unix"
                sport = "1364"
                user = "Credencial lo agrega Team IPA"
                password = "Credencial lo agrega Team IPA"
                parameters = dict(uuaa=uuaa, ns=ns, adapter_id=adapter_id,
                                  connection_id=connection_id,
                                  adapter_description=adapter_description,
                                  basepath=basepath, snode=snode,
                                  operating_system=operating_system, sport=sport,
                                  user=user, password=password)
                generated_structure_ticket(origen="XCOM", params=parameters, is_dev=is_dev)

        elif type_adapter.upper() == "CONNECTDIRECT":
            if 'uuaa' not in parameter.keys():
                print(get_color_b("required parameters uuaa"))
            else:
                env = "dev" if is_dev else "pro"
                uuaa = parameter.get("uuaa")
                ns = read_ns(uuaa=uuaa, is_dev=is_dev)
                adapter_id = f"adapter-connectdirectunix{name_adapter.lower()}-{uuaa.lower()}"
                connection_id = f"con-pe-adapter-connectdirectunix{name_adapter.lower()}-{uuaa.lower()}-{env}"
                adapter_description = f"Adapter to access {uuaa.upper()} connectdirectunix{name_adapter.lower()} files in {env}"
                basepath = ""
                snode = ""
                operating_system = ""
                sport = ""
                user = ""
                password = ""

                if name_adapter.upper() == "HOST":
                    basepath = "PEBD" if is_dev else "PEBP"
                    snode = "150.250.40.145" if is_dev else "150.250.40.21"
                    operating_system = "zos"
                    sport = "1364"
                    user = "Credencial lo agrega Team CyberSeguridad (Raul Salazar)"
                    password = "Credencial lo agrega Team CyberSeguridad  (Raul Salazar)"
                elif name_adapter.upper() == "OPENPAY":
                    basepath = "/mailbox/padq/openpay"
                    snode = "118.180.34.70" if is_dev else "118.180.54.113"
                    operating_system = "unix"
                    sport = "2364"
                    user = "usrdatax"
                    password = "u9m62sv" if is_dev else "d039jo0"
                elif name_adapter.upper() == "SPECTRUM":
                    basepath = "/BBVA/PWAPBDVTRUM01"
                    snode = "118.180.60.121"
                    operating_system = "unix"
                    sport = "1364"
                    user = "Credencial lo agrega Team IPA"
                    password = "Credencial lo agrega Team IPA"
                elif name_adapter.upper() == "PIC":
                    basepath = "/filespic/out"
                    snode = "150.250.242.60"
                    operating_system = "unix"
                    sport = "1364"
                    user = "zcapicpe"
                    password = "yajEl512"

                parameters = dict(uuaa=uuaa, ns=ns, adapter_id=adapter_id,
                                  connection_id=connection_id,
                                  adapter_description=adapter_description,
                                  basepath=basepath, snode=snode,
                                  operating_system=operating_system, sport=sport,
                                  user=user, password=password)
                generated_structure_ticket(origen="CONNECTDIRECT", params=parameters, is_dev=is_dev)

        elif type_adapter.upper() == "ORACLE":
            if 'uuaa' not in parameter.keys():
                print(get_color_b("required parameters uuaa"))
            if 'schema_oracle' not in parameter.keys():
                print(get_color_b("required parameters schema_oracle"))
            else:
                env = "dev" if is_dev else "pro"
                uuaa = parameter.get("uuaa")
                schema_oracle = parameter.get("schema_oracle")
                ns = read_ns(uuaa=uuaa, is_dev=is_dev)
                adapter_id = f"adapter-oraclepe{schema_oracle.lower()}-{uuaa.lower()}"
                connection_id = f"con-pe-adapter-oraclepe{schema_oracle.lower()}-{uuaa.lower()}-{env}"
                adapter_description = f"Adapter to access {uuaa.upper()} ORACLE{schema_oracle.upper()} files in {env}"
                host = ""
                port = ""
                service = ""
                user = ""
                password = ""

                if name_adapter.upper() == "PERU":
                    host = "118.180.35.45" if is_dev else "118.180.61.137"
                    port = "1521"
                    service = "tst12c"
                    user = "Credencial lo agrega el aplicativo"
                    password = "Credencial lo agrega el aplicativo"

                parameters = dict(uuaa=uuaa, ns=ns, adapter_id=adapter_id,
                                  connection_id=connection_id,
                                  adapter_description=adapter_description,
                                  host=host, port=port, service=service,
                                  user=user, password=password)
                generated_structure_ticket(origen="ORACLE", params=parameters, is_dev=is_dev)

# def generate_parquet_spark(spark=None,
#                            df=None,
#                            table_name=None,
#                            spark_schema=None,
#                            spark_schema_string=None,
#                            directory_output=None,
#                            sample_parquet=None,
#                            columns_string_default={},
#                            columns_date_default={},
#                            columns_decimal_default={},
#                            columns_integer_default={}
#                            ):
#     if not spark:
#         raise Exception(f'require object spark: {spark} ')
#
#     if not isinstance(df, pd.DataFrame):
#         raise Exception('require var df: {df} ')
#
#     if not table_name:
#         raise Exception(f'require var table_name: {table_name} ')
#
#     if not spark_schema:
#         raise Exception(f'require var spark_schema: {spark_schema} ')
#
#     import random
#     import string
#     from datetime import datetime
#     from dateutil.relativedelta import relativedelta
#     from faker import Faker
#     from pyspark.sql import functions as func
#
#     fake = Faker()
#
#     df = df[df["table"] == f'{table_name}']
#
#     output2 = list()
#     for _ in range(sample_parquet):
#         columns_dict = dict()
#
#         for index, row in df.iterrows():
#             naming = str(row['naming']).lower().strip()
#             _format = row['format']
#             if str(_format).upper() == "TIME":
#                 _format = "ALPHANUMERIC(8)"
#             _spark_format = spark_transform_dtype(format=_format)
#             _parentheses = extract_only_parentesis(format=_format)
#
#             _fake = None
#             if _spark_format in ("INTEGER",):
#                 _fake = fake.pyint(min_value=0, max_value=9999)
#                 if naming in list(columns_integer_default.keys()):
#                     new_int = int(columns_integer_default[naming])
#                     _fake = fake.pyint(min_value=new_int, max_value=new_int)
#
#             elif _spark_format in ("TIMESTAMP",):
#                 d2 = datetime.now()
#                 d1 = d2 - relativedelta(months=6)
#                 _fake = fake.date_time_between(start_date=d1, end_date=d2)
#             elif _spark_format in ("DECIMAL",):
#                 _parentheses_split = str(_parentheses).split(",")
#                 if len(_parentheses_split) <= 1:
#                     _decimal_left = int(_parentheses_split[0])
#                     _decimal_right = 0
#                 else:
#                     _decimal_left = int(_parentheses_split[0])
#                     _decimal_right = int(_parentheses_split[1])
#
#                 min_value_left = int("1" * (_decimal_left - _decimal_right))
#                 max_value_left = int("9" * (_decimal_left - _decimal_right))
#
#                 if _decimal_right == 0:
#                     _decimal_right2 = 1
#                     min_value_right = int("0" * _decimal_right2)
#                     max_value_right = int("0" * _decimal_right2)
#                 else:
#                     _decimal_right2 = _decimal_right
#                     min_value_right = int("1" * _decimal_right2)
#                     max_value_right = int("9" * _decimal_right2)
#
#                 _fake = str(fake.pydecimal(left_digits=_decimal_left,
#                                            right_digits=_decimal_right,
#                                            positive=True,
#                                            min_value=min_value_left,
#                                            max_value=max_value_left))
#
#                 if naming in list(columns_decimal_default.keys()):
#                     new_decimal = float(columns_decimal_default[naming])
#                     _fake = fake.bothify(text=f'{new_decimal}')
#
#             elif _spark_format in ("TIME",):
#                 _fake = fake.time()
#             elif _spark_format in ("DATE",):
#                 if naming in list(columns_date_default.keys()):
#                     new_text = columns_date_default[naming]
#                     _fake = datetime.strptime(new_text, '%Y-%m-%d')
#                 else:
#                     d2 = datetime.today()
#                     d1 = d2 - relativedelta(months=6)
#                     _fake = fake.date_between(start_date=d1, end_date=d2)
#             elif _spark_format in ("STRING", "DATE"):
#                 if naming in ("g_entific_id",):
#                     _fake = fake.bothify(text='PE')
#                 elif naming in ("gf_frequency_type", "frequency_type"):
#                     _fake = fake.bothify(text='?', letters='DM')
#                 elif naming in list(columns_string_default.keys()):
#                     new_text = columns_string_default[naming]
#                     _fake = fake.bothify(text=new_text)
#                 else:
#                     _fake = ''.join(random.choices(string.ascii_letters + string.digits, k=int(_parentheses)))
#             columns_dict[naming] = _fake
#         output2.append(columns_dict)
#     df2 = pd.DataFrame(output2)
#
#     df3 = spark.createDataFrame(df2, schema=spark_schema_string)
#
#     for i in spark_schema.jsonValue()["fields"]:
#         column_name = str(i["name"])
#         column_type = str(i["type"])
#         if column_type.startswith("decimal"):
#             df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast(f"{column_type}"))
#         elif column_type.startswith("date"):
#             df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("date"))
#         elif column_type.startswith("timestamp"):
#             df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("timestamp"))
#
#     df3.coalesce(1).write.mode("overwrite").parquet(f'{directory_output}/{table_name}/dummy_{table_name}.parquet')
#
#     return df3
#
#
# def generate_components(spark=None,
#                         path_excel=None,
#                         uuaa_name=None,
#                         table_name=None,
#                         schema_datax_version="0",
#                         directory_output="schema_dev_summary",
#                         sample_parquet=500,
#                         columns_string_default={},
#                         columns_date_default={},
#                         columns_decimal_default={},
#                         columns_integer_default={}):
#     pass
