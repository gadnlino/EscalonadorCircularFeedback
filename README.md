# Escalonador Circular com Feedback

## Objetivo

O objetivo do trabalho é simular a execução do escalonador de um sistema operacional, utilizando a estratégia circular para distribuição do tempo de processador entre os processos, e utilizando uma atribuição de prioridade dinâmica(Feedback) a depender das operações de IO realizadas por cada processo.

<!-- A princípio faremos em python.
Daniel propos a refaze-lo em C, após a finalização do código em python.
Após conversar com a professora e considerando o prazo do trabalho, 
julgamos desnecessário refazer em C -->

## Premissas:

O timeSlice de cada processo, o número de processos e o tempo de cada dispositivo de IO são parametrizáveis(Olhar seção 'Propriedades do arquivo de entrada'). Na maior parte dos nossos [exemplos](https://github.com/gadnlino/EscalonadorCircularFeedback/tree/main/exemplos), iremos usar os seguintes valores:

- O timeSlice de cada processo: 5
- **Tempo da E/S de disco**: 10, baixa prioridade
- **Tempo da E/S de fita magnética**: 4, alta prioridade
- **Tempo da E/S da impressora**: 5, alta prioridade

<!-- De inicio decidimos:
- **Tempo da E/S de disco**: 17
- **Tempo da E/S de fita magnética**: 39
- **Tempo da E/S da impressora**: 420

Após uma revisão desses tempos, era desnecessariamente alto, logo mudamos a parametrização.

Iremos parametrizar:
- O número de processos 
- O quantum de cada processos: 5
- **Tempo da E/S de disco**: 10, baixa prioridade
- **Tempo da E/S de fita magnética**: 4, alta prioridade
- **Tempo da E/S da impressora**: 5, alta prioridade -->

## Componentes principais

### Informações dos processos

O pid é gerado quando o processo entra na fila de prontos.
Todos pids tem como ppid o processo 1, que é o kernel do sistema operacional.
Informações do PCB estão definidas na nossa estrutura de dados([classe Process](https://github.com/gadnlino/EscalonadorCircularFeedback/blob/main/models/process.py)).

### Escalonador

O escalonador ([classe Scheduler](https://github.com/gadnlino/EscalonadorCircularFeedback/blob/main/scheduler.py)) manipula o estado dos processos, controlando as filas de execução do processador e de acesso aos dispositivos de entrada e saída, a cada instante de tempo.

### Filas

- Novos processos prontos - alta prioridade
- Processos em espera após usar time-slice - baixa prioridade

- E/S disco - baixa prioridade
- E/S fita - alta prioridade
- E/S impressora - alta prioridade

## Instalação
Tendo o Python instalado em sua máquina(https://www.python.org/downloads/), execute o comando abaixo para instalar as dependências do projeto:

	pip install -r requirements.txt

## Execução

    python3 main.py --input_file <input_file> [--output-type gif|stdout] [--save-intermediary]
	
### Opções:

- **--input-file**: O nome do arquivo de configuração a ser utilizado. Deve ser um arquivo json com as propriedades listadas na seção 'Propriedades do arquivo de entrada'
- **--output-type**: O formato de saída do escalonador. Valores: gif, stdout. Padrão: stdout.
- **--save-intermediary**: Se esta flag estiver presente, o programa irá gerar o arquivo intermediários com os frames do escalonador(esse é o arquivo utilizado para gerar a visualização).

## Propriedades do arquivo de entrada

- **generateProcessesAtRandom**: Se passsado como **true**, irá gerar um numero de processos e a configuração desses aleatoriamente. Deve ser passado como **false** se a propriedade '**processes**' estiver presente.
- **timeSlice**: Fatia de tempo atribuída a cada processo, em segundos.
- **ioDevices**: Lista com os dispositivos de IO que podem ser utilizados pelos processos. Um ioDevice deve possuir os seguintes parâmetros:
	- **name**: O nome do dispositivo (nos nossos exemplos: 'printer', 'hardDisk', 'magneticTape').
	- **requiredTime**: O tempo necessário para utilizar o dispositivo.
	- **returnPriority**: A prioridade atribuida ao processo que termina de utilizar o dispositivo.

- **processes**:
  Lista de processos. Um processo deve ter os seguintes parâmetros:
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

config.json

```json
{
	"generateProcessesAtRandom": false,
	"timeSlice": 5,
	"ioDevices": [
		{
			"name": "hardDisk",
			"requiredTime": 10,
			"returnPriority": "low"
		},
		{
			"name": "magneticTape",
			"requiredTime": 4,
			"returnPriority": "high"
		},
		{
			"name": "printer",
			"requiredTime": 5,
			"returnPriority": "high"
		}
	],
	"processes": [
		{
			"arrivalTime": 2,
			"totalTime": 20,
			"interruptions": [
				{
					"category": "hardDisk",
					"processTime": 4
				}
			]
		},
		{
			"arrivalTime": 10,
			"totalTime": 20
		}
	]
}
```

	python main.py -i config.json --output-type gif
	
[https://media.giphy.com/media/rM8ihhEeGZLK7c6mbq/giphy.gif](https://media.giphy.com/media/rM8ihhEeGZLK7c6mbq/giphy.gif)

![Visualização - Escalonador Round Robin/Feedback](https://media.giphy.com/media/rM8ihhEeGZLK7c6mbq/giphy.gif)


## Desafios

- Havia um bug com o scheduler, os dispositivos de IO estavam utilizando erroneamente o tempo do processador.

<!-- - Dificuldade com o plot das informações embaixo do gráfico gerado pelo código. Elas ficavam empilhadas uma na outra.  -->

- Problemas com o plot das barras dos processos no gráfico gerado pelo código. Dificuldade em saber o tamanho apropriado. 

## Membros do grupo:

<!-- Os participantes do Grupo 3: -->

- Daniel Cardoso ([DCarts](https://www.geeksforgeeks.org/program-round-robin-scheduling-set-1/))
- Guilherme Avelino ([gadnlino](https://github.com/gadnlino))
- Gustavo Muzy ([GustavoMuzyFraga](https://github.com/DCarts))

## Referências

[Algoritmo feedback](https://en.wikipedia.org/wiki/Multilevel_feedback_queue)

[Implementação de filas em Python](https://www.geeksforgeeks.org/queue-in-python/)

[Implementação de filas em Python 2](https://runestone.academy/runestone/books/published/pythonds/BasicDS/ImplementingaQueueinPython.html)

[Algoritmo de linked lists em Python](https://www.codefellows.org/blog/implementing-a-singly-linked-list-in-python/)

[Algoritmo de linked lists em Python 2](https://medium.com/@kevin.michael.horan/data-structures-linked-lists-with-python-2d0ec4fdc18c)

[Algoritmo Round Robin](https://www.geeksforgeeks.org/program-round-robin-scheduling-set-1/)

## Link para o projeto:

Mais detalhes e exemplos podem ser encontrados no link abaixo:

https://github.com/gadnlino/EscalonadorCircularFeedback