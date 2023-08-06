# Client Python pour la banque Crédit agricole - Particuliers

![](https://github.com/dmachard/creditagricole_particuliers/workflows/Publish%20to%20PyPI/badge.svg)

Ce client Python est à destination des particuliers souhaitant récupérer ses opérations bancaires stockées par le Crédit Agricole.
Une [procédure](https://gist.github.com/dmachard/9453bdb0c031a0042b1266fe23ccd732) de mise en oeuvre d'un dashboard Kibana permettant de suivre les opérations bancaires du crédit agricole est disponible sur GitHub Gist.

## Installation

```python
pip install creditagricole_particuliers
```
  
## Authentification

```python
from creditagricole_particuliers import Authenticator

session = Authenticator(username="<n° de compte bancaire>",
                        password=[1, 2, 3, 4, 5, 6],
                        region="normandie")
```
                
## Récupération des opérations bancaires du compte courant

```python
from creditagricole_particuliers import Operations

operations = Operations(session=session,
                        date_start="2020-02-21",
                        date_stop="2020-02-21")
print(operations.list)
[ 
    { 
        'dateOperation': 'Feb 21, 2020 12:00:00 AM',
        'dateValeur': 'Feb 21, 2020 12:00:00 AM',
        'typeOperation': '11',
        'codeTypeOperation': '52',
        'familleTypeOperation': '11',
        'libelleOperation': 'xxxxxxxxxxxxxxxxxxxx',
        'libelleTypeOperation': 'PAIEMENT PAR CARTE',
        'montant': -3.75,
        'idDevise': 'EUR',
        'libelleDevise': '€',
        'libelleComplementaire': '', 
        'referenceMandat': '',
        'idCreancier': '', 
        'libelleCash1': '',
        'libelleCash2': '', 
        'idCarte': '',
        'indexCarte': -1,
        'referenceClient': '', 
        'pictogrammeCSS': 'npc-card',
        'fitid': '579980012....'
    }
]
```

## Itérer sur les opérations bancaires

```python
operations = Operations(session=session,
                        date_start="2020-02-21",
                        date_stop="2020-02-21")
for op in operations:
    print(op)
```

## Type opérations

| Id | Type operation |
|----|----------------|
| 1 | Chèques émis |
| 2 | Chèques reçus |
| 3 | Traites émises |
| 4 | Traites remises |
| 5 | Prélèvements |
| 6 | Virements réalisés |
| 7 | Virements reçus |
| 8 | Réalisation de prêt |
| 9 | Retraits |
| 10 | Opération titre |
| 11 | Factures cartes |
| 12 | Autres |

## Récupération de l'ensemble des comptes bancaires

```python
from creditagricole_particuliers import Accounts

accounts = Accounts(session=session)
print(accounts.list)
[
    {
        'recipientOfTransfert': True, 
        'senderOfTransfert': True, 
        'accountNumber': 'xxxxxxxxxxxxxxxxxxxx', 
        'domain': '50', 
        'subAccountNumber': '00000000000', 
        'productFamilyCode': '50', 
        'bicCode': 'xxxxxxxxxxxxxxxxxxxx', 
        'ibanCode': 'xxxxxxxxxxxxxxxxxxxx', 
        'accountHolderShortDesignation': 'MADAME xxxxxxxxxx', 
        'accountHolderLongDesignation': 'MADAME xxxxxxxxxx', 
        'accountNature': 'PROFESSIONEL', 
        'accountNatureShortLabel': 'TIWI', 
        'accountNatureLongLabel': 'Livret Tiwi', 
        'balanceValue': xxxxxxxxxx, 
        'balanceSign': '+', 
        'balanceDate': {'iMillis': xxxxxxxxxx, 'iChronology': {'iBase': {'iMinDaysInFirstWeek': 4}}}, 
        'currencyCode': 'EUR', 
        'categoryCode': '40',
        'locked': False, 
        'realTimeBalanceRestitution': True, 
        'accountNumberRestitution': True,
        'customerRoleOnAccount': 'ADMINISTRATEUR_LEGAL', 
        'accountLiquidityLevelCode': '2', 
        'accountPersonalizationRankCode': '99',
        'rolePartenaireAffiche': 'Sous administration légale', 
        'weather': 'SOLEIL',
        'codeGdeFamilleProduit': '3'
    }
]
```
