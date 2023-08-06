def dq_creating_directory_hdfs(spark=None, path=None):
    from spark_quality_rules_tools import get_color, get_color_b

    sc = spark.sparkContext
    fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(spark._jsc.hadoopConfiguration())
    if path in ("", None):
        raise Exception(f'required variable path')
    if not fs.exists(sc._jvm.org.apache.hadoop.fs.Path(f'{path}')):
        fs.mkdirs(sc._jvm.org.apache.hadoop.fs.Path(f'{path}'))
        print(f"{get_color('Directory Created:')} {get_color_b(path)}")
    else:
        print(f"{get_color('Directory Exists:')} {get_color_b(path)}")


def dq_creating_directory_sandbox(path=None):
    from spark_quality_rules_tools import get_color, get_color_b
    import os

    if path in ("", None):
        raise Exception(f'required variable path')
    if not os.path.exists(f'{path}'):
        os.makedirs(f'{path}')
        print(f"{get_color('Directory Created:')} {get_color_b(path)}")
    else:
        print(f"{get_color('Directory Exists:')} {get_color_b(path)}")


def dq_spark_session(user_sandbox=None):
    import os
    from pyspark.sql import SparkSession
    from spark_quality_rules_tools import get_color, get_color_b

    dir_uuaa_code = os.getenv("pj_dq_dir_uuaa_code")
    dir_sandbox_dq_metrics = os.getenv("pj_dq_dir_sandbox_dq_metrics")
    dir_sandbox_dq_refusals = os.getenv("pj_dq_dir_sandbox_dq_refusals")
    if user_sandbox is None:
        user_sandbox = os.getenv('JPY_USER')
        if user_sandbox in ("", None):
            raise Exception(f'required variable user_sandbox')
    if dir_uuaa_code in ("", None):
        raise Exception(f'required environment: pj_dq_dir_uuaa_code')
    if dir_sandbox_dq_metrics in ("", None):
        raise Exception(f'required environment: pj_dq_dir_sandbox_dq_metrics')
    if dir_sandbox_dq_refusals in ("", None):
        raise Exception(f'required environment: pj_dq_dir_sandbox_dq_refusals')

    os.environ['UUAA_CODE'] = dir_uuaa_code
    os.environ['JPY_USER'] = user_sandbox
    os.environ['SANDBOX_DQ_METRICS'] = dir_sandbox_dq_metrics
    os.environ['SANDBOX_DQ_REFUSALS'] = dir_sandbox_dq_refusals

    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("JONAP") \
        .getOrCreate()
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    sc = spark.sparkContext
    sc._conf.setExecutorEnv("UUAA_CODE", os.getenv("UUAA_CODE"))
    sc._conf.setExecutorEnv("JPY_USER", os.getenv("JPY_USER"))
    sc._conf.setExecutorEnv("SANDBOX_DQ_METRICS", os.getenv("SANDBOX_DQ_METRICS"))
    sc._conf.setExecutorEnv("SANDBOX_DQ_REFUSALS", os.getenv("SANDBOX_DQ_REFUSALS"))

    print(f"{get_color('Created Session Spark for user:')} {get_color_b(user_sandbox)}")
    return spark, sc


