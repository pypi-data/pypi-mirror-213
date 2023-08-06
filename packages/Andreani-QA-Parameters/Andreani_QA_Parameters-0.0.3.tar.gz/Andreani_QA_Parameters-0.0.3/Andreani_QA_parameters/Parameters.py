import os
import platform


class Parameters:
    # CONFIGURACION PATH Y TESTCASE
    current_path = os.path.abspath(os.path.join(__file__, "../../../../../"))
    file_name_stored = None
    env = None

    # CONFIGURACION PARA UTILIZAR CSV DESDE SHAREPOINT
    #sharepoint_data_jmeter=None

    # CONFIGURACION FORMATO DE FECHA
    date_format = '%d/%m/%Y'
    time_format = "%H:%M:%S"

    # CONFIGURACION DE TIEMPO Y REINTENTOS PARA LA OBTENCIÓN DE ELEMENTOS
    time_between_retries = 0.5
    number_retries = 6
    highlight = True

    # CONFIGURACION DE TIEMPO Y REINTENTOS PARA LA OBTENCIÓN DE ELEMENTOS
    loggin_time = True
    loggin_exceptions = False
    timeout_base_sql_server = 20

    # ENTORNO POR DEFECTO
    environment = platform.system()
    enviroment_confguration = os.getenv('PYBOT_SYSTEM')

    # CONFIOGURACION DE BROWSER Y PRUEBAS
    browser = 'CHROME'
    debug = False
    headless = False
    #VARIABLE LISTA DE PASOS
    steps_list = []

    # CONFIGURACION INCREMENTO AUTO/MANUALEXCEL
    excel = f"{current_path}\\resources"
    manual_increment = False
    row = 2

    # CONFIGURACION PATH JMETER
    path_jmeter = f"C:\\Tools\\Jmeter\\bin\\jmeter.bat"
    path_jmeter_libraries_ext = f"C:\\Tools\\Jmeter\\lib\\ext"
    path_jmeter_downloads = f"{current_path}\\projects\\ApisCliente\\src\\downloads"
    path_jmeter_report_jtl = f"{path_jmeter_downloads}\\report.jtl"
    path_aggregate_report_csv_out = f"{path_jmeter_downloads}\\AggregateReport.csv"
    path_response_over_times_png_out = f"{path_jmeter_downloads}\\ResponseTimesOverTime.png"
    path_response_code_per_second_png_out = f"{path_jmeter_downloads}\\ResponseCodePerSecond.png"
    path_response_threads_state_over_time = f"{path_jmeter_downloads}\\ThreadsStateOverTime.png"
    path_dashboard = f"{current_path}\\projects\\ApisCliente\\src\\outputs\\dashboard_jmeter"
    path_index_html_dashboard = f"{path_dashboard}\\index.html"

    # CONFIGURACION TEST DE STRESS Y CARGA
    users_jmeter = 1
    rampup_jmeter = 1
    duration_jmeter = 1
    throughput_jmeter = 0
    url_jmeter = ""

    # CONFIGURACION PARA VALIDACION
    status_code_expected = 200
    parameter_id = None
    expected_value = ""

    server = "127.0.0.1"  # Direccion Ip de la UI desplegada por locust.
    port = 8089  # Puerto de la UI desplegada por locust.
    max_threads = 100  # Cantidad maxima de hilos (Peticiones) alcanzable.
    rate = 10  # Coeficiente incremental de carga.
    duration = 60  # Duracion de la prueba (Segundos)
    wait_time = 1  # Duracion de tiempos de espera entre peticiones.

    # CONFIGURACION DE EJECUCION
    if environment == 'Windows':
        # DIRECTORIO DE LA EVIDENCIA
        evidence_route = current_path
        resource = f"{current_path}\\projects"

    if environment == 'Linux':
        # DIRECTORIO DE LA EVIDENCIA
        evidence_route = current_path

    # CONFIGURACION PARA NOTIFICACIONES DE TEAMS
    teams_notifications_colors = "#5b5fc7"
    teams_focus_test_colors = "#383966"