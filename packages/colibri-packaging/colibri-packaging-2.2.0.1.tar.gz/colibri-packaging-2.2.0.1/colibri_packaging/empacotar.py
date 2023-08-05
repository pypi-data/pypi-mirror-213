# coding: utf-8
import json
import logging
import os
import subprocess
import re
import shutil
from functools import cmp_to_key
try:
    from scripts.versao_banco import obter_versao_db_scripts
except ImportError:
    obter_versao_db_scripts = None

CAM_7ZA = os.path.join(os.path.split(__file__)[0] or os.getcwd(), '7za.exe')
MANIFESTO_SERVER = 'manifesto.server'
MANIFESTO_LOCAL = 'manifesto.local'
MANIFESTO = 'manifesto.dat'
EXTENSAO_PACOTE = '.cmpkg'
RE_ARQ_SCRIPT = re.compile(r'_scripts(\d{0,2})(\S+)?\.zip')
EXTENSAO_ARQ_SCRIPT = '.zip'
PACOTE = 'nome'
VERSAO = 'versao'
SCHEMA = 'schema'
ARQUIVOS = 'arquivos'
NOME_ARQ = 'nome'
MENSAGEM = 'mensagem'
DESTINO = 'destino'
DEVELOP = 'develop'
INNOSERV = 'innoserv'
BASES_COMPATIVEIS = 'versoes_bases'
ARQ_PACOTE = 'pacote'
ARQ_SCRIPTS = 'scripts'
ARQ_CLIENT = 'client'
ARQ_SERVIDOR = 'server'
ARQ_SHARED = 'shared'
PASTA_QA = r'd:\Builder\QA'


logger = logging.getLogger('empacotar')

DEFAULTS_PACOTE = dict(
    versao="1.0.0.0"
)
_ordem_arquivo = dict()


def _acha_ordem(arq):
    def _obter_sequencia():
        def_ret = _ordem_arquivo.get((arq['nome'], arq["destino"]), 0)
        if arq['destino'] == ARQ_SCRIPTS:
            match = RE_ARQ_SCRIPT.match(arq['nome'])
            if match and match.group(1):
                def_ret = int(match.group(1))
        return def_ret

    ordem = {
        ARQ_PACOTE: -1000,
        ARQ_SCRIPTS: 0,
        ARQ_SHARED: 1000,
        ARQ_SERVIDOR: 2000,
        ARQ_CLIENT: 3000
    }

    return ordem.get(arq['destino']) + _obter_sequencia()


def _acha_tipo(arqorg):
    arqorg = arqorg.lower()
    if RE_ARQ_SCRIPT.match(arqorg):
        return ARQ_SCRIPTS


def _obter_chaves_arquivo(dict_chaves):
    return {chave: valor for chave, valor in dict_chaves.items() if
            chave != 'nome' and not chave.startswith('_')}


def _excluir_com_prefixo(pasta, prefixo):
    for arq in os.listdir(pasta):
        if arq.endswith(EXTENSAO_PACOTE) and arq.startswith(prefixo):
            try:
                os.unlink(os.path.join(pasta, arq))
            except Exception:
                logger.exception('Falha ao remover cmpkg anterior: ' + arq)


def obter_arquivos(pasta, manifesto_dat, lista_no_diretorio):
    lista_zip = list((os.path.join(pasta, MANIFESTO),))
    lista_anterior = manifesto_dat.get(ARQUIVOS, list())

    manifesto_dat[ARQUIVOS] = list()

    def criar_arq_(arq, chaves=None):
        dictarq = dict(
            nome=arq
        )

        if chaves is not None:
            dictarq.update(_obter_chaves_arquivo(chaves))

        if dictarq.get('destino') is None:
            dictarq['destino'] = _acha_tipo(arq)

        if dictarq.get('destino'):
            manifesto_dat[ARQUIVOS].append(dictarq)
            completo = os.path.join(pasta, arq)
            if completo not in lista_zip:
                lista_zip.append(completo)
        elif arq.lower().endswith('.exe'):
            raise RuntimeError(
                f"Arquivo executável desconhecido na pasta de empacotamento: {arq}"
            )
        return dictarq

    def temos_um_match(arq, a):
        return ('_pattern_nome' in a and re.match(a['_pattern_nome'], arq)) or \
               ('nome' in a and a['nome'].lower() == arq.lower())

    for arq in lista_no_diretorio:
        if arq.lower() == MANIFESTO:
            continue

        criado = False
        # se eu encontrar a definição do arquivo na lista anterior,
        # uso o que eu encontrar
        for pos, a in enumerate(lista_anterior):
            # arquivo está marcado com pattern? Adiciono
            if temos_um_match(arq, a):
                if "__count" in a:
                    a["__count"] += 1
                else:
                    a["__count"] = 1
                dictarq = criar_arq_(arq, _obter_chaves_arquivo(a))
                _ordem_arquivo[(arq, dictarq['destino'])] = pos
                criado = True

        if not criado:
            dictarq = criar_arq_(arq)
            _ordem_arquivo[(arq, dictarq['destino'])] = 0

    for a in lista_anterior:
        if '_pattern_nome' in a and "__count" not in a:
            raise RuntimeError(
                f"Pattern de nome arquivo não foi encontrado: {a['_pattern_nome']}"
            )
        elif 'nome' in a and "__count" not in a:
            raise RuntimeError(
                f"Nome arquivo não foi encontrado: {a['nome']}"
            )

    manifesto_dat[ARQUIVOS].sort(
        key=cmp_to_key(
            lambda arq1, arq2: _acha_ordem(arq1) - _acha_ordem(arq2)
        )
    )
    return lista_zip