def dq_path_workspace(spark=None,
                      user_sandbox=None,
                      uuaa_code='fina',
                      project_sda='CDD'):
    import os
    import sys

    if user_sandbox is None:
        user_sandbox = os.getenv('JPY_USER')
        print(f"user_sandbox = {user_sandbox}")
        if user_sandbox in ("", None):
            raise Exception(f'required variable user_sandbox')
    is_windows = sys.platform.startswith('win')
    pj_dir_workspace = ""
    pj_dq_dir_uuaa_code = os.path.join(uuaa_code, "data", "projects", project_sda, "data_quality_rules")
    pj_dq_dir_sandbox_dq_metrics = f"/data/sandboxes/{pj_dq_dir_uuaa_code}/data/users/{user_sandbox}/dq/metrics"
    pj_dq_dir_sandbox_dq_refusals = f"/data/sandboxes/{pj_dq_dir_uuaa_code}/data/users/{user_sandbox}/dq/refusals"
    pj_dq_dir_name = "data_quality_rules"
    pj_dq_dir_artifacts_python = os.path.join(pj_dir_workspace, "artifacts", "python")
    pj_dq_dir_artifacts_scala = os.path.join(pj_dir_workspace, "artifacts", "scala")
    pj_dq_dir_name = os.path.join(pj_dir_workspace, pj_dq_dir_name)
    pj_dq_dir_confs_name = os.path.join(pj_dir_workspace, pj_dq_dir_name, "data_confs")
    pj_dq_dir_hocons_name = os.path.join(pj_dir_workspace, pj_dq_dir_name, "data_hocons")
    pj_dq_dir_reports_name = os.path.join(pj_dir_workspace, pj_dq_dir_name, "data_reports")
    pj_dq_dir_resolve_name = os.path.join(pj_dir_workspace, pj_dq_dir_name, "data_resolve")

    if is_windows:
        pj_dq_dir_uuaa_code = pj_dq_dir_uuaa_code.replace("\\", "/")
        pj_dq_dir_sandbox_dq_metrics = pj_dq_dir_sandbox_dq_metrics.replace("\\", "/")
        pj_dq_dir_sandbox_dq_refusals = pj_dq_dir_sandbox_dq_refusals.replace("\\", "/")
        pj_dq_dir_artifacts_python = pj_dq_dir_artifacts_python.replace("\\", "/")
        pj_dq_dir_artifacts_scala = pj_dq_dir_artifacts_scala.replace("\\", "/")
        pj_dq_dir_name = pj_dq_dir_name.replace("\\", "/")
        pj_dq_dir_confs_name = pj_dq_dir_confs_name.replace("\\", "/")
        pj_dq_dir_hocons_name = pj_dq_dir_hocons_name.replace("\\", "/")
        pj_dq_dir_reports_name = pj_dq_dir_reports_name.replace("\\", "/")
        pj_dq_dir_resolve_name = pj_dq_dir_resolve_name.replace("\\", "/")

    dq_creating_directory_sandbox(path=pj_dq_dir_name)
    dq_creating_directory_sandbox(path=pj_dq_dir_artifacts_python)
    dq_creating_directory_sandbox(path=pj_dq_dir_artifacts_scala)
    dq_creating_directory_sandbox(path=pj_dq_dir_confs_name)
    dq_creating_directory_sandbox(path=pj_dq_dir_hocons_name)
    dq_creating_directory_sandbox(path=pj_dq_dir_reports_name)
    dq_creating_directory_sandbox(path=pj_dq_dir_resolve_name)
    dq_creating_directory_hdfs(spark=spark, path=pj_dq_dir_sandbox_dq_metrics)
    dq_creating_directory_hdfs(spark=spark, path=pj_dq_dir_sandbox_dq_refusals)
    os.environ['pj_dq_dir_name'] = pj_dq_dir_name
    os.environ['pj_dq_dir_artifacts_python'] = pj_dq_dir_artifacts_python
    os.environ['pj_dq_dir_artifacts_scala'] = pj_dq_dir_artifacts_scala
    os.environ['pj_dq_dir_confs_name'] = pj_dq_dir_confs_name
    os.environ['pj_dq_dir_hocons_name'] = pj_dq_dir_hocons_name
    os.environ['pj_dq_dir_reports_name'] = pj_dq_dir_reports_name
    os.environ['pj_dir_workspace'] = pj_dir_workspace
    os.environ['pj_dq_dir_uuaa_code'] = pj_dq_dir_uuaa_code
    os.environ['pj_dq_dir_sandbox_dq_metrics'] = pj_dq_dir_sandbox_dq_metrics
    os.environ['pj_dq_dir_sandbox_dq_refusals'] = pj_dq_dir_sandbox_dq_refusals
    os.environ['pj_dq_dir_resolve_name'] = pj_dq_dir_resolve_name


