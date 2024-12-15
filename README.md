# t1-visao-comp
Trabalho 1 de Visão Computacional UFES 2024/1

# RUN IT

- Dentro do diretório do projeto, faça no terminal:

    python3 ./main.py
    

# TODO
- fazer as funções de update das variáveis:
    - analisar e propor comportamento para os botões de update

- quando montar o esquema de projeção:
    - lembrar de inverter "extr_param_matrix" para fazer a projeção do objeto
    - lembrar de deixar a última coordenada do obj_2d em 1 antes de plotar

- deixar valores intrínsecos da camera mostrando na UI 
    - quando deseja-se mudar, basta sobrescrevê-los
    - se forem apagados (no user-input), retomar para valores default. 

# SUGGESTED IF ENED EARLY

- montar uma stack na UI, mostrando as alterações que fará na câmera. 
    - adicionar um botão de "adicionar na stack"