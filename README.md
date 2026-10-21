# Clinify

<p align="left">
  <img src="https://skillicons.dev/icons?i=html,css,js,python,git,github,vscode&theme=light" alt="HTML, CSS, JavaScript, Python, Git, GitHub e VS Code" />
</p>

O Clinify é uma plataforma de apoio à formação médica com estudos, questões, casos clínicos simulados, acompanhamento de desempenho e áreas para estudantes, professores e administradores.

## Grupo

| Integrante      | RM     |
| --------------- | ------ |
| Anita Palhares  | 571264 |
| Vitória Kereski | 569438 |
| Kauã Coelho     | 568665 |
| Carlos Alberto  | 571841 |

# Computational Thinking With Python

Esta entrega integra os dados exportados pelo Front Web do Clinify com uma análise em Python. O programa lê os arquivos JSON da pasta `Computational Thinking With Python/dados`, resume o uso das funções principais e apresenta os resultados organizados no terminal.

## Entrega

O programa está concentrado em `main.py` e utiliza somente as bibliotecas padrão `os`, `json` e `datetime`. Os testes automatizados usam `pytest`; a aplicação não depende dessa biblioteca para funcionar.

Funcionalidades implementadas:

- lista arquivos `.json` e permite escolher um pelo número;
- lê exportações individuais e históricos consolidados;
- contabiliza interações por tipo, ação mais frequente, até cinco telas mais acessadas e dia com mais atividade;
- resume estudos, simulados, média e maior/menor pontuação válida entre 0 e 100;
- calcula o período observado, o tempo total e o tempo médio entre cliques em funções principais: simulação, estudos, casos e salvar dados;
- calcula a média do intervalo antes de cada função;
- mostra a jornada registrada e a maior pausa entre funções;
- gera feedback geral com base nos estudos e nas pontuações registradas;
- apresenta ranking geral de notas entre todos os JSONs da pasta, agrupado por aluno;
- também mostra ranking dentro de históricos consolidados;
- valida arquivos e formatos, informa sucesso ou erros de leitura e estrutura;
- ignora registros inconsistentes e contabiliza os itens ignorados;
- encerra após apresentar o resultado e não altera os arquivos exportados.

O ranking geral reúne as notas de todos os arquivos e identifica o estudante por ID, e-mail ou nome. Atividades com o mesmo ID são contadas uma vez mesmo se aparecerem em várias exportações. O ranking usa a média das pontuações válidas dos simulados; médias iguais compartilham a mesma posição. Alunos sem notas válidas ficam fora da classificação. O feedback considera médias a partir de 80 como bom desempenho, de 60 a menos de 80 como desempenho em desenvolvimento e abaixo de 60 como necessidade de reforço. Sem notas válidas, o programa informa que não há dados suficientes para avaliar. A leitura de QR Code, login e eventos de navegação não entra no cálculo de tempo. Os tempos representam intervalos entre cliques registrados, não o tempo ativo para concluir uma tarefa. Para medir a duração real de uma tarefa, o Front Web precisa registrar eventos de início e conclusão.

## Integração com o Front Web

O JavaScript registra no navegador interações, módulos de estudo e simulações concluídas pelo estudante. Ao selecionar **Salvar dados**, o site cria um novo arquivo `clinify_dados_DATA_E_HORA.json`. Os arquivos anteriores são preservados.

O Python procura todos os arquivos `.json` dentro de `Computational Thinking With Python/dados` e permite escolher um para análise. O resumo aparece em quatro seções: **Uso do app**, **Tempo e funções principais**, **Atividades** e **Feedback geral**. Caminhos longos de páginas são apresentados pelo nome do arquivo para facilitar a leitura. A opção `R` no menu calcula o ranking geral usando todos os arquivos válidos da pasta.

A integração entre o front-end e a análise ocorre por arquivo JSON, sem API ou banco de dados. O servidor HTTP local indicado abaixo serve apenas os arquivos estáticos do front-end durante a demonstração.

## Como testar passo a passo

### 1. Abra o terminal na raiz do projeto

Os próximos comandos devem ser executados na pasta que contém `Front Web` e `Computational Thinking With Python`.

Para confirmar que está no local correto, execute:

```bash
ls
```

As duas pastas devem aparecer na lista.

### 2. Inicie o Front Web

