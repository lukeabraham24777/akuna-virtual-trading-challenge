output5_results.md

a.  Market parameters: MarketParameters(ajarai_drift=0.001, ajarai_idio_std_dev=0.01, ajarai_rate_beta=-0.02, ajarai_sector_beta=1.0, rate_down_probability=0.2, rate_reversion_strength=0.1, rate_up_probability=0.25, sector_std_dev=0.02, theriodic_drift=0.0015, theriodic_idio_std_dev=0.012, theriodic_rate_beta=-0.015, theriodic_sector_beta=1.0, rate_step=0.25, rate_target=2.0)
Underlyings: FED=3.0, AJR=500.0, THR=600.0
1 (1d FED >= 3.00): user theo=0.7000, actual theo=0.7000
2 (5d FED >= 3.50): user theo=0.0471, actual theo=0.0471
3 (1d AJR >= 500.00): user theo=0.5309, actual theo=0.5309
4 (10d THR >= 650.00): user theo=0.2068, actual theo=0.2068
5 (1d THR - AJR >= 0.00): user theo=1.0000, actual theo=1.0000
6 (10d THR - AJR >= 0.00): user theo=0.9999, actual theo=0.9999
Result: PASS (max_error=0.0000)

b. Ranking:
1. Bastion: $0.12
2. Stalemate Quoter: $0.0
Bastion bankrupt: False (cash balance: 10.12, starting capital: 10.0)
> FED: 5.75, AJR: 1391.0, THR: 2269.23
> FOK from counterparty 783057: buy 0.01 for 1 5498600 (2d THR >= 2419.00)
> Bastion ignored the FOK (theo=0.0475)

[Underlying state advanced by one step]
> FED: 5.5, AJR: 1327.04, THR: 2258.07
> RFQ from counterparty 689497: sell 6 8734500 (1d THR >= 2371.00)
> Bastion quoted buy 0.0 for 2 / sell 2 @ 0.09 (theo=0.0345)
> Bastion bought 0.0 for 2 8734500 (1d THR >= 2371.00) (counterparty 689497)
> RFQ from counterparty 689497: buy 2 8734500 (1d THR >= 2371.00)
> Bastion quoted buy 0.0 for 1 / sell 2 @ 0.06 (theo=0.0345)
> Bastion sold 2 @ 0.06 8734500 (1d THR >= 2371.00) (counterparty 689497)

[Underlying state advanced by one step]
> FED: 5.75, AJR: 1277.17, THR: 2241.32
> 8734500 (0d THR >= 2371.00) expired with expiry_val=0.0
Result: PASS (score=1.00)

c. Ranking:
1. Bastion: $0.64
2. Fixed Width 0.1: $0.35
3. Stalemate Quoter: $0.0
Bastion bankrupt: False (cash balance: 20.64, starting capital: 20.0)
> FED: 1.5, AJR: 1143.14, THR: 1787.62
> FOK from counterparty 482453: buy 0.99 for 2 4895269 (2d THR >= 1735.00)
> Bastion ignored the FOK (theo=0.9822)
> RFQ from counterparty 309546: buy 3 3857985 (1d FED >= 1.75)
> Bastion quoted buy 0.07 for 2 / sell 2 @ 0.32 (theo=0.1975)
> Bastion sold 2 @ 0.32 3857985 (1d FED >= 1.75) (counterparty 309546)

[Underlying state advanced by one step]
> FED: 1.5, AJR: 1142.9, THR: 1794.43
> 3857985 (0d FED >= 1.75) expired with expiry_val=0.0
> FOK from counterparty 482453: sell 9 @ 0.99 4895269 (1d THR >= 1735.00)
> Bastion ignored the FOK (theo=0.9994)
> FOK from counterparty 101661: sell 8 @ 0.99 1280022 (2d THR - AJR >= 0.00)
> Bastion ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 1.5, AJR: 1162.7, THR: 1808.13
> RFQ from counterparty 474121: buy 4 1280022 (1d THR - AJR >= 0.00)
> Bastion quoted buy 0.96 for 2 / sell 2 @ 1.0 (theo=1.0000)
> Bastion sold 2 @ 1.0 1280022 (1d THR - AJR >= 0.00) (counterparty 474121)
> FOK from counterparty 482453: buy 0.99 for 8 5517759 (1d THR >= 1523.00)
> Bastion ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 1.25, AJR: 1194.78, THR: 1863.33
> 1280022 (0d THR - AJR >= 0.00) expired with expiry_val=1.0
Result: PASS (score=1.00)

