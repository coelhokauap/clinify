import json
import os
from datetime import datetime, timezone

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
    print("R. Ranking geral de notas (todos os arquivos)")
    print("0. Sair")

    while True:
        escolha = input("\nEscolha um arquivo: ").strip()
        if escolha == "0":
            return None
        if escolha.lower() == "r":
            return "ranking"
        if escolha.isdecimal() and 1 <= int(escolha) <= len(arquivos):
            return os.path.join(PASTA_DADOS, arquivos[int(escolha) - 1])
        print("Digite um número da lista, R para ranking ou 0 para sair.")


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


def converter_data(valor):
    if not isinstance(valor, str):
        return None
    try:
        data = datetime.fromisoformat(valor.replace("Z", "+00:00"))
        if data.tzinfo:
            return data.astimezone(timezone.utc).replace(tzinfo=None)
        return data
    except ValueError:
        return None


def formatar_duracao(segundos):
    segundos = max(0, segundos)
    if segundos < 60:
        return f"{segundos:.1f}s"
    segundos = round(segundos)
    minutos, segundos = divmod(segundos, 60)
    horas, minutos = divmod(minutos, 60)
    if horas:
        return f"{horas}h {minutos}min {segundos}s"
    if minutos:
        return f"{minutos}min {segundos}s"
    return f"{segundos}s"


def eh_funcao_principal(item):
    if item.get("tipo") != "clique":
        return False
    acao = item.get("acao")
    if not isinstance(acao, str):
        return False
    acao = acao.lower()
    palavras_chave = ("simula", "estudo", "caso", "salvar")
    return any(palavra in acao for palavra in palavras_chave)


def nome_funcao_principal(acao):
    texto = acao.lower()
    if "simula" in texto:
        return "Simulação clínica"
    if "estudo" in texto:
        return "Estudos"
    if "caso" in texto:
        return "Casos clínicos"
    if "salvar" in texto:
        return "Salvar dados"
    return acao


def resumir_atividades(atividades):
    if not isinstance(atividades, list):
        return {"estudos": 0, "simulados": 0, "notas_validas": 0, "media": None, "melhor": None, "menor": None, "invalidas": 1}

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
    melhor = max(notas) if notas else None
    menor = min(notas) if notas else None
    return {
        "estudos": estudos, "simulados": simulados, "notas_validas": len(notas), "media": media,
        "melhor": melhor, "menor": menor, "invalidas": invalidas,
    }


def analisar_interacoes(interacoes):
    if not isinstance(interacoes, list):
        return {"total": 0, "tipos": {}, "acoes": {}, "paginas": {}, "eventos": [], "dias": {}, "invalidas": 1}

    tipos, acoes, paginas, dias = {}, {}, {}, {}
    eventos = []
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
        pagina = item.get("pagina")
        if isinstance(pagina, str) and pagina.strip():
            paginas[pagina] = paginas.get(pagina, 0) + 1
        data = converter_data(item.get("data"))
        if data:
            dia = data.strftime("%Y-%m-%d")
            dias[dia] = dias.get(dia, 0) + 1
        if data and eh_funcao_principal(item):
            eventos.append((data, item.get("acao")))
    return {
        "total": sum(tipos.values()), "tipos": tipos, "acoes": acoes,
        "paginas": paginas, "eventos": eventos, "dias": dias, "invalidas": invalidas,
    }


def imprimir_secao(titulo):
    print(f"\n{titulo}")
    print("-" * 60)


def imprimir_indicador(rotulo, valor):
    print(f"  {rotulo:<29} {valor}")


def imprimir_jornada(jornada, largura=55):
    linha = "  Jornada: "
    for indice, funcao in enumerate(jornada):
        item = (" → " if indice else "") + funcao
        if len(linha) + len(item) > largura and linha.strip() != "Jornada:":
            print(linha)
            linha = "           " + funcao
        else:
            linha += item
    print(linha)


