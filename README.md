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
https://runestone.academy/runestone/books/published/pythonds/BasicDS/ImplementingaQueueinPython.html
https://www.geeksforgeeks.org/program-round-robin-scheduling-set-1/

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
					"time":4
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
