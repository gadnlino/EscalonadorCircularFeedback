# Escalonador Circular com Feedback
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

O escalonador (classe Scheduler) manipula o estado dos processos, controlando as filas de execução do processador e de acesso aos dispositivos de entrada e saída, a cada instante de tempo.

### Filas

- Processos prontos - baixa prioridade
- Processos prontos - alta prioridade
- E/S disco
- E/S fita
- E/S impressora

## Execução


    python3 main.py --input_file <input_file> --output_file <output_file>

Mais métodos de impressão estão em desenvolvimento.

## Configuração

- **generateProcessesAtRandom**: Se passsado como **true**, irá gerar um numero de processos e a configuração desses aleatoriamente. Deve ser passado como **false** se a propriedade '**processes**' estiver presente.
- **timeSlice**: Fatia de tempo de cada processo, em segundos.
- **ioDevices**: Parâmetros dos dispositivos de E/S que poderão ser utilidados pelos processos.
- **processes**:
  Configuração dos processos.
  - **arrivalTime**: Tempo de chegada do processo na fila de prontos.
  - **totalTime**: Tempo  total de execução do processo.
  - **interruptions**: Definição das interrupções que irão ocorrer durante a execução do processo.
    - **category**: Categoria da interrução (equivalente a **ioDevices[i].name**)
    - **time**: Tempo de ocorrência da interrupção.
    
**Importante**: Alguns cuidados devem ser tomados ao inserir processos manualmente na configuração:
- Não podem existir, num mesmo processo, duas interrupções no mesmo instante de tempo.
- Não podem existir interrupções no último instante de execução do processo.

É bom lembrar que, nesse contexto, "interrupções" se referem exclusivamente a operações de entrada e saída.

Exemplo
---

```json
{
	"generateProcessesAtRandom": false,
	"timeSlice": 5,
	"ioDevices":[
		{
			"name":"hardDrive",
			"requiredTime": 17,
			"returnPriority": "low"
		},
		{
			"name":"magneticTape",
			"requiredTime": 39,
			"returnPriority": "high"
		},
		{
			"name":"printer",
			"requiredTime": 420,
			"returnPriority": "high"
		}
	],
	"processes":[
		{
			"arrivalTime":2,
			"totalTime": 20,
			"interruptions":[
				{
					"category":"hardDrive",
					"processTime":4
				}
			]
		},
		{
			"arrivalTime":3,
			"totalTime": 20
		}
	]
}
```

## Referências

[Algoritmo feedback](https://en.wikipedia.org/wiki/Multilevel_feedback_queue)

[Implementação de filas em Python](https://www.geeksforgeeks.org/queue-in-python/)

[Implementação de filas em Python 2](https://runestone.academy/runestone/books/published/pythonds/BasicDS/ImplementingaQueueinPython.html)

[Algoritmo de linked lists em Python](https://www.codefellows.org/blog/implementing-a-singly-linked-list-in-python/)

[Algoritmo de linked lists em Python 2](https://medium.com/@kevin.michael.horan/data-structures-linked-lists-with-python-2d0ec4fdc18c)

[Algoritmo Round Robin](https://www.geeksforgeeks.org/program-round-robin-scheduling-set-1/)

