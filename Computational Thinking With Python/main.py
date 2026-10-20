import json
import os
from datetime import datetime


PASTA_DADOS = os.path.join(os.path.dirname(__file__), "dados")


def listar_jsons():
    try:
        arquivos = []
        for nome in os.listdir(PASTA_DADOS):
            caminho = os.path.join(PASTA_DADOS, nome)
            if nome.lower().endswith(".json") and os.path.isfile(caminho):
                arquivos.append(nome)
        return sorted(arquivos, key=str.lower)
    except OSError:
        return []


def escolher_arquivo(arquivos):
    print("Arquivos disponíveis na pasta dados:\n")
    for numero, nome in enumerate(arquivos, start=1):
        print(f"{numero}. {nome}")
    print("0. Sair")

    while True:
        escolha = input("\nEscolha um arquivo: ").strip()
        if escolha == "0":
            return None
        if escolha.isdigit() and 1 <= int(escolha) <= len(arquivos):
            return os.path.join(PASTA_DADOS, arquivos[int(escolha) - 1])
        print("Digite um número exibido na lista.")


def ler_json(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError as erro:
        raise ValueError(f"JSON inválido na linha {erro.lineno}, coluna {erro.colno}.") from erro
    except (OSError, UnicodeError) as erro:
        raise ValueError("Não foi possível abrir ou decodificar o arquivo.") from erro


def formatar_data(valor):
    if not isinstance(valor, str) or not valor:
        return "não informada"
    try:
        data = datetime.fromisoformat(valor.replace("Z", "+00:00"))
        return data.strftime("%d/%m/%Y às %H:%M")
    except ValueError:
        return f"inválida ({valor})"


def resumir_atividades(atividades):
    if not isinstance(atividades, list):
        return {"estudos": 0, "simulados": 0, "media": None, "invalidas": 1}

    estudos = simulados = invalidas = 0
    notas = []
    for atividade in atividades:
        if not isinstance(atividade, dict):
            invalidas += 1
            continue
        tipo = atividade.get("tipo")
        if tipo == "estudo":
            estudos += 1
        elif tipo == "simulado":
            simulados += 1
            nota = atividade.get("pontuacao")
            if isinstance(nota, (int, float)) and not isinstance(nota, bool) and 0 <= nota <= 100:
                notas.append(nota)
            elif nota is not None:
                invalidas += 1
        elif tipo is not None:
            invalidas += 1

    media = round(sum(notas) / len(notas), 1) if notas else None
    return {"estudos": estudos, "simulados": simulados, "media": media, "invalidas": invalidas}


def analisar_interacoes(interacoes):
    if not isinstance(interacoes, list):
        return {"total": 0, "tipos": {}, "acoes": {}, "invalidas": 1}

    tipos, acoes = {}, {}
    invalidas = 0
    for item in interacoes:
        if not isinstance(item, dict):
            invalidas += 1
            continue
        tipo = item.get("tipo")
        if isinstance(tipo, str) and tipo.strip():
            tipos[tipo] = tipos.get(tipo, 0) + 1
        else:
            invalidas += 1
        acao = item.get("acao")
        if isinstance(acao, str) and acao.strip():
            acoes[acao] = acoes.get(acao, 0) + 1
    return {"total": sum(tipos.values()), "tipos": tipos, "acoes": acoes, "invalidas": invalidas}


def mostrar_usuario(usuario, interacoes=None, atividades=None):
    nome = usuario.get("nome")
    perfil = usuario.get("perfil")
    print("Aluno:", nome.strip() if isinstance(nome, str) and nome.strip() else "Nome não informado")
    print("Perfil:", perfil.strip() if isinstance(perfil, str) and perfil.strip() else "não informado")

    uso = analisar_interacoes(interacoes if interacoes is not None else usuario.get("interacoes", []))
    resultado = resumir_atividades(atividades if atividades is not None else usuario.get("atividades", []))
    print("Interações registradas:", uso["total"])
    if uso["tipos"]:
        print("Interações por tipo:", ", ".join(f"{tipo}: {qtd}" for tipo, qtd in sorted(uso["tipos"].items())))
    if uso["acoes"]:
        acao, quantidade = max(uso["acoes"].items(), key=lambda item: item[1])
        print(f"Ação mais frequente: {acao} ({quantidade})")
    print("Estudos concluídos:", resultado["estudos"])
    print("Simulados concluídos:", resultado["simulados"])
    print("Média dos simulados:", resultado["media"] if resultado["media"] is not None else "sem notas válidas")
    invalidos = uso["invalidas"] + resultado["invalidas"]
    if invalidos:
        print("Registros ignorados por inconsistência:", invalidos)
    if not resultado["estudos"] and not resultado["simulados"]:
        print("Observação: o arquivo não contém atividades; não é possível avaliar aprendizagem.")


def mostrar_resumo(dados):
    if not isinstance(dados, dict):
        print("Formato inválido: a raiz do JSON deve ser um objeto.")
        return False

    if isinstance(dados.get("usuario"), dict):
        print("Tipo: dados exportados pelo site")
        print("Gerado em:", formatar_data(dados.get("gerado_em")))
        mostrar_usuario(dados["usuario"], dados.get("interacoes", []), dados.get("atividades", []))
        return True

    if isinstance(dados.get("usuarios"), list):
        usuarios = [item for item in dados["usuarios"] if isinstance(item, dict)]
        print("Tipo: histórico consolidado")
        print("Atualizado em:", formatar_data(dados.get("atualizado_em")))
        print(f"Total de alunos: {len(usuarios)} (registros ignorados: {len(dados['usuarios']) - len(usuarios)})")
        for numero, usuario in enumerate(usuarios, start=1):
            print(f"\nAluno {numero}")
            mostrar_usuario(usuario)
        return True

    print("Formato não reconhecido. Esperado: 'usuario' ou lista 'usuarios'.")
    return False


def executar():
    print("\nClinify - análise dos dados de uso\n")
    arquivos = listar_jsons()
    if not arquivos:
        print("Nenhum arquivo JSON foi encontrado na pasta dados (ou a pasta não pôde ser lida).")
        return

    try:
        caminho = escolher_arquivo(arquivos)
        if caminho is None:
            print("Programa encerrado.")
            return
        dados = ler_json(caminho)
        print("\nArquivo lido:", os.path.basename(caminho))
        print("-" * 55)
        mostrar_resumo(dados)
        print("-" * 55)
        print("Análise concluída.")
    except ValueError as erro:
        print("\nErro:", erro)
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado pelo usuário.")


if __name__ == "__main__":
    executar()