No primeiro terminal, execute:

```bash
python3 -m http.server 8000 --directory "Front Web/clinify-front-web"
```

Mantenha esse terminal aberto e acesse no navegador:

<http://localhost:8000/index.html>

### 3. Gere atividades para o arquivo

1. Entre com a conta de estudante.
2. Abra **Estudos**, responda às questões e finalize um módulo.
3. Abra **Simulação Clínica**, escolha um caso, converse com o paciente virtual e finalize a simulação.
4. Use outras áreas do site caso queira registrar mais interações.

Essas informações ficam salvas no navegador até serem exportadas.

### 4. Salve o JSON

1. Na barra lateral, selecione **Salvar dados**.
2. Quando o navegador pedir uma pasta, escolha `Computational Thinking With Python/dados`.
3. Confirme que apareceu uma mensagem com o nome do novo arquivo.

Chrome e Edge permitem selecionar a pasta `dados` e gravar diretamente nela. Caso o navegador baixe o JSON em `Downloads`, mova o arquivo manualmente para:

```text
Computational Thinking With Python/dados/
```

Cada uso do botão cria um arquivo novo. O nome contém a data e o horário para evitar que uma exportação substitua outra.

### 5. Confirme que o arquivo está na pasta correta

Em outro terminal, ainda na raiz do projeto, execute:

```bash
ls "Computational Thinking With Python/dados"
```

Deve aparecer pelo menos um arquivo terminado em `.json`.

### 6. Execute o programa Python

Na raiz do projeto, execute:

```bash
python3 "Computational Thinking With Python/main.py"
```

Escolha o número do arquivo para analisar, digite `R` para montar o ranking geral de todos os arquivos ou `0` para sair. A análise individual encerra automaticamente depois do resumo. Exemplo de saída individual (os valores dependem do JSON selecionado):

```text
CLINIFY | Análise de uso

Arquivo: clinify_dados_2026-10-20T22-02-29-805Z.json
============================================================
Exportação individual | Gerada: 20/10/2026 às 22:02

Aluno: Estudante Clinify (estudante)

USO DO APP
------------------------------------------------------------
  Interações                    200
  Por tipo                      clique: 81, formulario: 8, navegacao: 111
  Ação mais frequente           Clinify | Home (34)
  Telas mais acessadas:
  casos.html                    40 acessos
  home_e.html                   34 acessos
  perfil.html                   26 acessos
  simulacao.html                21 acessos
  estudos.html                  19 acessos
  Dia com mais atividade        22/09/2026 (129 interações)

TEMPO E FUNÇÕES PRINCIPAIS
------------------------------------------------------------
  Período                       21/09/2026 às 23:49:03 até 20/10/2026 às 22:02:29
  Tempo total                   694h 13min 26s
  Média entre funções           15h 46min 40s
  Jornada: Salvar dados → Casos clínicos → Estudos
           Casos clínicos → Salvar dados → Estudos
           Simulação clínica → Estudos
           Simulação clínica → Salvar dados
           Casos clínicos → Salvar dados → Estudos
           Simulação clínica → Estudos
           Simulação clínica → Estudos → Casos clínicos
           Simulação clínica → Estudos
           Simulação clínica → Estudos
           Simulação clínica → Casos clínicos
           Salvar dados → Casos clínicos → Salvar dados
  Média antes de cada função:
  Salvar dados                  1min 30s
  Casos clínicos                1min 5s
  Estudos                       2h 16min 1s
  Simulação clínica             95h 51min 14s
  Maior pausa                   670h 42min 37s (Casos clínicos → Simulação clínica)

ATIVIDADES
------------------------------------------------------------
  Estudos                       0
  Simulados                     1
  Média dos simulados           64.0
  Maior pontuação               64
  Menor pontuação               64

FEEDBACK GERAL
------------------------------------------------------------
  Desempenho em desenvolvimento; revise os temas com menor pontuação.
============================================================
```

Para ver o ranking geral, execute o programa e digite `R` no menu. O resultado mostra a média por aluno, o número de notas válidas e quantos arquivos contribuíram para cada linha. As notas são agrupadas pelo ID do aluno, e-mail ou nome; atividades com o mesmo ID são contadas uma vez entre exportações. Exportações individuais também mostram o feedback daquele estudante. Os tempos e indicadores variam conforme os horários e as atividades capturados em cada exportação. Uma pausa longa entre funções pode incluir tempo sem uso do sistema; ela não representa necessariamente o tempo ativo de uma tarefa. Para validar o fluxo de estudo e simulação, gere uma nova exportação após concluir atividades no Front Web.

