from ldap3 import Server, Connection, ALL

def test_ad_connection():
    """Test connection to Active Directory server"""
    # AD server settings
    AD_SERVER = "172.16.30.142"
    AD_USER = "CN=Administrator,CN=Users,DC=idmtdc,DC=com"
    AD_PASSWORD = "Passw0rd!"

    # Connect to AD server
    server = Server(AD_SERVER, port=389, get_info=ALL)
    conn = Connection(
        server,
        user=AD_USER,
        password=AD_PASSWORD
    )

    try:
        if conn.bind():
            print("Successfully connected to AD server")
        else:
            print(f"Connection failed: {conn.result}")
    except Exception as e:
        print(f"Error connecting to AD server: {str(e)}")
    finally:
        conn.unbind()
        print("Disconnected from AD server")

if __name__ == "__main__":
    test_ad_connection()