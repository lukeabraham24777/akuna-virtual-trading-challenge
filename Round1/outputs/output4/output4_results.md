output4_results.md

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
1. Lodestar-A: $0.0
2. Stalemate Quoter: $0.0
Lodestar-A bankrupt: False (cash balance: 10.0, starting capital: 10.0)
> FED: 5.75, AJR: 1391.0, THR: 2269.23
> FOK from counterparty 783057: buy 0.01 for 1 5498600 (2d THR >= 2419.00)
> Lodestar-A ignored the FOK (theo=0.0475)

[Underlying state advanced by one step]
> FED: 5.5, AJR: 1327.04, THR: 2258.07
> RFQ from counterparty 689497: sell 6 8734500 (1d THR >= 2371.00)
> Lodestar-A quoted buy 0.01 for 6 / sell 3 @ 0.06 (theo=0.0345)
> Lodestar-A bought 0.01 for 6 8734500 (1d THR >= 2371.00) (counterparty 689497)
> RFQ from counterparty 689497: buy 2 8734500 (1d THR >= 2371.00)
> Lodestar-A quoted buy 0.0 for 2 / sell 2 @ 0.03 (theo=0.0345)
> Lodestar-A sold 2 @ 0.03 8734500 (1d THR >= 2371.00) (counterparty 689497)

[Underlying state advanced by one step]
> FED: 5.75, AJR: 1277.17, THR: 2241.32
> 8734500 (0d THR >= 2371.00) expired with expiry_val=0.0
Result: PASS (score=1.00)

c. Ranking:
1. Lodestar-A: $0.74
2. Stalemate Quoter: $0.0
3. Fixed Width 0.1: $0.0
Lodestar-A bankrupt: False (cash balance: 20.74, starting capital: 20.0)
> FED: 1.5, AJR: 1143.14, THR: 1787.62
> FOK from counterparty 482453: buy 0.99 for 2 4895269 (2d THR >= 1735.00)
> Lodestar-A ignored the FOK (theo=0.9822)
> RFQ from counterparty 309546: buy 3 3857985 (1d FED >= 1.75)
> Lodestar-A quoted buy 0.13 for 6 / sell 6 @ 0.26 (theo=0.1975)
> Lodestar-A sold 3 @ 0.26 3857985 (1d FED >= 1.75) (counterparty 309546)

[Underlying state advanced by one step]
> FED: 1.5, AJR: 1142.9, THR: 1794.43
> 3857985 (0d FED >= 1.75) expired with expiry_val=0.0
> FOK from counterparty 482453: sell 9 @ 0.99 4895269 (1d THR >= 1735.00)
> Lodestar-A ignored the FOK (theo=0.9994)
> FOK from counterparty 101661: sell 8 @ 0.99 1280022 (2d THR - AJR >= 0.00)
> Lodestar-A accepted the FOK (theo=1.0000)
> Lodestar-A bought 0.99 for 8 1280022 (2d THR - AJR >= 0.00) (counterparty 101661)

[Underlying state advanced by one step]
> FED: 1.5, AJR: 1162.7, THR: 1808.13
> RFQ from counterparty 474121: buy 4 1280022 (1d THR - AJR >= 0.00)
> Lodestar-A quoted buy 0.94 for 3 / sell 11 @ 0.97 (theo=1.0000)
> Lodestar-A sold 4 @ 0.97 1280022 (1d THR - AJR >= 0.00) (counterparty 474121)
> FOK from counterparty 482453: buy 0.99 for 8 5517759 (1d THR >= 1523.00)
> Lodestar-A ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 1.25, AJR: 1194.78, THR: 1863.33
> 1280022 (0d THR - AJR >= 0.00) expired with expiry_val=1.0
Result: PASS (score=1.00)

d. Ranking:
1. Fixed Width 0.05: $2.9
2. Mongoose: $0.3
3. Lodestar-A: $-0.02
Lodestar-A bankrupt: False (cash balance: 39.98, starting capital: 40.0)
> FED: 2.25, AJR: 1309.3, THR: 635.29
> FOK from counterparty 123260: buy 0.94 for 26 6685933 (1d THR >= 624.00)
> Lodestar-A ignored the FOK (theo=0.8147)
> FOK from counterparty 469703: buy 0.39 for 11 4986864 (2d AJR >= 1315.00)
> Lodestar-A ignored the FOK (theo=0.4192)
> FOK from counterparty 469703: buy 0.99 for 2 6685933 (1d THR >= 624.00)
> Lodestar-A accepted the FOK (theo=0.8147)
> Lodestar-A sold 2 @ 0.99 6685933 (1d THR >= 624.00) (counterparty 469703)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1324.96, THR: 651.85
> 6685933 (0d THR >= 624.00) expired with expiry_val=1.0
> RFQ from counterparty 469703: sell 11 4986864 (1d AJR >= 1315.00)
> Lodestar-A quoted buy 0.68 for 8 / sell 8 @ 0.75 (theo=0.7154)
> FOK from counterparty 808858: buy 0.99 for 16 4765820 (2d FED >= 1.50)
> Lodestar-A ignored the FOK (theo=1.0000)
> FOK from counterparty 578477: buy 0.78 for 17 4986864 (1d AJR >= 1315.00)
> Lodestar-A ignored the FOK (theo=0.7154)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1347.82, THR: 648.13
> FOK from counterparty 757814: sell 25 @ 0.01 7933446 (1d AJR >= 1408.00)
> Lodestar-A ignored the FOK (theo=0.0010)
> FOK from counterparty 808858: buy 0.99 for 26 7316899 (1d FED >= 1.00)
> Lodestar-A ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1361.52, THR: 690.84
Result: PASS (score=1.00)