d. Ranking:
1. Fixed Width 0.05: $2.9
2. Mongoose: $0.3
3. Bastion: $-0.02
Bastion bankrupt: False (cash balance: 39.98, starting capital: 40.0)
> FED: 2.25, AJR: 1309.3, THR: 635.29
> FOK from counterparty 123260: buy 0.94 for 26 6685933 (1d THR >= 624.00)
> Bastion ignored the FOK (theo=0.8147)
> FOK from counterparty 469703: buy 0.39 for 11 4986864 (2d AJR >= 1315.00)
> Bastion ignored the FOK (theo=0.4192)
> FOK from counterparty 469703: buy 0.99 for 2 6685933 (1d THR >= 624.00)
> Bastion accepted the FOK (theo=0.8147)
> Bastion sold 2 @ 0.99 6685933 (1d THR >= 624.00) (counterparty 469703)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1324.96, THR: 651.85
> 6685933 (0d THR >= 624.00) expired with expiry_val=1.0
> RFQ from counterparty 469703: sell 11 4986864 (1d AJR >= 1315.00)
> Bastion quoted buy 0.63 for 2 / sell 2 @ 0.8 (theo=0.7154)
> FOK from counterparty 808858: buy 0.99 for 16 4765820 (2d FED >= 1.50)
> Bastion ignored the FOK (theo=1.0000)
> FOK from counterparty 578477: buy 0.78 for 17 4986864 (1d AJR >= 1315.00)
> Bastion ignored the FOK (theo=0.7154)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1347.82, THR: 648.13
> FOK from counterparty 757814: sell 25 @ 0.01 7933446 (1d AJR >= 1408.00)
> Bastion ignored the FOK (theo=0.0010)
> FOK from counterparty 808858: buy 0.99 for 26 7316899 (1d FED >= 1.00)
> Bastion ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1361.52, THR: 690.84
Result: PASS (score=1.00)

e. Ranking:
1. Stalemate Quoter: $37.0
2. Bastion: $1.9
Bastion bankrupt: False (cash balance: 11.9, starting capital: 10.0)
Result: PASS (score=0.40)

f. Ranking:
1. Fixed Width 0.25: $15.16
2. Stalemate Quoter: $1.0
3. Bastion: $0.02
Bastion bankrupt: False (cash balance: 10.02, starting capital: 10.0)
Result: PASS (score=0.40)

g. Ranking:
1. Fixed Width 0.25: $23.71
2. Bastion: $4.22
Bastion bankrupt: False (cash balance: 14.22, starting capital: 10.0)
Result: PASS (score=0.40)

h. Ranking:
1. Fixed Width 0.1: $33.25
2. Bastion: $2.42
3. Stalemate Quoter: $1.0
Bastion bankrupt: False (cash balance: 12.42, starting capital: 10.0)
Result: PASS (score=0.70)

i. Ranking:
1. Fixed Width 0.1: $30.73
2. Fixed Width 0.25: $3.76
3. Bastion: $2.77
Bastion bankrupt: False (cash balance: 12.77, starting capital: 10.0)
Result: PASS (score=0.40)

j. Ranking:
1. Fixed Width 0.1: $42.67
2. Bastion: $6.22
3. Stalemate Quoter: $5.0
Bastion bankrupt: False (cash balance: 26.22, starting capital: 20.0)
Result: PASS (score=0.70)

k. Ranking:
1. Bastion: $11.76
2. Fixed Width 0.1: $0.62
3. Fixed Width 0.05: $-8.99
Bastion bankrupt: False (cash balance: 31.76, starting capital: 20.0)
Result: PASS (score=1.00)

l. Ranking:
1. Bastion: $8.71
2. Fixed Width 0.05: $-13.8
Bastion bankrupt: False (cash balance: 28.71, starting capital: 20.0)
Result: PASS (score=1.00)

m. Ranking:
1. Fixed Width 0.1: $22.38
2. Lattice: $8.22
3. Situational Unawareness: $4.39
4. Bastion: $-0.81
Bastion bankrupt: False (cash balance: 19.19, starting capital: 20.0)
Result: PASS (score=0.40)

n. Ranking:
1. Lattice: $31.28
2. Bastion: $4.98
3. Fixed Width 0.05: $3.2
Bastion bankrupt: False (cash balance: 24.98, starting capital: 20.0)
Result: PASS (score=0.70)

o. Ranking:
1. Bastion: $12.36
2. Lattice: $6.22
3. Situational Unawareness: $5.8
Bastion bankrupt: False (cash balance: 32.36, starting capital: 20.0)
Result: PASS (score=1.00)

p. Ranking:
1. Lattice: $10.79
2. Bastion: $8.45
3. Fixed Width 0.05: $5.59
Bastion bankrupt: False (cash balance: 48.45, starting capital: 40.0)
Result: PASS (score=0.70)

q. Ranking:
1. Situational Unawareness: $14.84
2. Lattice: $11.99
3. Bastion: $10.59
4. Mongoose: $-5.21
Bastion bankrupt: False (cash balance: 50.59, starting capital: 40.0)
Result: PASS (score=0.60)

r. Ranking:
1. Fixed Width 0.05: $48.2
2. Lattice: $3.57
3. Bastion: $-0.05
4. Mongoose: $-30.38
Bastion bankrupt: False (cash balance: 39.95, starting capital: 40.0)
Result: PASS (score=0.60)

s. Ranking:
1. Situational Unawareness: $23.44
2. Bastion: $-5.21
3. Mongoose: $-14.34
4. Fixed Width 0.05: $-29.48
Bastion bankrupt: False (cash balance: 34.79, starting capital: 40.0)
Result: PASS (score=0.80)

t. Ranking:
1. Bastion: $6.28
2. Lattice: $-19.49
3. Mongoose: $-32.88
4. Fixed Width 0.05: $-83.41
Bastion bankrupt: False (cash balance: 46.28, starting capital: 40.0)
Result: PASS (score=1.00)
