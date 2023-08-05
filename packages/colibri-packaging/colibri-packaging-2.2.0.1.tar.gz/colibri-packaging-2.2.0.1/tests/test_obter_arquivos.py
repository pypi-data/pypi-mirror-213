import unittest
from colibri_packaging.empacotar import obter_arquivos


class TestesObterListaArquivos(unittest.TestCase):
    def _criar_arquivo_server(self, pattern):
        return dict(
            params_serv="/SP- /SILENT /VERYSILENT /SUPPRESSMSGBOXES /NOCANCEL /NORESTART /SERVIDOR",
            destino="server", _pattern_nome=pattern
        )

    def _criar_arquivo_client(self, pattern):
        return dict(
            params_client="/SP- /SILENT /VERYSILENT /SUPPRESSMSGBOXES /NOCANCEL /NORESTART",
            destino="client", _pattern_nome=pattern
        )

    def test_sem_pattern(self):
        # Arrange
        pasta = r"c:\temp"
        configs = dict(
            arquivos=[
                dict(
                    params_serv="/SP- /SILENT /VERYSILENT /SUPPRESSMSGBOXES /NOCANCEL /NORESTART /SERVIDOR",
                    destino="server", nome="nomecravado.exe"
                ),
                dict(
                    params_client="/SP- /SILENT /VERYSILENT /SUPPRESSMSGBOXES /NOCANCEL /NORESTART",
                    destino="client", nome="nome_client.exe"
                )
            ]
        )
        diretorio = [
            "nomecravado.exe",
            "nome_client.exe"
        ]
        # Act
        lista_zip = obter_arquivos(pasta, configs, diretorio)
        # Assert
        self.assertEqual(
            lista_zip, [
            'c:\\temp\\manifesto.dat',
            'c:\\temp\\nomecravado.exe',
            'c:\\temp\\nome_client.exe'
            ]
        )
        self.assertEqual(
            configs['arquivos'],
            [
                {
                    'destino': 'server', 'nome': 'nomecravado.exe',
                    'params_serv': '/SP- /SILENT /VERYSILENT /SUPPRESSMSGBOXES /NOCANCEL /NORESTART /SERVIDOR'
                },
                {
                    'destino': 'client', 'nome': 'nome_client.exe',
                    'params_client': '/SP- /SILENT /VERYSILENT /SUPPRESSMSGBOXES /NOCANCEL /NORESTART'
                }]
        )

    def test_sem_pattern_cade_o_arquivo(self):
        # Arrange
        pasta = r"c:\temp"
        configs = dict(
            arquivos=[
                dict(
                    params_serv="/SP- /SILENT /VERYSILENT /SUPPRESSMSGBOXES /NOCANCEL /NORESTART /SERVIDOR",
                    destino="server", nome="nomecravado.exe"
                ),
                dict(
                    params_client="/SP- /SILENT /VERYSILENT /SUPPRESSMSGBOXES /NOCANCEL /NORESTART",
                    destino="client", nome="nome_client.exe"
                )
            ]
        )
        diretorio = [
            "nomecravado.exe"
        ]
        # Act & Assert
        with self.assertRaisesRegex(RuntimeError, "Nome arquivo não foi encontrado: nome_client.exe"):
            lista_zip = obter_arquivos(pasta, configs, diretorio)

    def test_obter_arquivos_dupla_referencia(self):
        # Arrange
        pasta = r"c:\temp"
        configs = dict(
            arquivos=[
                self._criar_arquivo_server(".*teste\\.exe\\b"),
                self._criar_arquivo_client(".*teste\\.exe\\b")
            ]
        )
        diretorio = [
            "manifesto.dat",
            "teste.exe"
        ]
        # Act
        lista_zip = obter_arquivos(pasta, configs, diretorio)
        # Assert
        self.assertEqual(lista_zip, [r'c:\temp\manifesto.dat', r'c:\temp\teste.exe'])
        self.assertEqual(
            configs['arquivos'],
            [
                {
                    'destino': 'server', 'nome': 'teste.exe',
                    'params_serv': '/SP- /SILENT /VERYSILENT /SUPPRESSMSGBOXES /NOCANCEL /NORESTART /SERVIDOR'
                },
                {
                    'destino': 'client', 'nome': 'teste.exe',
                    'params_client': '/SP- /SILENT /VERYSILENT /SUPPRESSMSGBOXES /NOCANCEL /NORESTART'
                }]
        )

    def test_scripts_automagicamente(self):
        # Arrange
        pasta = r"c:\temp"
        configs = dict(
            arquivos=[
                self._criar_arquivo_server(".*teste\\.exe\\b"),
                self._criar_arquivo_client(".*teste\\.exe\\b")
            ]
        )
        diretorio = [
            "manifesto.dat",
            "teste.exe",
            "_scripts.zip"
        ]
        # Act
        lista_zip = obter_arquivos(pasta, configs, diretorio)
        # Assert
        self.assertEqual(lista_zip, [r'c:\temp\manifesto.dat', r'c:\temp\teste.exe', r'c:\temp\_scripts.zip'])
        self.assertEqual(
            configs['arquivos'],
            [
                {'destino': 'scripts', 'nome': '_scripts.zip'},
                {
                    'destino': 'server', 'nome': 'teste.exe',
                    'params_serv': '/SP- /SILENT /VERYSILENT /SUPPRESSMSGBOXES /NOCANCEL /NORESTART /SERVIDOR'
                },
                {
                    'destino': 'client', 'nome': 'teste.exe',
                    'params_client': '/SP- /SILENT /VERYSILENT /SUPPRESSMSGBOXES /NOCANCEL /NORESTART'
                }]
        )

    def test_exe_dando_bobeira(self):
        # Arrange
        pasta = r"c:\temp"
        configs = dict(
            arquivos=[
                self._criar_arquivo_server(".*qualquer\\.exe\\b"),
                self._criar_arquivo_client(".*nao_importa\\.exe\\b")
            ]
        )
        diretorio = [
            "manifesto.dat",
            "qualquer.exe",
            "ignoto.exe"
        ]
        # Act & Assert
        with self.assertRaisesRegex(RuntimeError,
                "Arquivo executável desconhecido na pasta de empacotamento: ignoto.exe"):
            obter_arquivos(pasta, configs, diretorio)

    def test_pattern_nao_identificado(self):
        # Arrange
        pasta = r"c:\temp"
        configs = dict(
            arquivos=[
                self._criar_arquivo_server(".*qualquer\\.exe\\b"),
                self._criar_arquivo_client(".*teste\\.exe\\b")
            ]
        )
        diretorio = [
            "manifesto.dat",
            "teste.exe"
        ]
        # Act & Assert
        with self.assertRaisesRegex(RuntimeError,
                r"Pattern de nome arquivo não foi encontrado: \.\*qualquer\\\.exe\\b"):
            obter_arquivos(pasta, configs, diretorio)

    def test_deve_manter_a_ordem_pelo_tipo(self):
        # Arrange
        pasta = r"c:\temp"
        configs = dict(
            arquivos=[
                self._criar_arquivo_server(".*primeiro_server\\.exe\\b"),
                self._criar_arquivo_client(".*primeiro_client\\.exe\\b"),
                self._criar_arquivo_server(".*segundo_server\\.exe\\b"),
                self._criar_arquivo_client(".*segundo_client\\.exe\\b"),
                self._criar_arquivo_server(".*terceiro_server\\.exe\\b"),
                self._criar_arquivo_client(".*terceiro_client\\.exe\\b"),
            ]
        )
        diretorio = [
            "terceiro_server.exe",
            "primeiro_server.exe",
            "manifesto.dat",
            "segundo_client.exe",
            "terceiro_client.exe",
            "segundo_server.exe",
            "primeiro_client.exe",
        ]
        # Act
        lista_zip = obter_arquivos(pasta, configs, diretorio)

        # Assert
        self.assertEqual(
            lista_zip,
            [
                "c:\\temp\\manifesto.dat",
                "c:\\temp\\terceiro_server.exe",
                "c:\\temp\\primeiro_server.exe",
                "c:\\temp\\segundo_client.exe",
                "c:\\temp\\terceiro_client.exe",
                "c:\\temp\\segundo_server.exe",
                "c:\\temp\\primeiro_client.exe",
            ]
        )
        nomes_arquivos = [a['nome'] for a in configs['arquivos']]
        self.assertEqual(
            nomes_arquivos,
            [
                "primeiro_server.exe",
                "segundo_server.exe",
                "terceiro_server.exe",
                "primeiro_client.exe",
                "segundo_client.exe",
                "terceiro_client.exe",
            ]
        )


if __name__ == '__main__':
    unittest.main()
