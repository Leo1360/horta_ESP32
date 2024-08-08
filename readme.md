# Hosta ESP32
Projeto de um sistema para monitoramento da horta/estufa da Fatec de Mogi das Cruzes com baixo custo.
O sistema se conecta no wifi, capacitando a cadastramento de diversos sensores via web para que sejam lidos e tenham seus dados armazenados. Cada sensor tem setado uma faixa valores esperados para a leitura e caso ocorra uma leitura fora do espera uma notificação é enviada via Telegram.

O sistema é compartimentalizado e permite que sejam carregado novos "drivers" para sensores ainda não suportados ou customizados.
Todos os dados são persistidos em cartão SD e podem ser acessado pelo portal do sistema, que fica disponivel em [horta.local](horta.local) após o sistema se conectar no wifi. Pela api web tambem é possivel cadastrar nos sensores e acessar outras informações.

## Porque Micropython?
A linguagem foi escolhida principalmente por sua facilidade de manutenção, tendo em vista que a aplicação são tem requisitos de performance muito restritivos e o projeto teria sua manutenção feita por alunos voluntarios fora do horario de aula.


## Todo - Melhorias necessárias
- [ ] PCB: Selecionar conector mais robustos para fazer interface com os sensores - Preferencialmente a prova d'água
- [ ] PCB: Adicionar um circuito de UPS, para permitir que o sistema continue operando mesmo com quedas de energia
- [ ] PCB: Refazer PCB utilizar o Modulo esp32 diretament e não o devKit
- [ ] SW: Adicionar opções de configuração no portal
- [ ] SW: Possibilidar configuração do tempo de leitura para cada sensor individualmente
- [ ] SW: Add no portal a possibilidade de carregar o driver do sensor em tempo de execução
- [ ] SW: Add deep sleep