Se o JSON estiver inválido ou o arquivo não puder ser aberto, o programa apresenta uma mensagem de erro controlada e encerra sem modificar os dados. Para conferir o tratamento de erro, teste com uma cópia do JSON e deixe essa cópia inválida; preserve o arquivo original.

### 7. Execute os testes automatizados

Os testes usam `pytest`, que não é necessário para executar a aplicação. Caso ainda não esteja instalado, instale-o com:

```bash
python3 -m pip install pytest
```

Depois, execute na pasta `Computational Thinking With Python`:

```bash
python3 -m pytest -q
```

Os testes usam `assert` para verificar validação de JSON e atividades, tratamento de interações inconsistentes, respostas do menu e ranking entre arquivos, incluindo JSON corrompido e atividades repetidas. As exceções são tratadas no programa com `try/except`; os `assert` verificam nos testes os resultados esperados. Esses testes automatizam o fluxo do terminal e não substituem sessões de usabilidade com estudantes e professores. A suíte atual contém 9 testes.

## Estrutura

```text
Computational Thinking With Python/
├── main.py
├── test_main.py
└── dados/
```

# Edge Computing

O módulo de Edge Computing implementa um motor local de avaliação clínica em C++17. Ele utiliza `cpp-httplib` para o servidor HTTP e `nlohmann/json` para receber e devolver dados em JSON. Um cliente Python permite validar a comunicação entre as duas linguagens.

## Visão geral da arquitetura

```text
Cliente de teste Python
          │
          │ HTTP REST e JSON — porta 8080
          ▼
Clinify Edge Engine (C++17)
├── servidor HTTP local
├── leitura e criação de JSON
└── avaliação de critérios clínicos
    ├── acolhimento
    ├── anamnese
    ├── sinais de alerta
    └── segurança da conduta
```

O serviço funciona de forma local e independente. O arquivo `cliente_teste.py` demonstra o envio de uma fala clínica para o servidor e a leitura da resposta em JSON.

## Estrutura

```text
backend/Edge Computing/
├── CMakeLists.txt
├── main.cpp
├── cliente_teste.py
├── httplib.h
└── json.hpp
```

## Rotas disponíveis

### `GET /api/saude`

Verifica se o serviço está em execução.

```json
{
  "servico": "Clinify Edge C++",
  "status": "online",
  "porta": 8080
}
```

### `POST /api/avaliar`

Recebe a fala do estudante e os critérios já alcançados na sessão.

Exemplo de entrada:

```json
{
  "fala": "Olá Maria, quando começou essa dor e você teve febre?",
  "criterios_anteriores": []
}
```

Exemplo de resposta:

```json
{
  "feedback": "Investigou o histórico e características da queixa. Atenção adequada aos sinais de alerta graves.",
  "ganho_pontos": 18,
  "novos_criterios": ["anamnese", "sinais de alerta"]
}
```

Um corpo com JSON inválido recebe o status `400` e uma mensagem de erro.

## Como executar

Pré-requisitos:

- compilador com suporte a C++17;
- CMake 3.15 ou superior;
- Python 3 para executar o cliente de teste.

No Windows com MinGW, abra o terminal na raiz do projeto e compile o serviço:

```cmd
cd "backend\Edge Computing"
mkdir build
cd build
cmake -G "MinGW Makefiles" ..
cmake --build .
```

Inicie o servidor no mesmo diretório:

```cmd
clinify_edge.exe
```

O serviço ficará disponível em `http://127.0.0.1:8080`. Em outro terminal, execute o cliente Python:

```cmd
cd "backend\Edge Computing"
python cliente_teste.py
```

O script consulta a rota de saúde e envia uma avaliação clínica de exemplo, exibindo no terminal as respostas JSON produzidas pelo servidor C++.

# Front-End Design e Web Development

Esta entrega da Sprint 3 apresenta a interface visual e interativa do Clinify para estudante, professor e administrador.

## Front-End Design

A interface foi desenvolvida para manter identidade visual, clareza, responsividade e facilidade de uso.

