from ftplib import FTP, FTP_TLS
import http.client
import re
import time
import urllib.parse
import socket
import ssl
from TheSilent.return_user_agent import return_user_agent
from TheSilent.clear import clear

socket.setdefaulttimeout(120)

verify = ssl.create_default_context()
verify.set_ciphers('HIGH:!DH:!aNULL')
verify.check_hostname = False
verify.verify_mode = ssl.CERT_NONE

RED = "\033[1;31m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"

sql_errors = ["SQL syntax.*?MySQL",
        "Warning.*?\\Wmysqli?_",
        "MySQLSyntaxErrorException",
        "valid MySQL result",
        "check the manual that (corresponds to|fits) your MySQL server version",
        "check the manual that (corresponds to|fits) your MariaDB server version",
        "check the manual that (corresponds to|fits) your Drizzle server version",
        "Unknown column '[^ ]+' in 'field list'",
        "MySqlClient\\.",
        "com\\.mysql\\.jdbc",
        "Zend_Db_(Adapter|Statement)_Mysqli_Exception",
        "Pdo\\[./_\\]Mysql",
        "MySqlException",
        "SQLSTATE\\[\\d+\\]: Syntax error or access violation",
        "MemSQL does not support this type of query",
        "is not supported by MemSQL",
        "unsupported nested scalar subselect",
        "PostgreSQL.*?ERROR",
        "Warning.*?\\Wpg_",
        "valid PostgreSQL result",
        "Npgsql\\.",
        "PG::SyntaxError:",
        "org\\.postgresql\\.util\\.PSQLException",
        "ERROR:\\s\\ssyntax error at or near",
        "ERROR: parser: parse error at or near",
        "PostgreSQL query failed",
        "org\\.postgresql\\.jdbc",
        "Pdo\\[./_\\]Pgsql",
        "PSQLException",
        "OLE DB.*? SQL Server",
        "\bSQL Server[^&lt;&quot;]+Driver",
        "Warning.*?\\W(mssql|sqlsrv)_",
        "\bSQL Server[^&lt;&quot;]+[0-9a-fA-F]{8}",
        "System\\.Data\\.SqlClient\\.(SqlException|SqlConnection\\.OnError)",
        "(?s)Exception.*?\bRoadhouse\\.Cms\\.",
        "Microsoft SQL Native Client error '[0-9a-fA-F]{8}",
        "\\[SQL Server\\]",
        "ODBC SQL Server Driver",
        "ODBC Driver \\d+ for SQL Server",
        "SQLServer JDBC Driver",
        "com\\.jnetdirect\\.jsql",
        "macromedia\\.jdbc\\.sqlserver",
        "Zend_Db_(Adapter|Statement)_Sqlsrv_Exception",
        "com\\.microsoft\\.sqlserver\\.jdbc",
        "Pdo\\[./_\\](Mssql|SqlSrv)",
        "SQL(Srv|Server)Exception",
        "Unclosed quotation mark after the character string",
        "Microsoft Access (\\d+ )?Driver",
        "JET Database Engine",
        "Access Database Engine",
        "ODBC Microsoft Access",
        "Syntax error \\(missing operator\\) in query expression",
        "\bORA-\\d{5}",
        "Oracle error",
        "Oracle.*?Driver",
        "Warning.*?\\W(oci|ora)_",
        "quoted string not properly terminated",
        "SQL command not properly ended",
        "macromedia\\.jdbc\\.oracle",
        "oracle\\.jdbc",
        "Zend_Db_(Adapter|Statement)_Oracle_Exception",
        "Pdo\\[./_\\](Oracle|OCI)",
        "OracleException",
        "CLI Driver.*?DB2",
        "DB2 SQL error",
        "\bdb2_\\w+\\(",
        "SQLCODE[=:\\d, -]+SQLSTATE",
        "com\\.ibm\\.db2\\.jcc",
        "Zend_Db_(Adapter|Statement)_Db2_Exception",
        "Pdo\\[./_\\]Ibm",
        "DB2Exception",
        "ibm_db_dbi\\.ProgrammingError",
        "Warning.*?\\Wifx_",
        "Exception.*?Informix",
        "Informix ODBC Driver",
        "ODBC Informix driver",
        "com\\.informix\\.jdbc",
        "weblogic\\.jdbc\\.informix",
        "Pdo\\[./_\\]Informix",
        "IfxException",
        "Dynamic SQL Error",
        "Warning.*?\\Wibase_",
        "org\\.firebirdsql\\.jdbc",
        "Pdo\\[./_\\]Firebird",
        "SQLite/JDBCDriver",
        "SQLite\\.Exception",
        "(Microsoft|System)\\.Data\\.SQLite\\.SQLiteException",
        "Warning.*?\\W(sqlite_|SQLite3::)",
        "\\[SQLITE_ERROR\\]",
        "SQLite error \\d+:",
        "sqlite3.OperationalError:",
        "SQLite3::SQLException",
        "org\\.sqlite\\.JDBC",
        "Pdo\\[./_\\]Sqlite",
        "SQLiteException",
        "SQL error.*?POS([0-9]+)",
        "Warning.*?\\Wmaxdb_",
        "DriverSapDB",
        "-3014.*?Invalid end of SQL statement",
        "com\\.sap\\.dbtech\\.jdbc",
        "\\[-3008\\].*?: Invalid keyword or missing delimiter",
        "Warning.*?\\Wsybase_",
        "Sybase message",
        "Sybase.*?Server message",
        "SybSQLException",
        "Sybase\\.Data\\.AseClient",
        "com\\.sybase\\.jdbc",
        "Warning.*?\\Wingres_",
        "Ingres SQLSTATE",
        "Ingres\\W.*?Driver",
        "com\\.ingres\\.gcf\\.jdbc",
        "Exception (condition )?\\d+\\. Transaction rollback",
        "com\\.frontbase\\.jdbc",
        "Syntax error 1. Missing",
        "(Semantic|Syntax) error [1-4]\\d{2}\\.",
        "Unexpected end of command in statement \\[",
        "Unexpected token.*?in statement \\[",
        "org\\.hsqldb\\.jdbc",
        "org\\.h2\\.jdbc",
        "\\[42000-192\\]",
        "![0-9]{5}![^\n]+(failed|unexpected|error|syntax|expected|violation|exception)",
        "\\[MonetDB\\]\\[ODBC Driver",
        "nl\\.cwi\\.monetdb\\.jdbc",
        "Syntax error: EncounteCYAN",
        "org\\.apache\\.derby",
        "ERROR 42X01",
        ", Sqlstate: (3F|42).{3}, (Routine|Hint|Position):",
        "/vertica/Parser/scan",
        "com\\.vertica\\.jdbc",
        "org\\.jkiss\\.dbeaver\\.ext\\.vertica",
        "com\\.vertica\\.dsi\\.dataengine",
        "com\\.mckoi\\.JDBCDriver",
        "com\\.mckoi\\.database\\.jdbc",
        "&lt;REGEX_LITERAL&gt;",
        "com\\.facebook\\.presto\\.jdbc",
        "io\\.prestosql\\.jdbc",
        "com\\.simba\\.presto\\.jdbc",
        "UNION query has different number of fields: \\d+, \\d+",
        "Altibase\\.jdbc\\.driver",
        "com\\.mimer\\.jdbc",
        "Syntax error,[^\n]+assumed to mean",
        "io\\.crate\\.client\\.jdbc",
        "encounteCYAN after end of query",
        "A comparison operator is requiCYAN here",
        "-10048: Syntax error",
        "rdmStmtPrepare\\(.+?\\) returned",
        "SQ074: Line \\d+:",
        "SR185: Undefined procedure",
        "SQ200: No table ",
        "Virtuoso S0002 Error",
        "\\[(Virtuoso Driver|Virtuoso iODBC Driver)\\]\\[Virtuoso Server\\]"]

