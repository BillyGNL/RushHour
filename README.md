#RushHour

---

Dit programma lost het spel RushHour via verschillende algoritmen op. Het spel bestaat uit een vierkante grid met daarin auto's van verschillende grootte geplaatst. Het doel van het spel is om de rode auto naar de uitgang te leiden door middel van het verplaatsen van de auto's die de doorgang blokkeren. Het voornaamste doel is dit spel zo efficient mogelijk op te lossen. Daarbij is onder andere gekeken naar het aantal gezette stappen en de runtime om tot dit aantal stappen te komen.


Hiervoor hebben wij verschillende algoritmen geschreven; twee random algoritmen en een algoritme gebaseerd op de Breadth First Search methode.

## Aan de slag

---

### Vereisten

Dit programma is geschreven in Python 3.6.8. Verder staan in requirements.txt alle benodigde extra pakketten voor het runnen van dit programma. Deze zijn te installeren aan de hand van de volgende invoer:  
`pip install -r requirements.txt`

### Structuur

komt nog

### Test

Voor het testen van de verschillende algoritmen, voer het volgende uit:
`python random_algoritm.py  python random_upperbound.py  python BFS.py`    
Dit runt respectivelijk de random algoritmes en het algoritme aan de hand van Breadth First Search.


Hierna wordt gevraagd op welk bord dit uitgevoerd dient te worden, dit zijn allen .csv bestanden, te vinden in de map boards. Er zijn zeven borden beschikbaar, drie borden hebben een grootte van 6 bij 6, drie van 9 bij 9 en een van 12 bij 12. Deze kunnen worden aangeroepen door als input file het volgende in te voeren:
`6x6_1`
Bovenstaande roept bord 1 aan, wat een grootte heeft van 6 bij 6, dit loopt zo door tot het 12 bij 12 bord:
`12x12_7`


Als laatste is ook nog het aantal gewenste interaties nodig als input. Hiervoor dient simpelweg het aantal als getal te worden ingevoerd.

## Auteurs

---

* Billy Griep
* Jan Elders
* Floris Kienhuis

## Dankwoord

---

* Stackoverflow
* Wikipedia
