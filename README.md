# LiftingLoops (Protein Pow(d)er)

Deze repo is ter gedeeltelijke vervulling van de eindnormen voor het vak Algoritmen en Heuristieken aan de Universiteit van Amsterdam. Geschreven door Hendrik DuPont, Jeppe Mul en Nasreddine Ouchene, met vele dank aan onze TA's Nina van der Meulen en Rayen Oaf, alsmede de docenten Jelle van Assema, Bas Terwijn en Wouter Vrielink. 

## Model
Eiwitten, oftewel proteïnen bestaan uit een keten van aminozuren. Voor o.a. medisch onderzoek is het van groot belang dat men de vouwing kan inschatten voor een gegeven keten van aminozuren. De beste manier om een vouwing in te schatten is door een model te maken van het eiwit waarbij gezocht wordt naar de vouwing met de laagste grondtoestand. 

Één van de modellen om dit te simuleren is een versimpeld model, waarbij aminozuren worden voorgesteld als voorkomend op de punten ∈(ℤ, ℤ, ℤ) in een Cartesiaans assenstelsel. De verbindingen zijn altijd lijnstukken met een lengte van 1, wat tezamen met de definitie van de punten erop neerkomt dat punten alleen verbonden kunnen zijn met een hoek van 90°. Aminozuren mogen niet dezelfde coördinaten hebben. Dit leidt in combinatie met de vorige constraints tot het feit dat een geldige keten zichzelf niet kan kruisen.

Aminozuren hebben naast hun positie ook nog een type. Deze worden weergegeven met de hoofdletter P, H en C, wat respectievelijk staat voor Polair, Hydrofoob en Cysteïne. Een eiwit kan dan worden weergegeven als een combinatie van deze letters, waarbij letters die naast elkaar staan aan elkaar verbonden zijn. De grondtoestand van een vouwing neemt af naarmate er waterstofbruggen worden gevormd. Voor het model betekent dat concreet dat er minpunten worden toegekend aan bepaalde combinaties van eiwitten die naast elkaar liggen, dat wil zeggen dat de Euclidische afstand tussen de coördinaten 1 is, maar niet verbonden zijn aan elkaar. Voor een waterstofbrug tussen 2 hydrofobe aminozuren wordt 1 minpunt toegekend, evenals voor een brug tussen een hydrofoob aminozuur en een cysteïne. Voor een waterstofbrug tussen 2 cysteïnen worden zelfs 5 minpunten toegekend.

Een vouwing wordt weergegeven door een csv met een rij voor elk aminozuur, waarbij elke rij ten eerste bestaat uit het type aminozuur, en ten tweede uit een geheel getal dat de vouwrichting weergeeft. Een 1 staat voor een stap in de X-as, een 2 voor een stap in de Y-as, en een 3 voor een stap in de Z-as. Een negatief getal betekent een stap in dezelfde as, maar dan in de negatieve richting. Omgerekend naar mensentaal is -1 dus een stap naar "links" en 3 een stap naar "boven". Onderaan de csv staat ook de grondtoestand van het eiwit. Er wordt ook een plot gegenereerd van de oplossing. Deze wordt in principe niet opgeslagen, maar het staat de gebruiker vrij dit te doen vanuit matplotlib. Een voorbeeld kan worden gevonden in deze directory onder de naam 'output.csv'.

## Algoritmen
- Random
  Dit algoritme genereert een lijst met willekeurig gegenereerde vouwingen en construeerd vervolgens het bijbehorende eiwit. Vergeleken met de andere Random is dit algoritme meer willekeurig, maar duurt het langer om een iteratie te doen, omdat de kans groter is dat een iteratie opnieuw moet vanwege kruising.
  
- Beam
  Dit algoritme bestaat uit 2 parameters, namelijk het aantal beams en de lookahead-diepte. Beam is exact hetzelfde als greedy met 1 beam, en exact hetzelfde als breadth-first met een oneindig aantal beams. Een beam-algoritme met een lookahead die net zo groot is als de lengte van het aminozuur is technisch gezien hetzelfde als depth-first, alleen dan heel veel slomer omdat het voor elk aminozuur weer opnieuw de hele boom zou moeten doorzoeken. Dit is dus niet aan te raden.

## Aanroepen algoritmen
Om een algoritme aan te roepen, voer main.py out. Deze kent een aantal parameters. Ten eerste, een .txt file met op 4 rijen met in deze volgorde de parameters, waarbij de aanhalingstekens hier dienen als verduidelijking en moeten worden weggelaten, en in de haken de gewenste waarden:

- keten = [string van hoofdletters P,H en C]
- algoritme = ['random', of 'beam search']
- iteraties = [geheel getal]
- lookahead = [geheel getal of '0']

Let op: voor Beam staat iteraties NIET voor het aantal iteraties dat beam runt over de hele boom, maar voor het aantal beams. Lookahead is alleen geïmplementeerd voor Beam. Vul in '0' voor alle andere algoritmen.
Een voorbeeld kan worden gevonden in deze directory onder de naam 'experiment.txt'.

De tweede parameter is de naam van de output file waarin de output moet worden opgeslagen. Dit moet een .csv file zijn, zoals output.csv o.i.d.

Als laatste kan met -threeD, een optionele flag, de 3d-weergave ingeschakeld worden. Alle algoritmen zijn zo geïmplementeerd dat ze ook werken in 3d.

## Heatmap
De heatmap geeft een visuele weergave van hoe verschillende parameters de prestaties van het model beïnvloeden. Dit kan helpen bij het identificeren van trends en optimale instellingen voor de lookahead-diepte en het aantal beams.
De heatmap wordt gegenereerd door het volgende commando in de terminal uit te voeren:

python -m algorithms.heatmap

De parameters kunnen in de code zelf worden aangepast. De heatmap visualiseert de scores voor diverse parametercombinaties en toont tevens de benodigde berekeningstijd. De assen vertegenwoordigen de geselecteerde variabelen, terwijl de kleur de score aanduidt: een donkerdere kleur wijst op een lagere (en dus betere) score. Dit helpt bij het beoordelen van de efficiëntie en effectiviteit van verschillende instellingen.

## Algoritme Vergelijking
In deze vergelijking worden uitsluitend Random Folding en Beam Search getest. De Beam Search-algoritme wordt uitgevoerd en de tijd gemeten die nodig is om een bepaalde score te bereiken. Vervolgens wordt Random Folding exact even lang uitgevoerd, zodat een eerlijke vergelijking ontstaat.
De vergelijking wordt aangeroepen met:

python -m algorithms.algorithm_comparison

Net als bij de heatmap kunnen de parameters binnen de code worden aangepast. De resultaten worden samengevat in een grafiek waarin per algoritme de behaalde scores worden weergegeven. Dit geeft inzicht in hoe goed Beam Search en Random Folding presteren bij een gegeven dataset en welke instellingen het meest invloed hebben op de prestaties.

