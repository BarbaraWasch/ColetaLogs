import os
import time
import re
import mysql.connector
from datetime import datetime

# Configuração do diretório e banco de dados
LOG_DIR = '/var/log/remote/'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'password'
DB_NAME = 'logs_db'

# Função para conectar ao banco de dados MySQL
def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

# Função para identificar tipo de log a partir do conteúdo
def get_log_type(log_entry):
    if "ERROR" in log_entry:
        return "ERROR"
    elif "WARNING" in log_entry:
        return "WARNING"
    elif "INFO" in log_entry:
        return "INFO"
    else:
        return "OTHER"

# Função para identificar o usuário do log (dependente do formato do log)
def get_log_user(log_entry):
    # Exemplo: Se o log contiver o usuário após a string 'user:'
    if "user:" in log_entry:
        return log_entry.split("user:")[1].split()[0]
    return "unknown"

# Função para extrair dados do agente rsyslog a partir do formato dos logs
def parse_rsyslog_entry(log_entry):
    # Exemplo de log rsyslog: <PRI>timestamp hostname appname[procid]: message
    rsyslog_pattern = r'^<(\d+)>(\S+ \S+) (\S+) (\S+): (.+)$'
    match = re.match(rsyslog_pattern, log_entry)
    
    if match:
        priority = match.group(1)  # Prioridade do log (PRI)
        timestamp = match.group(2)  # Timestamp do log (data/hora)
        hostname = match.group(3)   # Nome do host que enviou o log
        appname = match.group(4)    # Nome do aplicativo/processo
        message = match.group(5)    # Mensagem real do log
        
        return {
            "priority": priority,
            "timestamp": timestamp,
            "hostname": hostname,
            "appname": appname,
            "message": message
        }
    else:
        return None

# Função para processar logs
def process_logs():
    db = connect_db()
    cursor = db.cursor()
    
    for filename in os.listdir(LOG_DIR):
        file_path = os.path.join(LOG_DIR, filename)
        
        # Processar cada linha de log
        with open(file_path, 'r') as file:
            for line in file:
                rsyslog_data = parse_rsyslog_entry(line)
                
                if rsyslog_data:
                    log_type = get_log_type(rsyslog_data["message"])
                    log_user = get_log_user(rsyslog_data["message"])
                    log_date = datetime.now().date()  # Data atual (pode ser extraída do log)
                    log_time = datetime.now().time()  # Hora atual (pode ser extraída do log)
                    
                    # Inserir os dados no banco de dados
                    cursor.execute(
                        "INSERT INTO logs (log_entry, log_type, log_user, log_date, log_time, priority, hostname, appname) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (rsyslog_data["message"], log_type, log_user, log_date, log_time,
                         rsyslog_data["priority"], rsyslog_data["hostname"], rsyslog_data["appname"])
                    )
        
        db.commit()
        os.remove(file_path)  # Remove o arquivo após o processamento

    cursor.close()
    db.close()

# Agendar a execução a cada hora
if __name__ == '__main__':
    while True:
        process_logs()
        time.sleep(3600)  # Pausa de 1 hora
