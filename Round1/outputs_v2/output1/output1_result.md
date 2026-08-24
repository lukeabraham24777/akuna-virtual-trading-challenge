a.Market parameters: MarketParameters(ajarai_drift=0.001, ajarai_idio_std_dev=0.01, ajarai_rate_beta=-0.02, ajarai_sector_beta=1.0, rate_down_probability=0.2, rate_reversion_strength=0.1, rate_up_probability=0.25, sector_std_dev=0.02, theriodic_drift=0.0015, theriodic_idio_std_dev=0.012, theriodic_rate_beta=-0.015, theriodic_sector_beta=1.0, rate_step=0.25, rate_target=2.0)
Underlyings: FED=3.0, AJR=500.0, THR=600.0
1 (1d FED >= 3.00): user theo=0.7000, actual theo=0.7000
2 (5d FED >= 3.50): user theo=0.0471, actual theo=0.0471
3 (1d AJR >= 500.00): user theo=0.5309, actual theo=0.5309
4 (10d THR >= 650.00): user theo=0.2068, actual theo=0.2068
5 (1d THR - AJR >= 0.00): user theo=1.0000, actual theo=1.0000
6 (10d THR - AJR >= 0.00): user theo=0.9999, actual theo=0.9999
Result: PASS (max_error=0.0000)

b. Ranking:
1. Lodestar: $0.1
2. Stalemate Quoter: $0.0
Lodestar bankrupt: False (cash balance: 10.1, starting capital: 10.0)
> FED: 5.75, AJR: 1391.0, THR: 2269.23
> FOK from counterparty 783057: buy 0.01 for 1 5498600 (2d THR >= 2419.00)
> Lodestar ignored the FOK (theo=0.0475)

[Underlying state advanced by one step]
> FED: 5.5, AJR: 1327.04, THR: 2258.07
> RFQ from counterparty 689497: sell 6 8734500 (1d THR >= 2371.00)
> Lodestar quoted buy 0.0 for 12 / sell 3 @ 0.07 (theo=0.0345)
> Lodestar bought 0.0 for 3 8734500 (1d THR >= 2371.00) (counterparty 689497)
> RFQ from counterparty 689497: buy 2 8734500 (1d THR >= 2371.00)
> Lodestar quoted buy 0.0 for 10 / sell 3 @ 0.05 (theo=0.0345)
> Lodestar sold 2 @ 0.05 8734500 (1d THR >= 2371.00) (counterparty 689497)

[Underlying state advanced by one step]
> FED: 5.75, AJR: 1277.17, THR: 2241.32
> 8734500 (0d THR >= 2371.00) expired with expiry_val=0.0
Result: PASS (score=1.00)

c. Ranking:
1. Lodestar: $0.82
2. Stalemate Quoter: $0.0
3. Fixed Width 0.1: $0.0
Lodestar bankrupt: False (cash balance: 20.82, starting capital: 20.0)
> FED: 1.5, AJR: 1143.14, THR: 1787.62
> FOK from counterparty 482453: buy 0.99 for 2 4895269 (2d THR >= 1735.00)
> Lodestar accepted the FOK (theo=0.9822)
> Lodestar sold 2 @ 0.99 4895269 (2d THR >= 1735.00) (counterparty 482453)
> RFQ from counterparty 309546: buy 3 3857985 (1d FED >= 1.75)
> Lodestar quoted buy 0.12 for 25 / sell 7 @ 0.28 (theo=0.1975)
> Lodestar sold 3 @ 0.28 3857985 (1d FED >= 1.75) (counterparty 309546)

[Underlying state advanced by one step]
> FED: 1.5, AJR: 1142.9, THR: 1794.43
> 3857985 (0d FED >= 1.75) expired with expiry_val=0.0
> FOK from counterparty 482453: sell 9 @ 0.99 4895269 (1d THR >= 1735.00)
> Lodestar ignored the FOK (theo=0.9994)
> FOK from counterparty 101661: sell 8 @ 0.99 1280022 (2d THR - AJR >= 0.00)
> Lodestar ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 1.5, AJR: 1162.7, THR: 1808.13
> 4895269 (0d THR >= 1735.00) expired with expiry_val=1.0
> RFQ from counterparty 474121: buy 4 1280022 (1d THR - AJR >= 0.00)
> Lodestar quoted buy 0.98 for 6 / sell 33 @ 1.0 (theo=1.0000)
> Lodestar sold 2 @ 1.0 1280022 (1d THR - AJR >= 0.00) (counterparty 474121)
> FOK from counterparty 482453: buy 0.99 for 8 5517759 (1d THR >= 1523.00)
> Lodestar ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 1.25, AJR: 1194.78, THR: 1863.33
> 1280022 (0d THR - AJR >= 0.00) expired with expiry_val=1.0
Result: PASS (score=1.00)