def dq_download_jar(haas_jar_url=None,
                    haas_version="4.8.0",
                    force=False):
    import requests
    import sys
    import os
    from spark_quality_rules_tools import get_color, get_color_b
    is_windows = sys.platform.startswith('win')
    dir_artifacts_python = os.getenv('pj_dq_dir_artifacts_python')
    dir_artifacts_scala = os.getenv('pj_dq_dir_artifacts_scala')
    jar_name = "hammurabi-sandbox-spark3.jar"
    if dir_artifacts_python is None:
        raise Exception(f'required environment: pj_dq_dir_artifacts_python')
    if dir_artifacts_scala is None:
        raise Exception(f'required environment: pj_dq_dir_artifacts_scala')
    if haas_jar_url is None:
        haas_jar_url = f"http://artifactory-gdt.central-02.nextgen.igrupobbva/artifactory/" \
                       f"gl-datio-spark-libs-maven-local/com/datio/hammurabi-sandbox/{haas_version}/" \
                       f"hammurabi-sandbox-{haas_version}-jar-with-dependencies.jar"
    dir_artifacts_python_jar_file = os.path.join(dir_artifacts_python, jar_name)
    dir_artifacts_scala_jar_file = os.path.join(dir_artifacts_scala, jar_name)
    if is_windows:
        dir_artifacts_python_jar_file = dir_artifacts_python_jar_file.replace("\\", "/")
        dir_artifacts_scala_jar_file = dir_artifacts_scala_jar_file.replace("\\", "/")

    os.makedirs(os.path.dirname(dir_artifacts_python_jar_file), exist_ok=True)
    os.makedirs(os.path.dirname(dir_artifacts_scala_jar_file), exist_ok=True)

    if force:
        if os.path.isfile(dir_artifacts_python_jar_file):
            os.remove(dir_artifacts_python_jar_file)
        if os.path.isfile(dir_artifacts_scala_jar_file):
            os.remove(dir_artifacts_scala_jar_file)
        with requests.get(haas_jar_url, stream=True, verify=True) as r:
            r.raise_for_status()
            with open(dir_artifacts_python_jar_file, 'wb+') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        with requests.get(haas_jar_url, stream=True, verify=True) as r:
            with open(dir_artifacts_scala_jar_file, 'wb+') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"{get_color('Download Python finished on:')} {get_color_b(dir_artifacts_python_jar_file)}")
        print(f"{get_color('Download Scala finished on:')} {get_color_b(dir_artifacts_scala_jar_file)}")
    else:
        print(f"{get_color('Exist Jar haas Path:')} {get_color_b(dir_artifacts_python_jar_file)}")


def dq_validate_conf(url_conf=None):
    import requests
    from spark_quality_rules_tools import get_color_b

    if url_conf in ("", None):
        raise Exception(f'required variable url_conf')
    res = requests.get(url_conf)
    print(f"{get_color_b(f'{res.text}')}")


def dq_extract_parameters(url_conf=None):
    import os
    import sys
    import re
    import json
    import requests
    from spark_quality_rules_tools import get_color, get_color_b
    is_windows = sys.platform.startswith('win')
    dir_confs_name = os.getenv('pj_dq_dir_confs_name')

    if url_conf in ("", None):
        raise Exception(f'required variable url_conf')
    if dir_confs_name is None:
        raise Exception(f'required environment: pj_dq_dir_confs_name')

    url = url_conf
    url_conf_extension = str(str(url).split("/")[-1]).replace("-", "_").upper().strip()
    url_conf_name = str(str(url_conf_extension).split(".")[0])
    uuaa_name = str(str(url).split("/")[-2]).upper()
    if not len(uuaa_name) == 4:
        uuaa_name = str(str(url).split("/")[-5]).upper()

    dir_confs_filename = os.path.join(dir_confs_name, uuaa_name, f"{url_conf_name}.txt")
    dir_confs_filename_parameters = os.path.join(dir_confs_name, uuaa_name, f"PARAMS-{url_conf_name}.json")

    if is_windows:
        dir_confs_filename = dir_confs_filename.replace("\\", "/")
        dir_confs_filename_parameters = dir_confs_filename_parameters.replace("\\", "/")

    os.makedirs(os.path.dirname(dir_confs_filename), exist_ok=True)

    with requests.get(url, stream=True, verify=True) as r:
        r.raise_for_status()
        with open(dir_confs_filename, 'wb+') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with open(dir_confs_filename) as f:
        hammurabi_conf = f.read()

    variables_1 = sorted(list(set(re.findall(r'{([a-zA-Z_.-]+)}', hammurabi_conf))))
    variables_2 = sorted(list(set(re.findall(r'{?([a-zA-Z_.-]+)}', hammurabi_conf))))
    variables_list = list(set(variables_1 + variables_2))
    variables_dict = {variables: "" for variables in variables_list}

    parameter_dict = dict()
    parameter_dict[uuaa_name] = list()
    parameter_dict[uuaa_name].append({"table": url_conf_name,
                                      "conf_name": url_conf_extension,
                                      "parameters": variables_dict})

    with open(f"{dir_confs_filename_parameters}", "w") as f:
        json.dump(parameter_dict, f, indent=4)

    with open(f"{dir_confs_filename_parameters}") as f:
        parameter_conf = f.read()
        parameter_conf = json.loads(parameter_conf)

    params = parameter_conf[uuaa_name][0]["parameters"]
    params = json.dumps(params, indent=4)
    print(f"{get_color(f'================================')} ")
    print(f"{get_color('uuaa name :')} {get_color_b(uuaa_name)}")
    print(f"{get_color('table name:')} {get_color_b(url_conf_name)}")
    print(f"{get_color('conf name :')} {get_color_b(url_conf_extension)}")
    print(f"{get_color('parameters:')} {get_color_b(params)}")
    print(f"{get_color('=================================')} ")


