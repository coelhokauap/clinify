import json

import pytest

import main


def test_json_invalido_informa_linha_e_coluna(tmp_path):
    arquivo = tmp_path / "invalido.json"
    arquivo.write_text('{"usuario": }', encoding="utf-8")

    with pytest.raises(ValueError, match="linha 1, coluna"):
        main.ler_json(str(arquivo))


def test_arquivo_inexistente_gera_erro_controlado(tmp_path):
    arquivo = tmp_path / "ausente.json"

    with pytest.raises(ValueError, match="Não foi possível abrir"):
        main.ler_json(str(arquivo))


def test_atividades_invalidas_sao_contabilizadas():
    resumo = main.resumir_atividades([
        {"tipo": "estudo"},
        {"tipo": "simulado", "pontuacao": 75},
        {"tipo": "simulado", "pontuacao": 101},
        {"tipo": "simulado", "pontuacao": True},
        "registro inválido",
        {"tipo": "desconhecido"},
    ])

    assert resumo["estudos"] == 1
    assert resumo["simulados"] == 3
    assert resumo["media"] == 75
    assert resumo["melhor"] == 75
    assert resumo["menor"] == 75
    assert resumo["invalidas"] == 4


def test_interacoes_malformadas_nao_interrompem_analise():
    resumo = main.analisar_interacoes([
        {"tipo": "clique", "acao": "Estudos", "data": "data incorreta"},
        {"tipo": "", "acao": 22},
        None,
    ])

    assert resumo["total"] == 1
    assert resumo["tipos"] == {"clique": 1}
    assert resumo["eventos"] == []
    assert resumo["invalidas"] == 2


def test_formato_desconhecido_mostra_mensagem(capsys):
    resultado = main.mostrar_resumo(["não é objeto"])
    saida = capsys.readouterr().out

    assert resultado is False
    assert "Formato inválido" in saida


def test_menu_rejeita_entrada_invalida_e_permite_sair(monkeypatch, capsys):
    respostas = iter(["abc", "9", "²", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(respostas))

    caminho = main.escolher_arquivo(["dados.json"])
    saida = capsys.readouterr().out

    assert caminho is None
    assert saida.count("Digite um número da lista, R para ranking ou 0 para sair.") == 3


def test_menu_abre_opcao_de_ranking(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "r")

    assert main.escolher_arquivo(["dados.json"]) == "ranking"


def test_execucao_trata_json_invalido_sem_interromper(monkeypatch, tmp_path, capsys):
    (tmp_path / "quebrado.json").write_text("{", encoding="utf-8")
    monkeypatch.setattr(main, "PASTA_DADOS", str(tmp_path))
    monkeypatch.setattr("builtins.input", lambda _: "1")

    main.executar()
    saida = capsys.readouterr().out

    assert "Erro:" in saida
    assert "JSON inválido" in saida


def test_ranking_junta_arquivos_e_deduplica_id_da_atividade(tmp_path, monkeypatch, capsys):
    atividade_1 = {"id": "sim-1", "tipo": "simulado", "pontuacao": 80}
    atividade_2 = {"id": "sim-2", "tipo": "simulado", "pontuacao": 100}
    exportacao_1 = {
        "usuario": {"id": "aluno-a", "nome": "Ana"},
        "atividades": [atividade_1, atividade_2],
    }
    exportacao_2 = {
        "usuario": {"id": "aluno-a", "nome": "Ana"},
        "atividades": [atividade_1],
    }
    consolidado = {
        "usuarios": [{
            "id": "aluno-b",
            "nome": "Bia",
            "atividades": [{"id": "sim-3", "tipo": "simulado", "pontuacao": 90}],
        }]
    }

    (tmp_path / "ana-1.json").write_text(json.dumps(exportacao_1), encoding="utf-8")
    (tmp_path / "ana-2.json").write_text(json.dumps(exportacao_2), encoding="utf-8")
    (tmp_path / "turma.json").write_text(json.dumps(consolidado), encoding="utf-8")
    (tmp_path / "quebrado.json").write_text("{", encoding="utf-8")
    monkeypatch.setattr(main, "PASTA_DADOS", str(tmp_path))

    main.mostrar_ranking_arquivos(main.listar_jsons())
    saida = capsys.readouterr().out

    assert "Arquivos analisados           3 de 4" in saida
    assert "Arquivos ignorados            1" in saida
    assert "Ana" in saida and "Bia" in saida
    assert "Notas repetidas entre arquivos" in saida
    assert "quebrado.json" in saida
    assert saida.count("90.0") == 2
