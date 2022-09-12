require 'oauth2'
 
callback = "[CALLBACK_URL]"
app_id = "[APPLICATION_ID]"
 
secret = "[SECRET]"
client = OAuth2::Client.new(app_id, secret, site: "[AUTHORIZATION_SERVER]")
client.auth_code.authorize_url(redirect_uri: callback)
 
 
code="[CODE]"
access = client.auth_code.get_token( code, redirect_uri: callback)
access.get("/api/user").parsed
 
puts access.token

#Then, you can use the token to access the resource server with :
# curl -H 'Authorization: Bearer [TOKEN]' [RESOURCE_SERVER]/api/keys --dump-header -

