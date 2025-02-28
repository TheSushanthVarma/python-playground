from ldap3 import Server, Connection, ALL, SUBTREE, Tls
from ldap3.core.tls import Tls
import random
import string
from datetime import datetime
import ssl

def generate_password(min_length=7):
    """Generate a password that meets AD complexity requirements"""
    import string
    import random
    
    # Ensure we have at least one of each required character type
    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice('!@#$%^&*()_+-=[]{}|;:,.<>?')
    
    # Calculate remaining length needed
    remaining_length = max(0, min_length - 4)
    
    # Fill the rest with random characters from all allowed types
    all_chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
    rest = ''.join(random.choice(all_chars) for _ in range(remaining_length))
    
    # Combine all parts and shuffle
    password = lowercase + uppercase + digit + special + rest
    password_list = list(password)
    random.shuffle(password_list)
    return ''.join(password_list)

def change_user_password(username):
    """Change password for given username and return new credentials"""

    AD_SERVER = "172.16.30.142"
    AD_USER = "CN=Administrator,CN=Users,DC=idmtdc,DC=com"
    AD_PASSWORD = "Passw0rd!"
    AD_SEARCH_BASE = "DC=idmtdc,DC=com"

    new_password = generate_password(min_length=7)
    
    # Try standard LDAP first (port 389)
    tls = Tls(validate=ssl.CERT_NONE)
    server = Server(
        AD_SERVER, 
        port=636,  # Changed to standard LDAP port
        use_ssl=True,  # Disabled SSL initially
        get_info=ALL
    )
    
    conn = Connection(
        server,
        user=AD_USER,
        password=AD_PASSWORD,
        authentication='SIMPLE',
        auto_bind=True  # Added auto_bind
    )

    try:
        if conn.bind():
            print("Connected to AD server")
            
            search_filter = f'(&(objectClass=user)(sAMAccountName={username}))'
            conn.search(
                AD_SEARCH_BASE,
                search_filter,
                search_scope=SUBTREE,
                attributes=['cn', 'distinguishedName', 'pwdLastSet']
            )
            
            if len(conn.entries) == 0:
                raise Exception(f"User {username} not found")
                
            user_dn = conn.entries[0].distinguishedName.value
            
            # Encode the password in UTF-16LE format
            encoded_password = f'"{new_password}"'.encode('utf-16-le')
            
            # Change the password using the encoded format
            modify_password_result = conn.extend.microsoft.modify_password(
                user_dn, 
                encoded_password,
                old_password=None
            )
            
            if not modify_password_result:
                raise Exception(f"Failed to change password: {conn.result}")
            
            # Force refresh to get the updated pwdLastSet
            conn.search(
                AD_SEARCH_BASE,
                search_filter,
                search_scope=SUBTREE,
                attributes=['cn', 'distinguishedName', 'pwdLastSet']
            )
            
            pwd_last_set = conn.entries[0].pwdLastSet.value
            
            if pwd_last_set:
                # pwdLastSet is already a datetime object, no need for conversion
                pass
            else:
                pwd_last_set = "Never"

            conn.extend.microsoft.modify_password(user_dn, new_password)
            print(f"Password changed successfully for {username}")
            
            return {
                "username": username,
                "new_password": new_password,
                "last_password_change": pwd_last_set
            }
            
        else:
            raise Exception(f"Connection failed: {conn.result}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    finally:
        conn.unbind()

def main():
    username = input("Enter username to reset password: ")
    result = change_user_password(username)
    
    if result:
        print("\nPassword Reset Summary:")
        print("-" * 30)
        print(f"Username: {result['username']}")
        print(f"New Password: {result['new_password']}")
        print(f"Last Password Change: {result['last_password_change']}")
        print("-" * 30)
    else:
        print("Password reset failed")

if __name__ == "__main__":
    main()
