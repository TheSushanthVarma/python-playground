from ldap3 import Server, Connection, ALL, SUBTREE, Tls
from ldap3.core.tls import Tls
import ssl

def get_password_policy():
    """Query and return the domain password policy"""
    
    # AD Connection settings
       # AD Connection settings
    AD_SERVER = "172.16.30.142"
    # Change the username format to domain\username
    AD_USER = "idmtdc\\Administrator"  # Note the double backslash
    AD_PASSWORD = "Passw0rd!"
    AD_SEARCH_BASE = "DC=idmtdc,DC=com"
    
    # Setup connection
    tls = Tls(validate=ssl.CERT_NONE)
    server = Server(
        AD_SERVER, 
        port=389,
        use_ssl=False,
        get_info=ALL
    )
    
    conn = Connection(
        server,
        user=AD_USER,
        password=AD_PASSWORD,
        authentication='NTLM',
        auto_bind=True
    )
    
    try:
        # Search for domain policy
        conn.search(
            AD_SEARCH_BASE,
            '(objectClass=domainDNS)',
            attributes=[
                'minPwdLength',
                'pwdHistoryLength',
                'maxPwdAge',
                'minPwdAge',
                'pwdProperties',
                'lockoutThreshold',
                'lockoutDuration',
                'pwdLastSet',
                'lockoutObservationWindow'
            ]
        )
        
        if len(conn.entries) > 0:
            policy = conn.entries[0]
            pwd_properties = int(policy.pwdProperties.value)
            
            complexity_requirements = []
            if pwd_properties & 1:
                complexity_requirements.append("Password must be complex")
            if pwd_properties & 2:
                complexity_requirements.append("Admin can't change password")
            if pwd_properties & 8:
                complexity_requirements.append("Machine account password change disabled")
            if pwd_properties & 16:
                complexity_requirements.append("User can't change password")
            
            print("\nPassword Policy Settings:")
            print("-" * 50)
            print(f"Minimum Password Length: {policy.minPwdLength.value}")
            print(f"Password History Length: {policy.pwdHistoryLength.value}")
            # Check the type of the attribute values
            print(f"Type of maxPwdAge: {type(policy.maxPwdAge.value)}")
            print(f"Type of minPwdAge: {type(policy.minPwdAge.value)}")
            print(f"Type of lockoutDuration: {type(policy.lockoutDuration.value)}")
            print(f"Type of lockoutObservationWindow: {type(policy.lockoutObservationWindow.value)}")

            # Convert the values to integers if they are not already
            max_pwd_age = int(policy.maxPwdAge.value.total_seconds()) if hasattr(policy.maxPwdAge.value, 'total_seconds') else int(policy.maxPwdAge.value)
            min_pwd_age = int(policy.minPwdAge.value.total_seconds()) if hasattr(policy.minPwdAge.value, 'total_seconds') else int(policy.minPwdAge.value)
            lockout_duration = int(policy.lockoutDuration.value.total_seconds()) if hasattr(policy.lockoutDuration.value, 'total_seconds') else int(policy.lockoutDuration.value)
            lockout_observation_window = int(policy.lockoutObservationWindow.value.total_seconds()) if hasattr(policy.lockoutObservationWindow.value, 'total_seconds') else int(policy.lockoutObservationWindow.value)

            print(f"Maximum Password Age (days): {abs(max_pwd_age) / 86400}")
            print(f"Minimum Password Age (days): {abs(min_pwd_age) / 86400}")
            print("\nComplexity Requirements:")
            for req in complexity_requirements:
                print(f"- {req}")
            print(f"\nAccount Lockout Threshold: {policy.lockoutThreshold.value}")
            print(f"Lockout Duration (minutes): {abs(lockout_duration) / 60}")
            print(f"Lockout Observation Window (minutes): {abs(lockout_observation_window) / 60}")
            print("-" * 50)
            
        else:
            print("No policy information found")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        conn.unbind()

if __name__ == "__main__":
    get_password_policy() 