def web_scanner(host):
    clear()
    response_command_url = False
    response_command_headers = False
    response_command_cookie = False
    response_python_url = False
    response_python_headers = False
    response_python_cookie = False
    response_sql_url = False
    response_sql_headers = False
    response_sql_cookie = False
    response_xss_url = False
    response_xss_headers = False
    response_xss_cookie = False

    try:
        # get admin
        print(CYAN + "checking for admin")
        my_request = http.client.HTTPSConnection(host, context=verify)
        my_request.request("GET", "/admin", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
        response_admin = my_request.getresponse().status
        time.sleep(5)

    except:
        pass

    try:
        # get cgi-bin
        print(CYAN + "checking for cgi-bin")
        my_request = http.client.HTTPSConnection(host, context=verify)
        my_request.request("GET", "/cgi-bin", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
        response_cgi_bin = my_request.getresponse().status
        time.sleep(5)

    except:
        pass

    try:
        # test directory traversal
        print(CYAN + "checking for directory traversal using /.../")
        my_request = http.client.HTTPSConnection(host, context=verify)
        my_request.request("GET", "/.../", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
        response_directory_traversal = my_request.getresponse().status
        time.sleep(5)

    except:
        pass

    try:
        # get .env
        print(CYAN + "checking for .env")
        my_request = http.client.HTTPSConnection(host, context=verify)
        my_request.request("GET", "/.env", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
        response_env = my_request.getresponse().status
        time.sleep(5)
    except:
        pass

    try:
        # get .git
        print(CYAN + "checking for .git")
        my_request = http.client.HTTPSConnection(host, context=verify)
        my_request.request("GET", "/.git", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
        response_git = my_request.getresponse().status
        time.sleep(5)

    except:
        pass

    try:
        # test trace method
        print(CYAN + "checking trace method")
        my_request = http.client.HTTPSConnection(host, context=verify)
        my_request.request("TRACE", "", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
        response_trace = my_request.getresponse().status
        time.sleep(5)

    except:
        pass

    try:
        # test track method
        print(CYAN + "checking track method")
        my_request = http.client.HTTPSConnection(host, context=verify)
        my_request.request("TRACK", "", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
        response_track = my_request.getresponse().status

    except:
        pass

    try:
        # test for command injection in url
        print(CYAN + "checking for command injection in url")
        mal_commands = ["/echo TheSilent", "/ping -c 60 127.0.0.1"]
        for mal in mal_commands:
            time.sleep(5)
            my_request = http.client.HTTPSConnection(host, context=verify)
            start = time.time()
            my_request.request("GET", f"/{urllib.parse.quote(mal)}", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
            simple_response = str(my_request.getresponse().read())
            end = time.time()
            if mal == "/echo TheSilent" and "TheSilent" in simple_response and "echo" not in simple_response:
                response_command_url = True

            if mal == "/ping -c 60 127.0.0.1" and end - start >= 60:
                response_command_url = True

    except:
        pass

    try:
        # test for command injection in headers
        print(CYAN + "checking for command injection in headers")
        mal_commands = ["/echo TheSilent", "/ping -c 60 127.0.0.1"]
        break_for_loop = False
        # get original headers
        my_request = http.client.HTTPSConnection(host, context=verify)
        my_request.request("GET", "", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
        header_response = my_request.getresponse().getheaders()
        time.sleep(5)
        for head in header_response:
            if break_for_loop:
                break
            
            for mal in mal_commands:
                time.sleep(5)
                my_request = http.client.HTTPSConnection(host, context=verify)
                start = time.time()
                my_request.request("GET", "", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36", head[0]:mal})
                simple_response = str(my_request.getresponse().read())
                end = time.time()
                if mal == "/echo TheSilent" and "TheSilent" in simple_response and "echo" not in str(simple_response.read()):
                    response_command_headers = True
                    break_for_loop = True
                    break

                if mal == "/ping -c 60 127.0.0.1" and end - start >= 60:
                    response_command_headers = True
                    break_for_loop = True
                    break

    except:
        pass

    try:
        # test for command injection in cookie
        print(CYAN + "checking for command injection in cookie")
        mal_commands = ["/echo TheSilent", "/ping -c 60 127.0.0.1"]
        for mal in mal_commands:
            time.sleep(5)
            my_request = http.client.HTTPSConnection(host, context=verify)
            start = time.time()
            my_request.request("GET", "", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36", "Cookie":f"{mal}={mal}"})
            simple_response = str(my_request.getresponse().read())
            end = time.time()
            if mal == "/echo TheSilent" and "TheSilent" in simple_response and "echo" not in simple_response:
                response_command_cookie = True
                break

            if mal == "/ping -c 60 127.0.0.1" and end - start >= 60:
                response_command_cookie = True

    except:
        pass

    try:
        # test for python injection in url
        print(CYAN + "checking for python injection in url")
        mal_python = [r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))', r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))', r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))']
        for mal in mal_python:
            time.sleep(5)
            my_request = http.client.HTTPSConnection(host, context=verify)
            start = time.time()
            my_request.request("GET", f"/{urllib.parse.quote(mal)}", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
            simple_response = str(my_request.getresponse().read())
            end = time.time()
            if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))' and "gcc" in simple_response.lower():
                response_python_url = True

            if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))' and "gcc" in simple_response.lower():
                response_python_url = True
                
            if mal == r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))' and end - start >= 60:
                response_python_url = True

    except:
        pass

    try:
        # test for python injection in headers
        print(CYAN + "checking for python injection in headers")
        mal_python = [r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))', r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))', r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))']
        break_for_loop = False
        # get original headers
        my_request = http.client.HTTPSConnection(host, context=verify)
        my_request.request("GET", "", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
        header_response = my_request.getresponse().getheaders()
        time.sleep(5)
        for head in header_response:
            if break_for_loop:
                break
            
            for mal in mal_python:
                time.sleep(5)
                my_request = http.client.HTTPSConnection(host, context=verify)
                start = time.time()
                my_request.request("GET", "", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36", head[0]:mal})
                simple_response = str(my_request.getresponse().read())
                end = time.time()
                if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))' and "gcc" in simple_response.lower():
                    response_python_headers = True
                    break_for_loop = True
                    break

                if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))' and "gcc" in simple_response.lower():
                    response_python_headers = True
                    break_for_loop = True
                    break
                    
                if mal == r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))' and end - start >= 60:
                    response_python_headers = True
                    break_for_loop = True
                    break

    except:
        pass

    try:
        # test for python injection in cookie
        print(CYAN + "checking for python injection in cookie")
        mal_python = [r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))', r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))', r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))']
        for mal in mal_python:
            time.sleep(5)
            my_request = http.client.HTTPSConnection(host, context=verify)
            start = time.time()
            my_request.request("GET", "", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36", "Cookie":f"{mal}={mal}"})
            simple_response = str(my_request.getresponse().read())
            end = time.time()
            if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))' and "gcc" in simple_response.lower():
                response_python_cookie = True

            if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))' and "gcc" in simple_response.lower():
                response_python_cookie = True
                
            if mal == r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))' and end - start >= 60:
                response_python_cookie = True

    except:
        pass

    try:
        # test for sql injection in url
        print(CYAN + "checking for sql injection in url")
        mal_sql = ["'", '"', "*", ";", "`", "')", '")', "*)", ";)", "`)", "'))", '"))', "*))", ";))", "`))", "')))", '")))', "*)))", ";)))", "`)))"]
        break_for_loop = False
        for mal in mal_sql:
            if break_for_loop:
                break

            time.sleep(5)
            my_request = http.client.HTTPSConnection(host, context=verify)
            my_request.request("GET", f"/{urllib.parse.quote(mal)}", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
            simple_response = str(my_request.getresponse().read())
            for error in sql_errors:
                result = re.search(error, simple_response)
                if result:
                    response_sql_url = True
                    break_for_loop = True
                    break

    except:
        pass

    try:
        # test for sql injection in headers
        print(CYAN + "checking for sql injection in headers")
        mal_sql = ["'", '"', "*", ";", "`", "')", '")', "*)", ";)", "`)", "'))", '"))', "*))", ";))", "`))", "')))", '")))', "*)))", ";)))", "`)))"]
        break_for_loop = False
        # get original headers
        my_request = http.client.HTTPSConnection(host, context=verify)
        my_request.request("GET", "", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
        header_response = my_request.getresponse().getheaders()
        time.sleep(5)
        for head in header_response:
            if break_for_loop:
                break

            for mal in mal_sql:
                if break_for_loop:
                    break

                time.sleep(5)
                my_request = http.client.HTTPSConnection(host, context=verify)
                my_request.request("GET", "", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36", head[0]:mal})
                simple_response = str(my_request.getresponse().read())
                for error in sql_errors:
                    result = re.search(error, simple_response)
                    if result:
                        response_sql_headers = True
                        break_for_loop = True
                        break

    except:
        pass

    try:
        # test for sql injection in cookie
        print(CYAN + "checking for sql injection in cookie")
        mal_sql = ["'", '"', "*", ";", "`", "')", '")', "*)", ";)", "`)", "'))", '"))', "*))", ";))", "`))", "')))", '")))', "*)))", ";)))", "`)))"]
        break_for_loop = False
        for mal in mal_sql:
            if break_for_loop:
                break

            time.sleep(5)
            my_request = http.client.HTTPSConnection(host, context=verify)
            my_request.request("GET", "", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36", "Cookie":f"{mal}={mal}"})
            simple_response = str(my_request.getresponse().read())
            for error in sql_errors:
                result = re.search(error, simple_response)
                if result:
                    response_sql_cookie = True
                    break_for_loop = True
                    break

    except:
        pass

    try:
        # test for xss in url
        print(CYAN + "checking for xss in url")
        mal_xss = ["<div>TheSilent</div>", "<em>TheSilent</em>", "<iframe>TheSilent</iframe>", "<input type='text' id='thesilent' name='TheSilent' value='TheSilent'>", "<p>TheSilent</p>", '<script>alert("TheSilent")</script>;', '<script>prompt("TheSilent")</script>;', "<strong>TheSilent</strong>"]
        for mal in mal_xss:
            time.sleep(5)
            my_request = http.client.HTTPSConnection(host, context=verify)
            my_request.request("GET", f"/{urllib.parse.quote(mal)}", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
            simple_response = str(my_request.getresponse().read())
            if mal in simple_response:
                response_xss_url = True
                break

    except:
        pass

    try:
        # test for xss in headers
        print(CYAN + "checking for xss in headers")
        mal_xss = ["<div>TheSilent</div>", "<em>TheSilent</em>", "<iframe>TheSilent</iframe>", "<input type='text' id='thesilent' name='TheSilent' value='TheSilent'>", "<p>TheSilent</p>", '<script>alert("TheSilent")</script>;', '<script>prompt("TheSilent")</script>;', "<strong>TheSilent</strong>"]
        break_for_loop = False
        # get original headers
        my_request = http.client.HTTPSConnection(host, context=verify)
        my_request.request("GET", "", headers={"User-Agent":return_user_agent(), "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding":"gzip, deflate","Accept-Language":"en-US,en;q=0.9"})
        header_response = my_request.getresponse().getheaders()
        time.sleep(5)
        for head in header_response:
            if break_for_loop:
                break
            
            for mal in mal_xss:
                time.sleep(5)
                my_request = http.client.HTTPSConnection(host, context=verify)
                my_request.request("GET", "", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36", head[0]:mal})
                simple_response = str(my_request.getresponse().read())
                if mal in simple_response:
                    response_xss_headers = True
                    break_for_loop = True
                    break

    except:
        pass

    try:
        # test for xss in cookie
        print(CYAN + "checking for xss in cookie")
        mal_xss = ["<div>TheSilent</div>", "<em>TheSilent</em>", "<iframe>TheSilent</iframe>", "<input type='text' id='thesilent' name='TheSilent' value='TheSilent'>", "<p>TheSilent</p>", '<script>alert("TheSilent")</script>;', '<script>prompt("TheSilent")</script>;', "<strong>TheSilent</strong>"]
        for mal in mal_xss:
            time.sleep(5)
            my_request = http.client.HTTPSConnection(host, context=verify)
            my_request.request("GET", "", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36", "Cookie":f"{mal}={mal}"})
            simple_response = str(my_request.getresponse().read())
            if mal in simple_response:
                response_xss_cookie = True
                break

    except:
        pass

    # test for annonymous ftp bindings
    print("checking for annonymous ftp bindings")
    ftp_verify = False
    
    time.sleep(5)
    try:
        ftp = FTP(new_url)
        ftp.login()
        ftp.close()
        ftp_verify = True
        
    except:
        pass

    time.sleep(5)
    try:
        ftp = FTP_TLS(new_url)
        ftp.login()
        ftp.close()
        ftp_verify = True
        
    except:
        pass
    
    secure = True
    clear()

    if response_admin == 200:
        print(RED + "Admin page found!")
        secure = False

    if response_cgi_bin == 200:
        print(RED + "CGI-BIN directory found!")
        secure = False

    if response_command_url:
        print(RED + "Command injection in url found!")
        secure = False

    if response_command_headers:
        print(RED + "Command injection in headers found!")
        secure = False

    if response_command_cookie:
        print(RED + "Command injection in cookie found!")
        secure = False

    if response_directory_traversal == 200:
        print(RED + "Directory traversal using /.../ found!")
        secure = False

    if response_env == 200:
        print(RED + ".ENV found!")
        secure = False

    if ftp_verify:
        print(RED + "Annonymous ftp binding found!")
        secure = False

    if response_git == 200:
        print(RED + ".GIT found!")
        secure = False

    if response_python_url:
        print(RED + "Python injection in url found!")
        secure = False

    if response_python_headers:
        print(RED + "Python injection in headers found!")
        secure = False

    if response_python_cookie:
        print(RED + "Python injection in cookie found!")
        secure = False

    if response_sql_url:
        print(RED + "SQL injection found in url!")
        secure = False

    if response_sql_headers:
        print(RED + "SQL injection found in headers!")
        secure = False

    if response_sql_cookie:
        print(RED + "SQL injection found in cookie!")
        secure = False

    if response_trace == 200:
        print(RED + "TRACE method allowed!")
        secure = False

    if response_track == 200:
        print(RED + "TRACK method allowed!")
        secure = False

    if response_xss_url:
        print(RED + "XSS found in url!")
        secure = False

    if response_xss_headers:
        print(RED + "XSS found in headers!")
        secure = False

    if response_xss_cookie:
        print(RED + "XSS found in cookie!")
        secure = False

    if secure:
        print(GREEN + "This server is secure!")