e. Ranking:
1. Stalemate Quoter: $35.0
2. Lodestar-A: $2.17
Lodestar-A bankrupt: False (cash balance: 12.17, starting capital: 10.0)
Result: PASS (score=0.40)

f. Ranking:
1. Fixed Width 0.25: $14.83
2. Stalemate Quoter: $1.0
3. Lodestar-A: $-0.67
Lodestar-A bankrupt: False (cash balance: 9.33, starting capital: 10.0)
Result: PASS (score=0.40)

g. Ranking:
1. Lodestar-A: $14.53
2. Fixed Width 0.25: $12.93
Lodestar-A bankrupt: False (cash balance: 24.53, starting capital: 10.0)
Result: PASS (score=1.00)

h. Ranking:
1. Fixed Width 0.1: $25.15
2. Lodestar-A: $8.4
3. Stalemate Quoter: $1.0
Lodestar-A bankrupt: False (cash balance: 18.4, starting capital: 10.0)
Result: PASS (score=0.70)

i. Ranking:
1. Fixed Width 0.1: $24.58
2. Lodestar-A: $13.87
3. Fixed Width 0.25: $0.76
Lodestar-A bankrupt: False (cash balance: 23.87, starting capital: 10.0)
Result: PASS (score=0.70)

j. Ranking:
1. Fixed Width 0.1: $37.39
2. Lodestar-A: $4.41
3. Stalemate Quoter: $4.0
Lodestar-A bankrupt: False (cash balance: 24.41, starting capital: 20.0)
Result: PASS (score=0.70)

k. Ranking:
1. Lodestar-A: $32.77
2. Fixed Width 0.1: $0.18
3. Fixed Width 0.05: $-24.06
Lodestar-A bankrupt: False (cash balance: 52.77, starting capital: 20.0)
Result: PASS (score=1.00)

l. Ranking:
1. Lodestar-A: $9.36
2. Fixed Width 0.05: $-17.96
Lodestar-A bankrupt: False (cash balance: 29.36, starting capital: 20.0)
Result: PASS (score=1.00)

m. Ranking:
1. Fixed Width 0.1: $22.08
2. Lattice: $9.65
3. Situational Unawareness: $3.35
4. Lodestar-A: $-2.59
Lodestar-A bankrupt: False (cash balance: 17.41, starting capital: 20.0)
Result: PASS (score=0.40)

n. Ranking:
1. Fixed Width 0.05: $3.93
2. Lodestar-A: $0.52
3. Lattice: $0.16
Lodestar-A bankrupt: True (cash balance: -0.85, starting capital: 20.0)
Session ended early with 63 of 70 days unplayed
Result: FAIL (score=0.00)

o. Ranking:
1. Lodestar-A: $14.2
2. Situational Unawareness: $7.46
3. Lattice: $6.62
Lodestar-A bankrupt: False (cash balance: 34.2, starting capital: 20.0)
Result: PASS (score=1.00)

p. Ranking:
1. Lodestar-A: $30.24
2. Lattice: $1.57
3. Fixed Width 0.05: $0.48
Lodestar-A bankrupt: False (cash balance: 70.24, starting capital: 40.0)
Result: PASS (score=1.00)

q. Ranking:
1. Lattice: $22.99
2. Lodestar-A: $16.97
3. Situational Unawareness: $8.77
4. Mongoose: $-12.59
Lodestar-A bankrupt: False (cash balance: 56.97, starting capital: 40.0)
Result: PASS (score=0.80)

r. Ranking:
1. Lodestar-A: $0.01
2. Lattice: $0.0
3. Mongoose: $-0.08
4. Fixed Width 0.05: $-0.9
Lodestar-A bankrupt: True (cash balance: -0.34, starting capital: 40.0)
Session ended early with 97 of 100 days unplayed
Result: FAIL (score=0.00)

s. Ranking:
1. Situational Unawareness: $16.88
2. Lodestar-A: $9.88
3. Fixed Width 0.05: $-22.63
4. Mongoose: $-27.68
Lodestar-A bankrupt: False (cash balance: 49.88, starting capital: 40.0)
Result: PASS (score=0.80)

t. Ranking:
1. Lodestar-A: $11.2
2. Lattice: $-19.43
3. Mongoose: $-33.23
4. Fixed Width 0.05: $-100.77
Lodestar-A bankrupt: False (cash balance: 51.2, starting capital: 40.0)
Result: PASS (score=1.00)