Principais entregas:

- HTML semântico e hierarquia organizada de títulos;
- identidade visual consistente entre os três perfis;
- estilos separados por responsabilidade e variáveis em `assets/css/root.css`;
- layouts com Flexbox, Grid e media queries;
- adaptação para celular, tablet e desktop;
- formulários com rótulos, validações e mensagens de retorno;
- foco visível e navegação por teclado;
- menus, cards, tabelas, modais e estados de interação;
- barra lateral com ícones e interação visual minimalista;
- área recolhível de sinais vitais em todas as simulações;
- ícones para pressão arterial, frequência cardíaca, temperatura e dor;
- notebook de anotações clínicas com salvamento automático.

O link do Figma não foi localizado no projeto. A revisão visual utiliza como referência a identidade já implementada no Clinify.

## Web Development

O JavaScript controla as interações, os componentes compartilhados e a persistência local da plataforma.

Principais entregas:

- scripts separados por perfil e responsabilidade;
- componentes compartilhados de navegação, mensagens, ícones e layout;
- login para estudante, professor e administrador;
- buscas, filtros, formulários, cards e modais interativos;
- persistência de sessão, perfil, progresso e atividades com `localStorage`;
- separação dos dados por usuário;
- registro de estudos e simulações concluídas;
- exportação de um novo JSON a cada uso do botão **Salvar dados**;
- geração de QR Code da sala pelo professor;
- leitura do QR Code por câmera ou imagem pelo estudante;
- acesso à sala com etapas e feedback de preenchimento;
- salas clínicas entre abas do mesmo navegador;
- paciente virtual integrado à simulação clínica.

O paciente virtual utiliza regras e palavras-chave definidas em `assets/js/student/agent.js`. Ele responde de acordo com o caso, reconhece critérios da conversa, oferece feedback educacional e atualiza a pontuação. O funcionamento é local, sem API e sem inteligência artificial generativa.

## Como executar

Na raiz do projeto, execute:

```bash
python3 -m http.server 8000 --directory "Front Web/clinify-front-web"
```

Acesse:

<http://localhost:8000/index.html>

## Contas de acesso

Todas utilizam a senha `123456`.

| Perfil        | E-mail                |
| ------------- | --------------------- |
| Administrador | admin@clinify.com     |
| Professor     | professor@clinify.com |
| Estudante     | 12345678900@gmail.com |

## Roteiro de uso

1. Entre como estudante.
2. Navegue pelas áreas de estudos, casos, desempenho e perfil.
3. Conclua uma atividade de estudo.
4. Abra uma simulação e converse com o paciente virtual.
5. Consulte os sinais vitais e escreva no notebook de anotações.
6. Finalize a simulação e recarregue a página para conferir a persistência.
7. Clique em **Salvar dados** para gerar um novo JSON usado pela entrega de Python.
8. Entre como professor e administrador para demonstrar os outros fluxos.

## Estrutura

```text
Front Web/
├── index.html
├── estudante/
├── professor/
├── administrador/
├── assets/
│   ├── css/
│   ├── img/
│   └── js/
└── README.md
```

## Observações

- O login não representa autenticação segura de produção.
- O `localStorage` não sincroniza dados entre dispositivos.
- As salas funcionam entre abas do mesmo navegador e origem.
- O paciente virtual não realiza diagnóstico médico.
- A versão publicada deve ser conferida após cada atualização local.

## Links

Repositório do GitHub

- https://github.com/coelhokauap/clinify

Deploy no Vercel

- https://clinifylxp.vercel.app/

Protótipo no Figma

- https://www.figma.com/design/5XBp7dz9bmiCKe95phM3xM/Clinify---prototipo?node-id=115-51&t=rlj9wU2Wilee0FHX-1

## Uso de Inteligência Artificial

A Inteligência Artificial (IA) foi utilizada como ferramenta de apoio durante o desenvolvimento do projeto, auxiliando na comparação dos requisitos da Sprint 3 com o código, organização dos arquivos e componentes, correção de referências e melhorias nas interações e acessibilidade. A IA também auxiliou na preparação e revisão deste README.

As alterações foram acompanhadas de verificações no código e testes de navegação. A IA foi utilizada apenas como suporte ao desenvolvimento, e o agente da simulação não realiza diagnósticos.
