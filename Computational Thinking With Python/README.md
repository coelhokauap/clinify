# Clinify — análise de dados em Python

O programa lê os arquivos JSON exportados pelo front-end e salvos na pasta `dados/`. Ele exibe indicadores de uso e atividades do estudante sem alterar os arquivos de origem.

## Requisitos

- Python 3
- Bibliotecas usadas: `json`, `os` e `datetime`, todas incluídas no Python. Não é necessário instalar pacotes.

## Como executar

No terminal, abra a pasta do projeto e rode:

```bash
python3 main.py
```

Escolha o número do arquivo JSON que deseja analisar. Digite `0` para sair.

## O que o programa mostra

- Data e hora de geração da exportação.
- Nome e perfil do estudante.
- Total de interações e quantidade por tipo.
- A ação mais frequente.
- Quantidade de estudos e simulados concluídos.
- Média das pontuações válidas de simulados, considerando notas numéricas entre 0 e 100.
- Quantidade de registros inconsistentes ignorados.

O programa reconhece exportações individuais, com as chaves `usuario`, `interacoes` e `atividades`, e históricos consolidados com a chave `usuarios`.

## Testar as funcionalidades

O arquivo `dados/clinify_dados_2026-09-23T19-15-44-078Z.json` pode ser usado para conferir a leitura de uma exportação real. Execute o programa e escolha esse arquivo. O resumo esperado inclui 7 interações: 3 cliques, 1 formulário e 3 navegações. Como essa exportação não contém atividades, estudos e simulados aparecem como zero e o programa informa que não é possível avaliar aprendizagem.

Para testar outros casos, crie uma cópia do JSON dentro de `dados/` e altere somente a cópia:

1. **Média de simulados:** adicione à lista `atividades` dois objetos de simulado com pontuações 80 e 90. A média exibida deve ser 85.
2. **Registro inválido:** adicione um item que não seja um objeto à lista `interacoes`, ou uma pontuação de simulado fora da faixa de 0 a 100. O programa deve ignorar o registro inconsistente e contabilizá-lo.
3. **JSON inválido:** remova uma vírgula ou uma aspa da cópia. O programa deve informar a linha e a coluna do erro.
4. **Formato desconhecido:** remova ou renomeie as chaves esperadas. O programa deve informar que não reconheceu o formato.

Apague as cópias de teste ao terminar para não confundi-las com exportações reais.

## Evidência disponível e limites

A execução com o JSON fornecido confirmou que o programa consegue ler uma exportação do front-end e resumir suas 7 interações. Esse arquivo contém apenas um usuário e nenhuma atividade. Portanto, ele não comprova teste de usabilidade nem resultados de aprendizagem. Para documentar essa validação, o grupo deve reunir feedback e registros reais de sessões com usuários, além de exportações que contenham atividades, evitando incluir dados pessoais desnecessários.