def gerar_feedback(atividades):
    if atividades["simulados"] and atividades["media"] is not None:
        media = atividades["media"]
        if media >= 80:
            return "Bom desempenho nos simulados; mantenha a rotina de estudos."
        if media >= 60:
            return "Desempenho em desenvolvimento; revise os temas com menor pontuação."
        return "Pontuação baixa nos simulados; recomende revisão e acompanhamento."
    if atividades["simulados"]:
        return "Há simulados registrados, mas faltam pontuações válidas para avaliar o desempenho."
    if atividades["estudos"]:
        return "Há estudos registrados, mas faltam notas de simulados para avaliar o desempenho."
    return "Ainda não há atividades suficientes para avaliar o progresso."


def mostrar_usuario(usuario, interacoes=None, atividades=None):
    nome = usuario.get("nome")
    perfil = usuario.get("perfil")
    nome = nome.strip() if isinstance(nome, str) and nome.strip() else "Nome não informado"
    perfil = perfil.strip() if isinstance(perfil, str) and perfil.strip() else "não informado"

    uso = analisar_interacoes(interacoes if interacoes is not None else usuario.get("interacoes", []))
    resultado = resumir_atividades(atividades if atividades is not None else usuario.get("atividades", []))
    print(f"\nAluno: {nome} ({perfil})")
    imprimir_secao("USO DO APP")
    imprimir_indicador("Interações", uso["total"])
    if uso["tipos"]:
        tipos = ", ".join(f"{tipo}: {qtd}" for tipo, qtd in sorted(uso["tipos"].items()))
        imprimir_indicador("Por tipo", tipos)
    if uso["acoes"]:
        acao, quantidade = max(uso["acoes"].items(), key=lambda item: item[1])
        imprimir_indicador("Ação mais frequente", f"{acao} ({quantidade})")
    if uso["paginas"]:
        print("  Telas mais acessadas:")
        telas = sorted(uso["paginas"].items(), key=lambda item: (-item[1], item[0]))[:5]
        for pagina, quantidade in telas:
            imprimir_indicador(pagina.rsplit("/", 1)[-1], f"{quantidade} acessos")
    if uso["dias"]:
        dia, quantidade = max(uso["dias"].items(), key=lambda item: item[1])
        dia_formatado = datetime.strptime(dia, "%Y-%m-%d").strftime("%d/%m/%Y")
        imprimir_indicador("Dia com mais atividade", f"{dia_formatado} ({quantidade} interações)")
    if len(uso["eventos"]) >= 2:
        eventos = sorted(uso["eventos"], key=lambda evento: evento[0])
        inicio, fim = eventos[0][0], eventos[-1][0]
        intervalos = [(eventos[i][0] - eventos[i - 1][0]).total_seconds()
                      for i in range(1, len(eventos))]
        tempo_total = (fim - inicio).total_seconds()
        media_tempo = sum(intervalos) / len(intervalos)
        imprimir_secao("TEMPO E FUNÇÕES PRINCIPAIS")
        inicio_texto = inicio.strftime("%d/%m/%Y às %H:%M:%S")
        fim_texto = fim.strftime("%d/%m/%Y às %H:%M:%S")
        imprimir_indicador("Período", f"{inicio_texto} até {fim_texto}")
        imprimir_indicador("Tempo total", formatar_duracao(tempo_total))
        imprimir_indicador("Média entre funções", formatar_duracao(media_tempo))
        jornada = []
        for _, acao in eventos:
            funcao = nome_funcao_principal(acao)
            if not jornada or jornada[-1] != funcao:
                jornada.append(funcao)
        imprimir_jornada(jornada)
        tempos_por_funcao = {}
        for indice in range(1, len(eventos)):
            funcao = nome_funcao_principal(eventos[indice][1])
            tempos_por_funcao.setdefault(funcao, []).append(intervalos[indice - 1])
        print("  Média antes de cada função:")
        for funcao, tempos in tempos_por_funcao.items():
            imprimir_indicador(funcao, formatar_duracao(sum(tempos) / len(tempos)))
        maior_pausa = max(range(len(intervalos)), key=lambda indice: intervalos[indice])
        primeira = nome_funcao_principal(eventos[maior_pausa][1])
        segunda = nome_funcao_principal(eventos[maior_pausa + 1][1])
        imprimir_indicador("Maior pausa", f"{formatar_duracao(intervalos[maior_pausa])} ({primeira} → {segunda})")
    elif uso["eventos"]:
        imprimir_secao("TEMPO E FUNÇÕES PRINCIPAIS")
        imprimir_indicador("Dados de tempo", "São necessários dois cliques com data válida")
    imprimir_secao("ATIVIDADES")
    imprimir_indicador("Estudos", resultado["estudos"])
    imprimir_indicador("Simulados", resultado["simulados"])
    if resultado["media"] is not None:
        imprimir_indicador("Média dos simulados", resultado["media"])
        imprimir_indicador("Maior pontuação", resultado["melhor"])
        imprimir_indicador("Menor pontuação", resultado["menor"])
    invalidos = uso["invalidas"] + resultado["invalidas"]
    if invalidos:
        imprimir_indicador("Registros inválidos ignorados", invalidos)
    if not resultado["estudos"] and not resultado["simulados"]:
        print("  Sem atividades para avaliar aprendizagem.")
    imprimir_secao("FEEDBACK GERAL")
    print("  " + gerar_feedback(resultado))