d. Ranking:
1. Fixed Width 0.05: $2.9
2. Mongoose: $0.3
3. Lodestar: $-5.32
Lodestar bankrupt: False (cash balance: 34.68, starting capital: 40.0)
> FED: 2.25, AJR: 1309.3, THR: 635.29
> FOK from counterparty 123260: buy 0.94 for 26 6685933 (1d THR >= 624.00)
> Lodestar accepted the FOK (theo=0.8147)
> Lodestar sold 26 @ 0.94 6685933 (1d THR >= 624.00) (counterparty 123260)
> FOK from counterparty 469703: buy 0.39 for 11 4986864 (2d AJR >= 1315.00)
> Lodestar ignored the FOK (theo=0.4192)
> FOK from counterparty 469703: buy 0.99 for 2 6685933 (1d THR >= 624.00)
> Lodestar accepted the FOK (theo=0.8147)
> Lodestar sold 2 @ 0.99 6685933 (1d THR >= 624.00) (counterparty 469703)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1324.96, THR: 651.85
> 6685933 (0d THR >= 624.00) expired with expiry_val=1.0
> RFQ from counterparty 469703: sell 11 4986864 (1d AJR >= 1315.00)
> Lodestar quoted buy 0.65 for 16 / sell 46 @ 0.78 (theo=0.7154)
> FOK from counterparty 808858: buy 0.99 for 16 4765820 (2d FED >= 1.50)
> Lodestar ignored the FOK (theo=1.0000)
> FOK from counterparty 578477: buy 0.78 for 17 4986864 (1d AJR >= 1315.00)
> Lodestar accepted the FOK (theo=0.7154)
> Lodestar sold 17 @ 0.78 4986864 (1d AJR >= 1315.00) (counterparty 578477)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1347.82, THR: 648.13
> 4986864 (0d AJR >= 1315.00) expired with expiry_val=1.0
> FOK from counterparty 757814: sell 25 @ 0.01 7933446 (1d AJR >= 1408.00)
> Lodestar ignored the FOK (theo=0.0010)
> FOK from counterparty 808858: buy 0.99 for 26 7316899 (1d FED >= 1.00)
> Lodestar ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1361.52, THR: 690.84
Result: PASS (score=1.00)

e. Ranking:
1. Stalemate Quoter: $33.0
2. Lodestar: $3.1
Lodestar bankrupt: False (cash balance: 13.1, starting capital: 10.0)
Result: PASS (score=0.40)

f. Ranking:
1. Fixed Width 0.25: $14.08
2. Stalemate Quoter: $0.0
3. Lodestar: $-2.24
Lodestar bankrupt: False (cash balance: 7.76, starting capital: 10.0)
Result: PASS (score=0.40)

g. Ranking:
1. Lodestar: $10.73
2. Fixed Width 0.25: $7.78
Lodestar bankrupt: False (cash balance: 20.73, starting capital: 10.0)
Result: PASS (score=1.00)

h. Ranking:
1. Fixed Width 0.1: $28.13
2. Lodestar: $5.89
3. Stalemate Quoter: $0.0
Lodestar bankrupt: False (cash balance: 15.89, starting capital: 10.0)
Result: PASS (score=0.70)

i. Ranking:
1. Lodestar: $27.82
2. Fixed Width 0.1: $16.7
3. Fixed Width 0.25: $3.0
Lodestar bankrupt: False (cash balance: 37.82, starting capital: 10.0)
Result: PASS (score=1.00)

j. Ranking:
1. Fixed Width 0.1: $29.39
2. Lodestar: $17.99
3. Stalemate Quoter: $0.0
Lodestar bankrupt: False (cash balance: 37.99, starting capital: 20.0)
Result: PASS (score=0.70)

k. Ranking:
1. Lodestar: $40.2
2. Fixed Width 0.1: $0.18
3. Fixed Width 0.05: $-29.2
Lodestar bankrupt: False (cash balance: 60.2, starting capital: 20.0)
Result: PASS (score=1.00)

l. Ranking:
1. Lodestar: $18.43
2. Fixed Width 0.05: $-20.96
Lodestar bankrupt: False (cash balance: 38.43, starting capital: 20.0)
Result: PASS (score=1.00)

m. Ranking:
1. Fixed Width 0.1: $19.03
2. Lattice: $10.89
3. Situational Unawareness: $3.43
4. Lodestar: $-7.33
Lodestar bankrupt: False (cash balance: 12.67, starting capital: 20.0)
Result: PASS (score=0.40)

n. Ranking:
1. Lattice: $13.22
2. Fixed Width 0.05: $11.6
3. Lodestar: $-2.26
Lodestar bankrupt: False (cash balance: 17.74, starting capital: 20.0)
Result: PASS (score=0.40)

o. Ranking:
1. Lodestar: $28.64
2. Lattice: $4.65
3. Situational Unawareness: $2.17
Lodestar bankrupt: False (cash balance: 48.64, starting capital: 20.0)
Result: PASS (score=1.00)

p. Ranking:
1. Lodestar: $35.63
2. Lattice: $4.77
3. Fixed Width 0.05: $2.58
Lodestar bankrupt: False (cash balance: 75.63, starting capital: 40.0)
Result: PASS (score=1.00)

q. Ranking:
1. Lodestar: $24.6
2. Situational Unawareness: $8.78
3. Lattice: $5.06
4. Mongoose: $-32.26
Lodestar bankrupt: False (cash balance: 64.6, starting capital: 40.0)
Result: PASS (score=1.00)

r. Ranking:
1. Fixed Width 0.05: $28.9
2. Lattice: $-1.12
3. Mongoose: $-4.0
4. Lodestar: $-12.02
Lodestar bankrupt: False (cash balance: 27.98, starting capital: 40.0)
Result: PASS (score=0.40)

s. Ranking:
1. Situational Unawareness: $22.31
2. Lodestar: $-10.55
3. Fixed Width 0.05: $-19.56
4. Mongoose: $-24.69
Lodestar bankrupt: False (cash balance: 29.45, starting capital: 40.0)
Result: PASS (score=0.80)

t. Ranking:
1. Lodestar: $10.57
2. Lattice: $-9.04
3. Mongoose: $-32.91
4. Fixed Width 0.05: $-128.1
Lodestar bankrupt: False (cash balance: 50.57, starting capital: 40.0)
Result: PASS (score=1.00)