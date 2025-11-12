# ISSUE: MultiAgentWithTools

## Objetivo

Criar a feature `MultiAgentWithTools` utilizando o MicrosoftAgentFramework. A feature deve demonstrar uma arquitetura com múltiplos agentes que podem orquestrar ferramentas (tools) para resolver tarefas compostas.

## Descrição

Este issue serve como lista de tarefas inicial (to-do) para criar a feature. O repositório já contém exemplos do `MicrosoftAgentFrameworkExamples`; a nova feature ficará organizada sob `MicrosoftAgentFrameworkExamples/AgentsWithMcp`.

## Lista de tarefas (To-do)

1. Criar branch `feature/MultiAgentWithTools` (local e push para origin).
2. Scaffold inicial:
   - Criar um diretório `AgentsWithTools` ou estender `AgentsWithMcp` com:
     - `multi_agent_manager.py` - orquestrador de agentes
     - `agent_worker.py` - classe base para agentes que usam tools
     - `tools/` - implementações de ferramentas (ex.: SearchTool, CalculatorTool)
     - `examples/` - pequeno script `run_demo.py` mostrando fluxo end-to-end
3. Configuração e dependências: atualizar `requirements.txt` se necessário e documentar como ativar o virtualenv.
4. Tests mínimos:
   - Teste unitário para orquestração básica (um agente delega para outro via ferramentas).
   - Teste para uma tool simulada (mock) garantindo contrato I/O.
5. Documentação:
   - Atualizar `README.md` ou criar `docs/MultiAgentWithTools.md` com instruções de uso.
6. Abrir PR da branch `feature/MultiAgentWithTools` para `main` com descrição e checklist.

## Critérios de aceitação

- Projeto builda localmente e demo `run_demo.py` roda sem erros num ambiente Python 3.8+.
- Há pelo menos um teste automatizado cobrindo fluxo happy-path.
- Código organizado, com README explicando como executar a demo e os testes.

## Notas de implementação (MicrosoftAgentFramework)

- Reutilizar código em `MicrosoftAgentFrameworkExamples/AgentsWithMcp` quando aplicável.
- Modelar as tools como componentes desacoplados que expõem uma interface simples (ex.: execute(input) -> output).
- Pensar na serialização de mensagens entre agentes (JSON simples) para facilitar logs e testes.

## Checklist

- [ ] Branch criada e push
- [ ] Arquivos scaffold criados
- [ ] Dependências documentadas
- [ ] Tests adicionados
- [ ] Docs atualizados

---
_Issue gerado automaticamente pelo assistente em 2025-11-12._
