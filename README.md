# Number game

## Papildu prasības programmatūrai 

Spēles sākumā cilvēks-spēlētājs norāda spēlē izmantojamas skaitļu virknes garumu, kas var būt diapazonā no 15 līdz 25 skaitļiem. Spēles programmatūra gadījuma ceļā saģenerē skaitļu virkni atbilstoši uzdotajam garumam, tajā iekļaujot skaitļus no 1 līdz 6. 


## Spēles apraksts 

Spēles sākumā ir dota ģenerētā skaitļu virkne. Spēlētāji izpilda gājienus pēc kārtas. Katram spēlētājam ir 0 punktu. Gājiena laikā spēlētājs var:  

saskaitīt skaitļu pāri (pirmo ar otro, trešo ar ceturto, piekto ar sesto) un summu ierakstīt saskaitīto skaitļu pāra vieta vietā (ja summa ir lielāka par 6, tad notiek aizvietošanas: 7 = 1, 8 = 2, 9 = 3, 10 = 4, 11=5, 12=6), kā arī pieskaitīt savam punktu skaitam 1 punktu, vai  

nodzēst to skaitli, kas ir palicis bez pāra un atņemt vienu punktu no sava punktu skaita.  

Spēle beidzas, kad skaitļu virknē paliek viens skaitlis. Uzvar spēlētājs, kam ir vairāk punktu. 


## Before running:
```bash
pip3 install -r requirements.txt
```

## Test the game: 

### For integration tests:
```bash
python3 -m pytest -s .\test_integration.py
```


## Run the game:
```bash
python3 .\Game_v4.py
```