def mostrar_ranking(usuarios):
    ranking = []
    sem_notas = 0
    for usuario in usuarios:
        atividades = resumir_atividades(usuario.get("atividades", []))
        if atividades["media"] is None:
            sem_notas += 1
            continue
        nome = usuario.get("nome")
        nome = nome.strip() if isinstance(nome, str) and nome.strip() else "Nome não informado"
        ranking.append((nome, atividades["media"], atividades["notas_validas"]))

    imprimir_secao("RANKING | MÉDIA DOS SIMULADOS")
    if not ranking:
        print("  Ainda não há pontuações válidas para montar o ranking.")
    else:
        ranking.sort(key=lambda item: (-item[1], item[0].lower()))
        posicao = 0
        media_anterior = None
        for indice, (nome, media, simulados) in enumerate(ranking, start=1):
            if media != media_anterior:
                posicao = indice
                media_anterior = media
            imprimir_indicador(f"{posicao}. {nome}", f"média {media:.1f} | {simulados} notas válidas")
    if sem_notas:
        print(f"  Alunos sem pontuação válida fora do ranking: {sem_notas}")


def mostrar_ranking_arquivos(arquivos):
    alunos = {}
    arquivos_invalidos = []
    arquivos_validos = 0

    for nome_arquivo in arquivos:
        caminho = os.path.join(PASTA_DADOS, nome_arquivo)
        try:
            dados = ler_json(caminho)
        except ValueError:
            arquivos_invalidos.append(nome_arquivo)
            continue

        registros = []
        if isinstance(dados, dict) and isinstance(dados.get("usuario"), dict):
            registros.append((dados["usuario"], dados.get("atividades", [])))
        elif isinstance(dados, dict) and isinstance(dados.get("usuarios"), list):
            for usuario in dados["usuarios"]:
                if isinstance(usuario, dict):
                    registros.append((usuario, usuario.get("atividades", [])))
        else:
            arquivos_invalidos.append(nome_arquivo)
            continue

        arquivos_validos += 1
        for indice, (usuario, atividades) in enumerate(registros):
            identificador = usuario.get("id") or usuario.get("email") or usuario.get("nome")
            if isinstance(identificador, str) and identificador.strip():
                chave_aluno = identificador.strip().casefold()
            else:
                chave_aluno = f"{nome_arquivo}:{indice}"
            nome = usuario.get("nome")
            if not isinstance(nome, str) or not nome.strip():
                nome = "Nome não informado"

            aluno = alunos.setdefault(chave_aluno, {"nome": nome.strip(), "notas": {}, "arquivos": set()})
            aluno["arquivos"].add(nome_arquivo)
            if not isinstance(atividades, list):
                continue
            for indice_atividade, atividade in enumerate(atividades):
                if not isinstance(atividade, dict) or atividade.get("tipo") != "simulado":
                    continue
                nota = atividade.get("pontuacao")
                if not isinstance(nota, (int, float)) or isinstance(nota, bool) or not 0 <= nota <= 100:
                    continue
                id_atividade = atividade.get("id")
                if isinstance(id_atividade, str) and id_atividade.strip():
                    chave_nota = f"id:{id_atividade.strip()}"
                else:
                    chave_nota = f"{nome_arquivo}:{indice}:{indice_atividade}"
                aluno["notas"][chave_nota] = nota

    ranking = []
    sem_notas = 0
    for aluno in alunos.values():
        notas = list(aluno["notas"].values())
        if not notas:
            sem_notas += 1
            continue
        media = round(sum(notas) / len(notas), 1)
        ranking.append((aluno["nome"], media, len(notas), len(aluno["arquivos"])))

    imprimir_secao("RANKING GERAL | TODOS OS ARQUIVOS")
    imprimir_indicador("Arquivos analisados", f"{arquivos_validos} de {len(arquivos)}")
    if arquivos_invalidos:
        imprimir_indicador("Arquivos ignorados", len(arquivos_invalidos))
        for nome in arquivos_invalidos:
            print("    " + nome)
    if not ranking:
        print("  Ainda não há notas válidas de simulados para classificar.")
    else:
        ranking.sort(key=lambda item: (-item[1], item[0].casefold()))
        posicao = 0
        media_anterior = None
        print("\n  POS.  ALUNO                         MÉDIA  NOTAS  ARQUIVOS")
        print("  " + "-" * 58)
        for indice, (nome, media, quantidade, quantidade_arquivos) in enumerate(ranking, start=1):
            if media != media_anterior:
                posicao = indice
                media_anterior = media
            print(f"  {posicao:<5} {nome[:28]:<29} {media:>5.1f} {quantidade:>6} {quantidade_arquivos:>9}")
    if sem_notas:
        imprimir_indicador("Alunos sem notas válidas", sem_notas)
    print("\n  Notas repetidas entre arquivos foram contadas uma vez quando tinham o mesmo ID de atividade.")


