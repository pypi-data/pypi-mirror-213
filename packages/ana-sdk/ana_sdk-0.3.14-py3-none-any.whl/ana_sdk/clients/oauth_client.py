import requests

from ..settings import logger


class OAuthClient:
    """
    Classe para interagir com o cliente OAuth.

    Atributos:
        email (str): Email do usuário.
        _password (str): Senha do usuário.
        keycloak_url (str): URL de obtenção/checagem do token.
        token (dict): Informações completas do token do usuário,
        incluindo o `access_token`.
    """
    token: dict = None

    def __init__(self, email: str, password: str, keycloak_url: str):
        """
        Inicializa um objeto OAuthClient.

        Args:
            email (str): Email do usuário.
            password (str): Senha do usuário.
            keycloak_url (str): URL de obtenção/checagem do token.
        """

        self.email = email
        self._password = password
        self.keycloak_url = keycloak_url

    def _token_is_valid(self) -> bool:
        """
        Checa se o `token` vinculado a essa instância continua válido.

        Returns:
            bool: `True` caso válido, ou `False` caso inválido.
        """

        if not self.token:
            return False

        url = self.keycloak_url + "/userinfo"
        headers = {'Authorization': "Bearer " + self.token["access_token"]}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            user_info: dict = response.json()
            if user_info.get("email"):
                return True
        
        return False

    def get_token(self) -> dict[str, str]:
        """
        Retorna um token válido.

        Checa se existe um token válido associado a esta instância e
        retorna este. Caso contrário, obtém um novo token para o
        usuário associado a instância.

        Returns:
            str: Token de acesso com todas as suas informações.

        Raises:
            requests.HTTPError: Se ocorrer um erro ao fazer a requisição.
        """

        if not self._token_is_valid():
            logger.debug("Nenhum token válido encontrado.")

            data = {
                "client_id": "pontoweb",
                "username": self.email,
                "password": self._password,
                "grant_type": "password"
            }

            logger.debug("Adquirindo novo token...")

            url = self.keycloak_url + "/token"
            response = requests.post(
                url,
                data=data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            response.raise_for_status()
            token = response.json()

            self.token = token

            logger.debug("Novo token adquirido com sucesso!")
        
        return self.token
