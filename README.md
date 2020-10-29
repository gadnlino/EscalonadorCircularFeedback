# EscalonadorCircularFeedback
Projeto final da matéria de Sistemas Operacionais(SO 1) do período 2020.PLE do curso de Ciencia da Computação - UFRJ

#### Plano

Iremos fazer em python (se ficar trivial, o Daniel vai refazer em C)

## Premissas:

Iremos parametrizar:
- O número de processos 
- O quantum de cada processos
- **Tempo da E/S de disco**: 17, baixa prioridade
- **Tempo da E/S de fita magnética**: 39, alta prioridade
- **Tempo da E/S da impressora**: 420, alta prioridade

## Informações dos processos

O pid vai ser gerado quando o processo entrar fila de prontos  
Informações do PCB vão estar na nossa estrutura de dados(classe Processo).

## Escalonador

Escalonador (classe Escalonador) será quem irá manipular os processos (um monte de filas)

### Filas

- Processos prontos - baixa prioridade
- Processos prontos - alta prioridade
- E/S disco
- E/S fita
- E/S impressora

## Referências

https://www.geeksforgeeks.org/queue-in-python/
