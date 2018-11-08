import aws

from requests_oauthlib import OAuth2Session


"""App Configuration"""
class Auth:
    """Google Project Credentials"""
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email']


    def get_google_auth(url, state=None, token=None):

        redirect_uri=url+"gAuthCallback"
  #      redirect_uri="https://filemediaonline.com/gAuthCallback"
        if token:
            return OAuth2Session(aws.getGoogleClientId(), token=token)
        if state:
            return OAuth2Session(aws.getGoogleClientId(),
                    state=state,redirect_uri=redirect_uri)
        oauth = OAuth2Session(aws.getGoogleClientId(),
                redirect_uri=redirect_uri, scope=Auth.SCOPE)
        return oauth




#if __name__ == "__main__":
#     ssl_dir: str = os.path.dirname(__file__)+'/ssl'
#     key_path: str = os.path.join(ssl_dir, 'server.key')
#     crt_path: str = os.path.join(ssl_dir, 'server.crt')
#     ssl_context: tuple = (crt_path, key_path)
#     application.debug = True 
#     sslify = SSLify(application, permanent=True) 
#     application.run(ssl_context=ssl_context)

