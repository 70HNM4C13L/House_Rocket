# House Rocket
<p align="center">
<img src = "https://github.com/70HNM4C13L/House_Rocket/blob/main/houses.jpg">
</p>
O problema de negócio e a empresa 'House Rocket' são fictícios, os dados foram retirados do https://www.kaggle.com/datasets/harlfoxem/housesalesprediction

# Descricao do projeto e do problema de negócio 
 House Rocket é uma empresa sediada em  Seattle - USA, seu business é comprar imóveis e vender por um preço superior, o principal desafio é encontrar boas oportunidades.  
Boas oportunidades são:  boas casas em ótimas localizações com preços baixos. Quanto maior a diferença entre o preço de aquisição e o preço de venda, maior o lucro.  
O desafio é que as casas possuem vários atributos, o que as tronam mais ou menos atrativas, assim como a localização que as fazem serem mais ou menos valorizadas.  
## Perguntas que deverão ser respondidas:
 - Quais casas a empresa deve comprar, e qual o valor?
 - Por quanto e quando vender essas casas?
## Premissas de negócio
 - ID`s duplicados serão removidos, mantendo o registro mais recente.
 - A localização e possuir ou não vista para orla foram fatores determinantes na definição dos valores dos imóveis
- Foi considerada a estação do ano na precificação dos imóveis
## Informações sobre os dados:
Kaggle https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885  
- id - Unique ID for each home sold
- date - Date of the home sale
- price - Price of each home sold
- bedrooms - Number of bedrooms
- bathrooms - Number of bathrooms, where .5 accounts for a room with a toilet but no shower
- sqft_living - Square footage of the apartments interior living space
- sqft_lot - Square footage of the land space
- floors - Number of floors
- waterfront - A dummy variable for whether the apartment was overlooking the waterfront or not
- view - An index from 0 to 4 of how good the view of the property was
- condition - An index from 1 to 5 on the condition of the apartment,
- grade - An index from 1 to 13, where 1-3 falls short of building construction and design, 7 as an average level of construction and design, and 11-13 have a high quality level of construction and design.
- sqft_above - The square footage of the interior housing space that is above ground level
- sqft_basement - The square footage of the interior housing space that is below ground level
- yr_built - The year the house was initially built
- yr_renovated - The year of the house’s last renovation
- zipcode - What zipcode area the house is in
- lat - Lattitude
- long - Longitude
- sqft_living15 - The square footage of interior housing living space for the nearest 15 eighbors
- sqft_lot15 - The square footage of the land lots of the nearest 15 neighbors
 
 ## Planejamento da solução:
 **- Entender o problema de negócio**

**- Carregar os dados e fazer a analise primaria**

**- Limpar os dados, e fazer analise descritiva**  

**- Levantar hipóteses sobre o negócio**  

**- Testar as hipóteses**  

**- Responder as perguntas de negócio**  

**- Criação do [APP](https://dashboard.heroku.com/apps/analytics-house-rocket-john)**    
  
**- Conclusão**    


## Hipóteses:  
 **- Casas com vista para orla são pelo menos 30% mais caras:**  
   - Verdadeira. Casas com vista para orla são em média 37.013% mais caras.  


 **- Casas em boas condições são mais caras:**  
  - Verdadeira. Casas com atributo 'condition' igual ou superior a 3, são mais caras que as que possuem 'condition' inferiores.
    
    
## Resultado:  
 Para precificar de forma mais justa independente do tamanho do imóvel o processo de analise e seleção de imóveis levou em conta o preço médio por 'SQFT' (square foot, unidade de medida utilizada na base de dados)do lote, separado por lotes que possui ou não vista para orla. Esse valor foi confrontado com a media de preço daquela região (separada por ZIPCODE) ,estação do ano e vista para orla, foram selecionadas as que estavam pelo menos 30% abaixo da média e em condição mínima 3.
 O preço de venda foi baseado na média de preços daquela região de acordo com a estação do ano, buscando a maior valorização possível do imóvel.  
 De um total de 21.613 casas, foram selecionadas 4923 para compra.  
 Valor total investido será de $2.367.054.900.00  
 Valor total de venda $8.452.463.171.40  
 Valor do lucro total $6.085.408.271.40  
 
 
