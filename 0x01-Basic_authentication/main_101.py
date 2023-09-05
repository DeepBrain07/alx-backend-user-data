from api.v1.auth.auth import Auth

obj = Auth()
print(obj.require_auth('/api/v1/users', ["/api/v1/stat*"]))
print(obj.require_auth('/api/v1/status', ["/api/v1/stat*"]))
print(obj.require_auth('/api/v1/stats', ["/api/v1/stat*"]))