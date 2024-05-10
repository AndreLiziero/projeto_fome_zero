## 1. Problema de negócio

A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

O CEO precisa de novas métricas do negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero. E para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises, para responder às seguintes perguntas:

### Aspectos Gerais

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

### Métricas por Pais

1. Qual o nome do país que possui mais cidades e restaurantes registradas?
2. Qual o nome do país que possui a maior quantidade de tipos de culinária
distintos?
3. Qual o nome do país que possui a maior quantidade de avaliações feitas?
4. Qual o nome do país que possui, na média, a maior e a menor nota média registrada?

### Métricas por Cidade

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
4 e abaixo de 2.5?
3. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
4. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
distintas?

### Métricas por Restaurantes

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
pessoas?

### Métricas por Tipos de Culinária

1. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
pessoas?
2. Qual o tipo de culinária que possui a maior nota média?
3. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
online e fazem entregas?

## 2. Premissas do negócio

- Esse caso assume o modelo de negócios do tipo Marketplace.
- O projeto foi segmentado nas visões por País, Cidades e Tipos de Culinárias.
- Estratégia da solução:
    
    O Dashboard foi elaborado em um conjunto de 4 páginas. Na página principal foi detalhado aspectos gerais dos restaurantes, apontando as seguintes métricas:
    
    1. Mapa da localização dos restaurantes cadastrados na plataforma.
    2. Números gerais sobre as quantidades de:
        - restaurantes cadastrados;
        - países cadastrados;
        - cidades cadastradas;
        - avalições dos clientes dentro da plataforma;
        - tipos de culinárias oferecidas nos restaurantes.
    3. Um filtro onde é possível determinar quais países aparecem no mapa de restaurantes cadastrados. 
    
    A outra página presente no painel detalha algumas métricas pela visão dos países. Nos quais estão presentes gráficos de barras que detalham:
    
    1. Quantidade de restaurante registrados por país;
    2. Quantidade de cidades registradas por país;
    3. Média de avaliações feitas por país;
    4. Média de preço de um prato para duas pessoas por país;
    5. Um filtro onde é possível determinar quais países serão exibidas as informações acima.
    
    Na página seguinte, com dados a partir das cidades, é apresentado também por gráfico de barras:
    
    1. Top 10 cidades com mais restaurantes na base de dados;
    2. As 7 cidades com mais restaurantes avaliados acima de 4 pontos;
    3. As 7 cidades com mais restaurantes avaliados abaixo de 2,5 pontos;
    4. Top 10 cidades que oferecem a maior variedade de tipos de culinárias distintas;
    5. Um filtro onde é possível determinar quais países serão exibidas as informações acima.
    
    Por fim, na última página, há informações relacionadas aos tipos de culinárias oferecidas nos restaurante cadastrados. Nesta página são apresentadas as seguintes métricas.
    
    1. Os restaurantes melhor avaliados de acordo com o tipo de culinária oferecida;
    2. Uma tabela com dados dos restaurantes mais bem avaliados;
    3. Um gráfico de barras exibindo os tipos de culinárias melhor avaliadas.
    4. Um gráfico de barras exibindo os tipos de culinárias pior avaliadas.
    5. Há três filtros nessa página que são aplicados nas informações acima:
        - Filtro onde determina os países em que os restaurantes estão localizados;
        - Filtro que determina a quantidade de restaurantes que serão exibidas as informações;
        - Filtro que determina os tipos de culinárias oferecidas pelos restaurantes.
    

## 4. Top 3 insights de dados

1. A Indonésia é um país em que os restaurantes possuem a melhor média de avaliações, o menor desvio padrão de avaliações e a maior média de votos por restaurante. Apesar disso, o número de restaurantes cadastrados na Fome Zero endereçados neste país é um dos menores. Logo, pode-se concluir que este país tem grande potencial de trazer resultados positivos para a empresa, principalmente por causa do alto índice de interatividade na plataforma.
2. Há uma limitação na quantidade de restaurantes por cidade. Das 125 cidades cadastradas, 54 possuem 80 restaurantes na base de dados e nenhum outro possui mais do que isso. Assim, tal limite pode, de alguma forma, interferir nas métricas por cidade. Nesse sentido, cabe reavaliar e aumentar esse limite para apresentar da melhor forma os potenciais de cada região. 
3. Os restaurantes que recebem, em média, mais avaliações são aqueles fornecem os serviços de delivery. Do ponto de vista de relacionamento com o cliente ‘Restaurantes’, essa métrica pode demonstrar valor à plataforma Fome Zero de modo que o restaurante identifique, por meio dela, aspectos como esse de disponibilizar serviços de delivery para melhorar seu atendimento.

## 5. O produto final do projeto

Painel online, hospedado em um Cloud e disponível para acesso em
qualquer dispositivo conectado à internet.
O painel pode ser acessado através desse link: https://andreliziero-projetofomezero.streamlit.app/

## 6. Conclusão

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

É possível notar que não há um intervalo de tempo definido para os dados coletados.

Esse conjunto de gráficos/tabelas se estruturam a partir das visões de Países, Cidades e Tipos de Culinárias. De modo que destacam-se, principalmente, a quantidade de restaurantes em relação a essas visões ou de acordo com a avalição média.

Tais métricas podem proporcionar ao CEO ou ao usuário do dashboard, uma noção clara da abrangência da plataforma Fome Zero em todo o mundo, bem como a distribuição de restaurantes e diversidade culinária em cada região. 

Por fim, é possível notar também a interatividade dos clientes em cada região ao avaliarem os restaurantes. Nessa perspectiva, regiões como América do Norte e Ásia possuem mais interatividade do que regiões como América do Sul e África, por exemplo. 

## 7. Próximos passos

1. Igualar as moedas para melhorar a comparação nos preços;
2. Adicionar outros filtros;
3. Criar outras visões de negócio.