def _atualizar_versoes_bases(manifesto_dat, kwargs):
    OBTER = '_obter_versao_do_json'
    versoes_bases = [
        dict(schema=a[0], versao=a[1]) for a in kwargs.pop('versoes_bases', [])
    ]
    schemas = [a[SCHEMA] for a in versoes_bases]

    for base in manifesto_dat.get(BASES_COMPATIVEIS, []):
        obter = base.get(OBTER)
        if obter:
            if obter_versao_db_scripts is None:
                raise RuntimeError('Biblioteca de scripts indisponivel')
            schema, versao = obter_versao_db_scripts(obter)
            base[SCHEMA] = schema
            base[VERSAO] = versao
            del base[OBTER]
        if base.get(SCHEMA) and base.get(SCHEMA) not in schemas:
            versoes_bases.append(base)

    if len(versoes_bases):
        manifesto_dat[BASES_COMPATIVEIS] = versoes_bases


def _obter_manifesto_do_template(pasta):
    manifesto_usado = os.path.join(pasta, MANIFESTO_SERVER)
    try:
        with open(manifesto_usado, 'r', encoding='utf-8-sig') as arq:
            manifesto_dat = json.load(arq)
            logger.info('usando ' + MANIFESTO_SERVER)
    except IOError:
        try:
            manifesto_usado = os.path.join(pasta, MANIFESTO_LOCAL)
            with open(manifesto_usado, 'r', encoding='utf-8-sig') as arq:
                manifesto_dat = json.load(arq)
                logger.info('usando ' + MANIFESTO_LOCAL)
        except IOError:
            logger.info(u'template de manifesto não encontrado. gerando...')
            manifesto_dat = DEFAULTS_PACOTE.copy()
    except Exception as e:
        logger.exception(f'Erro ao processar manifesto {manifesto_usado}')
        print('Erro ao processar: ' + manifesto_usado)
        print(e)
        raise
    return manifesto_dat


def empacotar(pasta, pasta_saida, senha, **kwargs):
    manifesto_dat = _obter_manifesto_do_template(pasta)

    # Atualizo o manifesto com o que foi passado pela linha de comando
    _atualizar_versoes_bases(manifesto_dat, kwargs)
    manifesto_dat.update(kwargs)

    arquivos = obter_arquivos(pasta, manifesto_dat, os.listdir(pasta))

    with open(os.path.join(pasta, MANIFESTO), 'w') as manifile:
        json.dump(manifesto_dat, manifile, indent=2)

    prefixo = manifesto_dat[PACOTE].replace(' ', '') + '_'
    nome_cmpkg = prefixo + \
        manifesto_dat[VERSAO].replace(' ', '').replace('.', '_') + \
        EXTENSAO_PACOTE
    saida = os.path.join(pasta_saida, nome_cmpkg)

    _excluir_com_prefixo(pasta_saida, prefixo)
    zipar(saida, arquivos=arquivos, senha=senha)
    arquivo_cmpkg = os.path.join(os.getcwd(), saida)

    # Suporte a uma pasta para os QAs
    _copiar_para_qa(nome_cmpkg, prefixo, saida)

    return arquivo_cmpkg


def _copiar_para_qa(nome_cmpkg, prefixo, saida):
    if os.environ.get('QA', '').lower() != 'true':
        return

    if os.environ.get('ALOHA', '').lower() == 'true':
        logger.info('Arquivo não será gerado na pasta de QA pois ALOHA=true')
        return

    pasta_QA = os.environ.get('PASTA_QA', PASTA_QA)
    if not os.path.exists(pasta_QA):
        logger.error(f'PASTA_QA nao encontrada: {pasta_QA}')
        return

    _excluir_com_prefixo(pasta_QA, prefixo)
    try:
        print(f'Copiando para pasta de QA: {pasta_QA}')
        shutil.copyfile(saida, os.path.join(pasta_QA, nome_cmpkg))
    except Exception:
        logger.exception(
            f'Falha ao copiar arquivo {saida} para a pasta {pasta_QA}'
        )


def zipar(destino, arquivos=None, pasta=None, senha=''):
    destino = os.path.join(os.getcwd(), destino)

    cmdline = [
        CAM_7ZA,
        'a',
        '-tzip',
        '-mx9',
        '-y'
    ]
    if senha:
        cmdline.append('-p' + senha)
    cmdline.append(destino)

    prevdir = None
    if arquivos:
        cmdline = cmdline + arquivos
    elif pasta:
        prevdir = os.getcwd()
        pasta = os.path.join(os.getcwd(), pasta)
        os.chdir(pasta)

    logger.debug('comando gerado: "{}"'.format(cmdline))
    subprocess.call(cmdline)
    if prevdir:
        os.chdir(prevdir)
