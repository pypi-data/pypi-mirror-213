ENV = "PRODUCTION"

if ENV == "PRODUCTION":
    HOST_API = "https://api.solidityscan.com/private"
    HOST = "https://solidityscan.com"

else:
    #  HOST="http://localhost:5002/private"
    HOST_API = "https://api-develop.solidityscan.com/external/private"
    HOST = "https://develop.solidityscan.com"
