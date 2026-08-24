output3_results.md

a. Market parameters: MarketParameters(ajarai_drift=0.001, ajarai_idio_std_dev=0.01, ajarai_rate_beta=-0.02, ajarai_sector_beta=1.0, rate_down_probability=0.2, rate_reversion_strength=0.1, rate_up_probability=0.25, sector_std_dev=0.02, theriodic_drift=0.0015, theriodic_idio_std_dev=0.012, theriodic_rate_beta=-0.015, theriodic_sector_beta=1.0, rate_step=0.25, rate_target=2.0)
Underlyings: FED=3.0, AJR=500.0, THR=600.0
1 (1d FED >= 3.00): user theo=0.7000, actual theo=0.7000
2 (5d FED >= 3.50): user theo=0.0471, actual theo=0.0471
3 (1d AJR >= 500.00): user theo=0.5309, actual theo=0.5309
4 (10d THR >= 650.00): user theo=0.2068, actual theo=0.2068
5 (1d THR - AJR >= 0.00): user theo=1.0000, actual theo=1.0000
6 (10d THR - AJR >= 0.00): user theo=0.9999, actual theo=0.9999
Result: PASS (max_error=0.0000)

b. Ranking:
1. Lodestar-R: $0.08
2. Stalemate Quoter: $0.0
Lodestar-R bankrupt: False (cash balance: 10.08, starting capital: 10.0)
> FED: 5.75, AJR: 1391.0, THR: 2269.23
> FOK from counterparty 783057: buy 0.01 for 1 5498600 (2d THR >= 2419.00)
> Lodestar-R ignored the FOK (theo=0.0475)

[Underlying state advanced by one step]
> FED: 5.5, AJR: 1327.04, THR: 2258.07
> RFQ from counterparty 689497: sell 6 8734500 (1d THR >= 2371.00)
> Lodestar-R quoted buy 0.0 for 4 / sell 2 @ 0.08 (theo=0.0345)
> Lodestar-R bought 0.0 for 3 8734500 (1d THR >= 2371.00) (counterparty 689497)
> RFQ from counterparty 689497: buy 2 8734500 (1d THR >= 2371.00)
> Lodestar-R quoted buy 0.0 for 2 / sell 2 @ 0.04 (theo=0.0345)
> Lodestar-R sold 2 @ 0.04 8734500 (1d THR >= 2371.00) (counterparty 689497)

[Underlying state advanced by one step]
> FED: 5.75, AJR: 1277.17, THR: 2241.32
> 8734500 (0d THR >= 2371.00) expired with expiry_val=0.0
Result: PASS (score=1.00)

c. Ranking:
1. Lodestar-R: $0.9
2. Stalemate Quoter: $0.0
3. Fixed Width 0.1: $0.0
Lodestar-R bankrupt: False (cash balance: 20.9, starting capital: 20.0)
> FED: 1.5, AJR: 1143.14, THR: 1787.62
> FOK from counterparty 482453: buy 0.99 for 2 4895269 (2d THR >= 1735.00)
> Lodestar-R ignored the FOK (theo=0.9822)
> RFQ from counterparty 309546: buy 3 3857985 (1d FED >= 1.75)
> Lodestar-R quoted buy 0.09 for 3 / sell 3 @ 0.3 (theo=0.1975)
> Lodestar-R sold 3 @ 0.3 3857985 (1d FED >= 1.75) (counterparty 309546)

[Underlying state advanced by one step]
> FED: 1.5, AJR: 1142.9, THR: 1794.43
> 3857985 (0d FED >= 1.75) expired with expiry_val=0.0
> FOK from counterparty 482453: sell 9 @ 0.99 4895269 (1d THR >= 1735.00)
> Lodestar-R ignored the FOK (theo=0.9994)
> FOK from counterparty 101661: sell 8 @ 0.99 1280022 (2d THR - AJR >= 0.00)
> Lodestar-R ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 1.5, AJR: 1162.7, THR: 1808.13
> RFQ from counterparty 474121: buy 4 1280022 (1d THR - AJR >= 0.00)
> Lodestar-R quoted buy 0.97 for 5 / sell 5 @ 1.0 (theo=1.0000)
> Lodestar-R sold 2 @ 1.0 1280022 (1d THR - AJR >= 0.00) (counterparty 474121)
> FOK from counterparty 482453: buy 0.99 for 8 5517759 (1d THR >= 1523.00)
> Lodestar-R ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 1.25, AJR: 1194.78, THR: 1863.33
> 1280022 (0d THR - AJR >= 0.00) expired with expiry_val=1.0
Result: PASS (score=1.00)

