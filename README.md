# Simulador de Catraca de Ônibus

Aplicação web que simula a catraca de um ônibus com leitor de cartão. O usuário aproxima o cartão, o sistema valida, cobra a passagem e libera ou recusa a passagem. Também há uma tela de recarga de créditos.

## Escopo

### Fase 1 (atual)
- Tela de simulação da catraca (catraca, leitor de cartão e validador)
- Tela de recarga (inicialmente adiciona saldo direto, sem pagamento real)
- API em Python
- Banco de dados PostgreSQL

### Fora do escopo por enquanto
- Integração temporal (desconto ou gratuidade em viagens seguidas)
- Pagamento real na recarga (será feito por último)

## Stack

| Camada | Tecnologia |
| Backend | Python + FastAPI (sujeito a mudanças) |
| Banco | PostgreSQL |
| Frontend | A definir |

## Regras de negócio

1. Cada passagem é cobrada **inteira**, sem integração.
2. O valor da tarifa fica em configuração: `TARIFA = a definir`.
3. O cartão precisa existir, estar ativo e pertencer a um usuário válido.
4. Se o saldo for maior ou igual à tarifa: desconta, registra a viagem e libera a catraca.
5. Se o saldo for insuficiente: recusa e informa o saldo atual.
6. Cartão inexistente ou bloqueado: recusa com mensagem apropriada.
7. O desconto do saldo e o registro da viagem acontecem na mesma transação do banco, com lock na linha do cartão, para evitar cobrança duplicada.
8. Recarga: soma o valor ao saldo e registra a recarga.

## Telas

- **Simulação da catraca:** seleção do cartão/usuário que vai aproximar, botão de aproximar, resultado (liberado ou recusado), saldo restante.
- **Recarga:** seleção do cartão, valor, confirmação, saldo atualizado.

## Endpoints (rascunho)

| Método | Rota | Descrição |
|---|---|---|
| POST | `/catraca/validar` | Recebe `card_id`, valida, cobra e retorna o resultado |
| GET | `/cartoes/{id}` | Dados e saldo do cartão |
| POST | `/cartoes/{id}/recarga` | Adiciona saldo ao cartão |
| GET | `/cartoes/{id}/viagens` | Histórico de viagens |

Exemplo de resposta de `POST /catraca/validar`:

```json
{
  "liberado": true,
  "mensagem": "Passagem liberada",
  "saldo_restante": 12.30
}
```

## Modelo do banco (rascunho)

- `usuarios`: id, nome, ativo
- `cartoes`: id, usuario_id, saldo, status
- `viagens`: id, cartao_id, valor_cobrado, data_hora
- `recargas`: id, cartao_id, valor, data_hora

## Como rodar

```bash
# a preencher quando o projeto tiver a primeira versão
```

## Organização do time

- Uma branch por funcionalidade (`feature/funcionalidade`)
- Mudanças entram na `main` via pull request, revisado pela outra pessoa
- Tarefas organizadas em quadro (ex: GitHub Projects, Trello)
- Padrão de commits: a combinar

## Decisões em aberto

- Valor da tarifa
- Tecnologia do frontend
- Padrão de commits

## Desenvolvedores

- [Marcos Costa](https://github.com/marcoladashub)
- [Enzo Festa](https://github.com/festa-enzo)