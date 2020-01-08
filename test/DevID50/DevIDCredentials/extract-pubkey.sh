openssl x509 -pubkey -noout  -in IDevID50.cert.pem > IDevID50.pubkey.pem
openssl ec -pubin -inform PEM -in IDevID50.pubkey.pem -conv_form compressed -outform DER -out IDevID50.pubkey.der
#openssl ec -in IDevID50.pubkey.pem -outform DER -out IDevID50.pubkey.der