def dq_run_sandbox(spark=None,
                   sc=None,
                   parameter_conf_list=None,
                   url_conf=None):
    import json
    import sys
    import os
    from datetime import datetime
    from tqdm import tqdm
    from pyhocon import ConfigFactory
    from pyhocon.converter import HOCONConverter
    from pyspark.sql import functions as func
    from spark_quality_rules_tools import get_color, get_color_b
    from spark_quality_rules_tools import get_replace_resolve_parameter

    is_windows = sys.platform.startswith('win')
    dir_confs_name = os.getenv('pj_dq_dir_confs_name')
    dir_hocons_name = os.getenv('pj_dq_dir_hocons_name')
    dir_reports_name = os.getenv('pj_dq_dir_reports_name')
    uuaa_code = os.getenv("UUAA_CODE")
    user_sandbox = os.getenv("JPY_USER")
    dir_sandbox_dq_metrics = os.getenv("pj_dq_dir_sandbox_dq_metrics")
    dir_sandbox_dq_refusals = os.getenv("pj_dq_dir_sandbox_dq_refusals")

    if url_conf in ("", None):
        raise Exception(f'required variable url_conf')
    if parameter_conf_list in ("", None):
        raise Exception(f'required variable parameter_conf_list')
    if dir_confs_name is None:
        raise Exception(f'required environment: pj_dq_dir_confs_name')
    if dir_hocons_name is None:
        raise Exception(f'required environment: pj_dq_dir_hocons_name')
    if dir_reports_name is None:
        raise Exception(f'required environment: pj_dq_dir_reports_name')
    if uuaa_code is None:
        raise Exception(f'required environment: UUAA_CODE')
    if user_sandbox is None:
        raise Exception(f'required environment: JPY_USER')
    if dir_sandbox_dq_metrics is None:
        raise Exception(f'required environment: pj_dq_dir_sandbox_dq_metrics')

    url = url_conf
    url_conf_extension = str(str(url).split("/")[-1]).replace("-", "_").upper().strip()
    url_conf_name = str(str(url_conf_extension).split(".")[0])
    uuaa_name = str(str(url).split("/")[-2]).upper()
    if not len(uuaa_name) == 4:
        uuaa_name = str(str(url).split("/")[-5]).upper()

    now = datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    current_datetime_str = now.strftime("%Y%m%d%H%M")

    dir_confs_filename = os.path.join(dir_confs_name, uuaa_name, f"{url_conf_name}.txt")
    dir_confs_filename_parameters = os.path.join(dir_confs_name, uuaa_name, f"PARAMS-{url_conf_name}.json")
    dir_hocons_filename = os.path.join(dir_hocons_name, uuaa_name, f"{url_conf_name}.conf")

    if is_windows:
        dir_confs_filename = dir_confs_filename.replace("\\", "/")
        dir_confs_filename_parameters = dir_confs_filename_parameters.replace("\\", "/")
        dir_hocons_filename = dir_hocons_filename.replace("\\", "/")
    os.makedirs(os.path.dirname(dir_hocons_filename), exist_ok=True)

    with open(dir_confs_filename_parameters) as f:
        parameter_conf = f.read()
        parameter_conf = json.loads(parameter_conf)

    params_parameter = parameter_conf[uuaa_name][0]["parameters"]
    validate_parameter_keys = list(set(params_parameter.keys()))
    validate_parameter_conf_keys = list(set([b for a in parameter_conf_list for b in a.keys()]))
    validate_compare_parameters = (sorted(validate_parameter_keys) == sorted(validate_parameter_conf_keys))
    if not validate_compare_parameters:
        raise Exception(f'Need more variables the parameters: parameter_conf_list')

    cutoff_date = ""
    with open(dir_confs_filename) as f:
        txt_conf = f.read()
    for params_parameter_conf in tqdm(parameter_conf_list):
        for k, v in params_parameter_conf.items():
            if str(k).upper() in ("ODATE", "ODATE_DATE", "CUTOFF_DATE"):
                cutoff_date = str(v).replace("-", "").strip()
            txt_conf = txt_conf.replace(f'${{{k}}}', v)
            txt_conf = txt_conf.replace(f'${{?{k}}}', v)
    txt_conf = txt_conf.replace(f'"/artifactory/"', "/artifactory/")
    dir_reports_name_filename = os.path.join(dir_reports_name, uuaa_name,
                                             f"{url_conf_name}_{current_datetime_str}_{cutoff_date}.csv")
    if is_windows:
        dir_reports_name_filename = dir_reports_name_filename.replace("\\", "/")
    os.makedirs(os.path.dirname(dir_reports_name_filename), exist_ok=True)

    conf_file = ConfigFactory.parse_string(txt_conf)
    hocons_file = HOCONConverter.to_hocon(conf_file)
    with open(dir_hocons_filename, "w") as f:
        f.write(hocons_file)

    spark._jvm.org.apache.hadoop.fs.Path
    spark._jvm.org.apache.hadoop.fs.FileSystem.get(spark._jsc.hadoopConfiguration())

    conf = sc._jvm.java.io.File(dir_hocons_filename)
    ConfigFactory2 = sc._jvm.com.typesafe.config.ConfigFactory
    parsed_conf = ConfigFactory2.parseFile(conf)
    resolve_path = get_replace_resolve_parameter(sc=sc)
    resolvedConfig = parsed_conf.withFallback(resolve_path).resolve()
    Standalone = sc._jvm.com.datio.hammurabi.sandbox
    result = Standalone.Hammurabi.run(spark._jsparkSession, resolvedConfig)

    if result == 2:
        print(f"{get_color('Problema para construir la ejecución, posible configuración o regla mal definida')} ")
    else:
        if result == 1:
            print(f"{get_color('La validación de calidad falló, la regla crítica falló')} ")
        elif result == 0:
            print(
                f"{get_color('Ha pasado la validación de calidad. Esto significa que no hay ninguna regla crítica que haya fallado.')} ")

    metrics_df = spark.read.parquet(dir_sandbox_dq_metrics)
    metrics_filter = metrics_df.filter(
        func.col("gf_quality_rule_execution_date") >= func.unix_timestamp(func.lit(current_datetime)).cast('timestamp'))
    df2 = metrics_filter.select(
        func.col("gf_qr_functional_definition_id"),
        func.concat(func.col("g_quality_rule_principle_type"),
                    func.lit("."),
                    func.col("g_quality_rule_type")).alias("Rule"),
        func.regexp_replace(func.col("gf_quality_rule_metadata_map.ruleName"),
                            "com.datio.hammurabi.rules.", ""
                            ).alias("Rule Name"),
        func.col("gf_qr_tg_object_physical_name"),
        func.col("gf_cutoff_date"),
        func.col("gf_field_physical_name").alias("Field"),
        func.col("gf_qr_aux_attribute_desc").alias("Format"),
        func.col("g_qr_critical_type").alias("Is Critical"),
        func.col("gf_qr_min_acceptance_per").alias("% Acceptation"),
        func.col("g_quality_rule_status_type").alias("Status"),
        func.col("gf_quality_rule_compliance_per").alias("Por"))
    df3 = df2.distinct().sort("gf_qr_functional_definition_id")
    df3.show(500, False, True)

    metrics_filter_pandas = df3.toPandas()
    metrics_filter_pandas.to_csv(dir_reports_name_filename, index=False)

    print(f"{get_color(f'================================')} ")
    print(f"{get_color('uuaa name :')} {get_color_b(uuaa_name)}")
    print(f"{get_color('table name:')} {get_color_b(url_conf_name)}")
    print(f"{get_color('conf name :')} {get_color_b(url_conf_extension)}")
    print(f"{get_color('cutoff date:')} {get_color_b(cutoff_date)}")
    print(f"{get_color('Generating a file csv:')} {get_color_b(dir_reports_name_filename)}")
    print(f"{get_color('=================================')} ")


def dq_validate_rules(url_conf=None):
    import sys
    import os
    from spark_quality_rules_tools import get_validate_rules

    is_windows = sys.platform.startswith('win')
    dir_hocons_name = os.getenv('pj_dq_dir_hocons_name')

    url = url_conf
    url_conf_extension = str(str(url).split("/")[-1]).replace("-", "_").upper().strip()
    url_conf_name = str(str(url_conf_extension).split(".")[0])
    uuaa_name = str(str(url).split("/")[-2]).upper()
    if not len(uuaa_name) == 4:
        uuaa_name = str(str(url).split("/")[-5]).upper()

    if url_conf in ("", None):
        raise Exception(f'required variable url_conf')

    dir_hocons_filename = os.path.join(dir_hocons_name, uuaa_name, f"{url_conf_name}.conf")
    if is_windows:
        dir_hocons_filename = dir_hocons_filename.replace("\\", "/")
    get_validate_rules(hocons_dir=dir_hocons_filename)
