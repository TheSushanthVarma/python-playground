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