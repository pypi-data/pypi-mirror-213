from requests import Session

from ..clients.base_client import BaseClient
from ..settings import logger


class RPAAPIClient(BaseClient):
    """
    Classe para interagir com o cliente RPA API.

    Atributos:
        session (requests.Session): Sessão para realizar requisições.
        _base_url (str): URL base da API do RPA.
    """

    def __init__(self, session: Session, base_url: str):
        """
        Inicializa um objeto RPAAPIClient.

        Args:
            session (requests.Session): Sessão para realizar requisições.
            base_url (str): URL base da API do Dashboard.
        """

        self.session = session
        self._base_url = base_url

    def get_comandos(self) -> list[dict]:
        """
        Obtém os comandos disponíveis.

        Returns:
            list[dict]: Lista de comandos disponíveis.
        """

        url = self._base_url + "/jobs"
        return self._get_all_content(url)

    def get_json_schema(self, mope: str) -> dict:
        """
        Obtém o esquema JSON para um determinado comando.

        Args:
            mope (str): Identificador do comando.

        Returns:
            dict: Esquema JSON do comando.
        """

        url = self._base_url + f"/jobs/{mope}/schema"
        return self._get_all_content(url)

    def get_task(self, task_id: str) -> dict:
        """
        Obtém informações sobre uma tarefa específica.

        Args:
            task_id (str): ID da tarefa.

        Returns:
            dict: Informações da tarefa.
        """

        url = self._base_url + f"/tasks/{task_id}"
        return self._get_all_content(url)

    def get_tasks(self, **query_string_parameters) -> dict:
        """
        Obtém as tarefas com base nos parâmetros de string de consulta fornecidos.

        Args:
            **query_string_parameters: Parâmetros de string de consulta para filtrar as tarefas.

        Returns:
            dict: Tarefas correspondentes aos parâmetros de string de consulta.
        """

        query_string = self._dict_to_query_string(query_string_parameters)
        url = self._base_url + f"/tasks" + query_string
        return self._get_all_content(url)

    def get_task_status(self, task_id: str) -> dict:
        """
        Obtém o status de uma tarefa específica.

        Args:
            task_id (str): ID da tarefa.

        Returns:
            dict: Status da tarefa.
        """

        url = self._base_url + f"/jobs/{task_id}/status"
        return self._get_all_content(url)

    def execute_command(self, mope: str, data: dict) -> dict:
        """
        Executa um comando.

        Args:
            mope (str): Identificador do comando.
            data (dict): Dados para o comando.

        Returns:
            dict: Resultado da execução do comando.

        Raises:
            requests.HTTPError: Se ocorrer um erro ao fazer a requisição.
        """
        
        logger.info(f"Executando comando de MOPE [{mope}]...")
        logger.debug(data)

        url = self._base_url + f"/jobs/{mope}"
        response = self.session.post(url=url, json=data)
        response.raise_for_status()

        content = response.json()

        return content