d. Ranking:
1. Fixed Width 0.05: $2.9
2. Mongoose: $0.3
3. Lodestar-R: $-0.02
Lodestar-R bankrupt: False (cash balance: 39.98, starting capital: 40.0)
> FED: 2.25, AJR: 1309.3, THR: 635.29
> FOK from counterparty 123260: buy 0.94 for 26 6685933 (1d THR >= 624.00)
> Lodestar-R ignored the FOK (theo=0.8147)
> FOK from counterparty 469703: buy 0.39 for 11 4986864 (2d AJR >= 1315.00)
> Lodestar-R ignored the FOK (theo=0.4192)
> FOK from counterparty 469703: buy 0.99 for 2 6685933 (1d THR >= 624.00)
> Lodestar-R accepted the FOK (theo=0.8147)
> Lodestar-R sold 2 @ 0.99 6685933 (1d THR >= 624.00) (counterparty 469703)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1324.96, THR: 651.85
> 6685933 (0d THR >= 624.00) expired with expiry_val=1.0
> RFQ from counterparty 469703: sell 11 4986864 (1d AJR >= 1315.00)
> Lodestar-R quoted buy 0.65 for 4 / sell 4 @ 0.78 (theo=0.7154)
> FOK from counterparty 808858: buy 0.99 for 16 4765820 (2d FED >= 1.50)
> Lodestar-R ignored the FOK (theo=1.0000)
> FOK from counterparty 578477: buy 0.78 for 17 4986864 (1d AJR >= 1315.00)
> Lodestar-R ignored the FOK (theo=0.7154)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1347.82, THR: 648.13
> FOK from counterparty 757814: sell 25 @ 0.01 7933446 (1d AJR >= 1408.00)
> Lodestar-R ignored the FOK (theo=0.0010)
> FOK from counterparty 808858: buy 0.99 for 26 7316899 (1d FED >= 1.00)
> Lodestar-R ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1361.52, THR: 690.84
Result: PASS (score=1.00)

e. Ranking:
1. Stalemate Quoter: $35.0
2. Lodestar-R: $2.38
Lodestar-R bankrupt: False (cash balance: 12.38, starting capital: 10.0)
Result: PASS (score=0.40)

f. Ranking:
1. Fixed Width 0.25: $14.83
2. Stalemate Quoter: $1.0
3. Lodestar-R: $-0.21
Lodestar-R bankrupt: False (cash balance: 9.79, starting capital: 10.0)
Result: PASS (score=0.40)

g. Ranking:
1. Fixed Width 0.25: $22.71
2. Lodestar-R: $15.11
Lodestar-R bankrupt: False (cash balance: 25.11, starting capital: 10.0)
Result: PASS (score=0.40)

h. Ranking:
1. Fixed Width 0.1: $36.56
2. Stalemate Quoter: $2.0
3. Lodestar-R: $0.52
Lodestar-R bankrupt: False (cash balance: 10.52, starting capital: 10.0)
Result: PASS (score=0.40)

i. Ranking:
1. Fixed Width 0.1: $29.48
2. Lodestar-R: $9.97
3. Fixed Width 0.25: $2.76
Lodestar-R bankrupt: False (cash balance: 19.97, starting capital: 10.0)
Result: PASS (score=0.70)

j. Ranking:
1. Fixed Width 0.1: $36.44
2. Lodestar-R: $8.77
3. Stalemate Quoter: $4.0
Lodestar-R bankrupt: False (cash balance: 28.77, starting capital: 20.0)
Result: PASS (score=0.70)

k. Ranking:
1. Lodestar-R: $21.23
2. Fixed Width 0.1: $0.5
3. Fixed Width 0.05: $-18.5
Lodestar-R bankrupt: False (cash balance: 41.23, starting capital: 20.0)
Result: PASS (score=1.00)

l. Ranking:
1. Lodestar-R: $12.04
2. Fixed Width 0.05: $-17.3
Lodestar-R bankrupt: False (cash balance: 32.04, starting capital: 20.0)
Result: PASS (score=1.00)
 
m. Ranking:
1. Fixed Width 0.1: $21.34
2. Lattice: $11.26
3. Situational Unawareness: $3.34
4. Lodestar-R: $-1.31
Lodestar-R bankrupt: False (cash balance: 18.69, starting capital: 20.0)
Result: PASS (score=0.40)

n. Ranking:
1. Lattice: $23.54
2. Lodestar-R: $7.79
3. Fixed Width 0.05: $6.12
Lodestar-R bankrupt: False (cash balance: 27.79, starting capital: 20.0)
Result: PASS (score=0.70)

o. Ranking:
1. Lattice: $11.81
2. Lodestar-R: $9.29
3. Situational Unawareness: $4.92
Lodestar-R bankrupt: False (cash balance: 29.29, starting capital: 20.0)
Result: PASS (score=0.70)

p. Ranking:
1. Fixed Width 0.05: $12.22
2. Lattice: $4.67
3. Lodestar-R: $4.42
Lodestar-R bankrupt: False (cash balance: 44.42, starting capital: 40.0)
Result: PASS (score=0.40)

q. Ranking:
1. Lattice: $15.37
2. Lodestar-R: $10.43
3. Situational Unawareness: $9.59
4. Mongoose: $-32.1
Lodestar-R bankrupt: False (cash balance: 50.43, starting capital: 40.0)
Result: PASS (score=0.80)

r. Ranking:
1. Fixed Width 0.05: $39.77
2. Lodestar-R: $5.98
3. Lattice: $5.7
4. Mongoose: $-31.73
Lodestar-R bankrupt: False (cash balance: 45.98, starting capital: 40.0)
Result: PASS (score=0.80)

s. Ranking:
1. Lodestar-R: $22.85
2. Situational Unawareness: $19.83
3. Mongoose: $-28.02
4. Fixed Width 0.05: $-41.34
Lodestar-R bankrupt: False (cash balance: 62.85, starting capital: 40.0)
Result: PASS (score=1.00)

t. Ranking:
1. Lodestar-R: $19.33
2. Lattice: $-5.04
3. Mongoose: $-32.95
4. Fixed Width 0.05: $-116.36
Lodestar-R bankrupt: False (cash balance: 59.33, starting capital: 40.0)
Result: PASS (score=1.00)
