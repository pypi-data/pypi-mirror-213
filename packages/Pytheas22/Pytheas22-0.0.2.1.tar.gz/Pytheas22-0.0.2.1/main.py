from Pytheas22 import Python_Port_Scanner

data = Python_Port_Scanner.PythonPortScannerList(well_known_ports=True)
data = data.make_lst()

scanning = Python_Port_Scanner.PythonPortScanner(data, ssh_bruteforce=True)
scanning.scan_internal_network()
