# AD_check_user_existence.py
from ldap3 import Server, Connection, ALL, SUBTREE

def check_user_exists(ad_server, ad_user, ad_password, ad_search_base, username_to_check):
    """Check if a user exists in Active Directory"""
    # Connect to AD server
    server = Server(ad_server, port=389, get_info=ALL)
    conn = Connection(server, user=ad_user, password=ad_password)

    try:
        if conn.bind():
            print("Successfully connected to AD server")
            conn.search(f'{ad_search_base}', f'(sAMAccountName={username_to_check})', search_scope=SUBTREE)
            if conn.entries:
                print(f"User '{username_to_check}' exists in Active Directory.")
            else:
                print(f"User '{username_to_check}' does not exist in Active Directory.")
        else:
            print(f"Connection failed: {conn.result}")
    except Exception as e:
        print(f"Error connecting to AD server: {str(e)}")
    finally:
        conn.unbind()
        print("Disconnected from AD server")

if __name__ == "__main__":

    AD_SERVER = "172.16.30.142"
    AD_USER = "CN=Administrator,CN=Users,DC=idmtdc,DC=com"
    AD_PASSWORD = "Passw0rd!"
    USERNAME_TO_CHECK = "Nik.Meldon" 
    AD_SEARCH_BASE = "DC=idmtdc,DC=com" 

    check_user_exists(AD_SERVER, AD_USER, AD_PASSWORD, AD_SEARCH_BASE, USERNAME_TO_CHECK)