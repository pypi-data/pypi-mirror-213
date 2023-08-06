from requests.auth import AuthBase

from .clients.oauth_client import OAuthClient


class RefreshAuth(AuthBase):
    
    def __init__(self, email: str, password: str, oauth_token_full_url: str):
        self.email = email
        self._password = password
        self.env_oauth_token_full_url = oauth_token_full_url
        
        self.oauth_client = OAuthClient(
            self.email,
            self._password,
            self.env_oauth_token_full_url
        )

        # Tenta pegar o token do usuário já na instanciação, levantando
        # exceção caso login não consiga ser feito.
        self.oauth_client.get_token()

    def __call__(self, r):
        access_token = self.oauth_client.get_token()["access_token"]
        r.headers['Authorization'] = "Bearer " + access_token        
        return r