def mostrar_resumo(dados):
    if not isinstance(dados, dict):
        print("Formato inválido: a raiz do JSON deve ser um objeto.")
        return False

    if isinstance(dados.get("usuario"), dict):
        print("Exportação individual | Gerada:", formatar_data(dados.get("gerado_em")))
        mostrar_usuario(dados["usuario"], dados.get("interacoes", []), dados.get("atividades", []))
        return True

    if isinstance(dados.get("usuarios"), list):
        usuarios = [item for item in dados["usuarios"] if isinstance(item, dict)]
        print("Histórico consolidado | Atualizado:", formatar_data(dados.get("atualizado_em")))
        print(f"Alunos: {len(usuarios)} | Registros ignorados: {len(dados['usuarios']) - len(usuarios)}")
        for numero, usuario in enumerate(usuarios, start=1):
            print(f"\n{'=' * 20} ALUNO {numero} {'=' * 20}")
            mostrar_usuario(usuario)
        total_interacoes = 0
        total_estudos = 0
        total_simulados = 0
        notas = []
        for usuario in usuarios:
            uso = analisar_interacoes(usuario.get("interacoes", []))
            atividades = resumir_atividades(usuario.get("atividades", []))
            total_interacoes += uso["total"]
            total_estudos += atividades["estudos"]
            total_simulados += atividades["simulados"]
            if atividades["media"] is not None:
                notas.append((atividades["media"], atividades["notas_validas"]))
        print("\nRESUMO GERAL")
        print("Interações:", total_interacoes)
        print("Estudos:", total_estudos, "| Simulados:", total_simulados)
        if notas:
            quantidade_notas = sum(qtd for _, qtd in notas)
            media_geral = round(sum(media * qtd for media, qtd in notas) / quantidade_notas, 1)
            print("Média geral dos simulados:", media_geral)
        mostrar_ranking(usuarios)
        return True

    print("Formato não reconhecido. Esperado: 'usuario' ou lista 'usuarios'.")
    return False


def executar():
    print("\nCLINIFY | Análise de uso\n")
    arquivos = listar_jsons()
    if not arquivos:
        print("Nenhum arquivo JSON foi encontrado na pasta dados (ou a pasta não pôde ser lida).")
        return

    try:
        caminho = escolher_arquivo(arquivos)
        if caminho is None:
            print("Programa encerrado.")
            return
        if caminho == "ranking":
            mostrar_ranking_arquivos(arquivos)
            return
        dados = ler_json(caminho)
        print(f"\nArquivo: {os.path.basename(caminho)}")
        print("=" * 60)
        mostrar_resumo(dados)
        print("=" * 60)
    except ValueError as erro:
        print("\nErro:", erro)
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado pelo usuário.")


if __name__ == "__main__":
    executar()
