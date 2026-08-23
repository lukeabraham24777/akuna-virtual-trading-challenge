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
1. Meridian: $0.1
2. Stalemate Quoter: $0.0
Meridian bankrupt: False (cash balance: 10.1, starting capital: 10.0)
> FED: 5.75, AJR: 1391.0, THR: 2269.23
> FOK from counterparty 783057: buy 0.01 for 1 5498600 (2d THR >= 2419.00)
> Meridian ignored the FOK (theo=0.0475)

[Underlying state advanced by one step]
> FED: 5.5, AJR: 1327.04, THR: 2258.07
> RFQ from counterparty 689497: sell 6 8734500 (1d THR >= 2371.00)
> Meridian quoted buy 0.0 for 12 / sell 3 @ 0.07 (theo=0.0345)
> Meridian bought 0.0 for 3 8734500 (1d THR >= 2371.00) (counterparty 689497)
> RFQ from counterparty 689497: buy 2 8734500 (1d THR >= 2371.00)
> Meridian quoted buy 0.0 for 10 / sell 3 @ 0.05 (theo=0.0345)
> Meridian sold 2 @ 0.05 8734500 (1d THR >= 2371.00) (counterparty 689497)

[Underlying state advanced by one step]
> FED: 5.75, AJR: 1277.17, THR: 2241.32
> 8734500 (0d THR >= 2371.00) expired with expiry_val=0.0
Result: PASS (score=1.00)

c. Ranking:
1. Meridian: $0.81
2. Stalemate Quoter: $0.0
3. Fixed Width 0.1: $0.0
Meridian bankrupt: False (cash balance: 20.81, starting capital: 20.0)
> FED: 1.5, AJR: 1143.14, THR: 1787.62
> FOK from counterparty 482453: buy 0.99 for 2 4895269 (2d THR >= 1735.00)
> Meridian ignored the FOK (theo=0.9822)
> RFQ from counterparty 309546: buy 3 3857985 (1d FED >= 1.75)
> Meridian quoted buy 0.13 for 25 / sell 7 @ 0.27 (theo=0.1975)
> Meridian sold 3 @ 0.27 3857985 (1d FED >= 1.75) (counterparty 309546)

[Underlying state advanced by one step]
> FED: 1.5, AJR: 1142.9, THR: 1794.43
> 3857985 (0d FED >= 1.75) expired with expiry_val=0.0
> FOK from counterparty 482453: sell 9 @ 0.99 4895269 (1d THR >= 1735.00)
> Meridian ignored the FOK (theo=0.9994)
> FOK from counterparty 101661: sell 8 @ 0.99 1280022 (2d THR - AJR >= 0.00)
> Meridian ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 1.5, AJR: 1162.7, THR: 1808.13
> RFQ from counterparty 474121: buy 4 1280022 (1d THR - AJR >= 0.00)
> Meridian quoted buy 0.97 for 6 / sell 25 @ 1.0 (theo=1.0000)
> Meridian sold 2 @ 1.0 1280022 (1d THR - AJR >= 0.00) (counterparty 474121)
> FOK from counterparty 482453: buy 0.99 for 8 5517759 (1d THR >= 1523.00)
> Meridian ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 1.25, AJR: 1194.78, THR: 1863.33
> 1280022 (0d THR - AJR >= 0.00) expired with expiry_val=1.0
Result: PASS (score=1.00)

d. Ranking:
1. Fixed Width 0.05: $2.9
2. Mongoose: $0.3
3. Meridian: $-5.32
Meridian bankrupt: False (cash balance: 34.68, starting capital: 40.0)
> FED: 2.25, AJR: 1309.3, THR: 635.29
> FOK from counterparty 123260: buy 0.94 for 26 6685933 (1d THR >= 624.00)
> Meridian accepted the FOK (theo=0.8147)
> Meridian sold 26 @ 0.94 6685933 (1d THR >= 624.00) (counterparty 123260)
> FOK from counterparty 469703: buy 0.39 for 11 4986864 (2d AJR >= 1315.00)
> Meridian ignored the FOK (theo=0.4192)
> FOK from counterparty 469703: buy 0.99 for 2 6685933 (1d THR >= 624.00)
> Meridian accepted the FOK (theo=0.8147)
> Meridian sold 2 @ 0.99 6685933 (1d THR >= 624.00) (counterparty 469703)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1324.96, THR: 651.85
> 6685933 (0d THR >= 624.00) expired with expiry_val=1.0
> RFQ from counterparty 469703: sell 11 4986864 (1d AJR >= 1315.00)
> Meridian quoted buy 0.67 for 16 / sell 46 @ 0.76 (theo=0.7154)
> FOK from counterparty 808858: buy 0.99 for 16 4765820 (2d FED >= 1.50)
> Meridian ignored the FOK (theo=1.0000)
> FOK from counterparty 578477: buy 0.78 for 17 4986864 (1d AJR >= 1315.00)
> Meridian accepted the FOK (theo=0.7154)
> Meridian sold 17 @ 0.78 4986864 (1d AJR >= 1315.00) (counterparty 578477)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1347.82, THR: 648.13
> 4986864 (0d AJR >= 1315.00) expired with expiry_val=1.0
> FOK from counterparty 757814: sell 25 @ 0.01 7933446 (1d AJR >= 1408.00)
> Meridian ignored the FOK (theo=0.0010)
> FOK from counterparty 808858: buy 0.99 for 26 7316899 (1d FED >= 1.00)
> Meridian ignored the FOK (theo=1.0000)

[Underlying state advanced by one step]
> FED: 2.25, AJR: 1361.52, THR: 690.84
Result: PASS (score=1.00)

e. Ranking:
1. Stalemate Quoter: $34.0
2. Meridian: $2.21
Meridian bankrupt: False (cash balance: 12.21, starting capital: 10.0)
Result: PASS (score=0.40)

f. Ranking:
1. Fixed Width 0.25: $13.83
2. Stalemate Quoter: $0.0
3. Meridian: $-2.16
Meridian bankrupt: False (cash balance: 7.84, starting capital: 10.0)
Result: PASS (score=0.40)

g. Ranking:
1. Meridian: $10.85
2. Fixed Width 0.25: $5.99
Meridian bankrupt: False (cash balance: 20.85, starting capital: 10.0)
Result: PASS (score=1.00)

h. Ranking:
1. Fixed Width 0.1: $28.98
2. Meridian: $3.03
3. Stalemate Quoter: $0.0
Meridian bankrupt: False (cash balance: 13.03, starting capital: 10.0)
Result: PASS (score=0.70)

i. Ranking:
1. Meridian: $30.32
2. Fixed Width 0.1: $10.29
3. Fixed Width 0.25: $0.0
Meridian bankrupt: False (cash balance: 40.32, starting capital: 10.0)
Result: PASS (score=1.00)

j. Ranking:
1. Fixed Width 0.1: $32.44
2. Meridian: $7.27
3. Stalemate Quoter: $4.0
Meridian bankrupt: False (cash balance: 27.27, starting capital: 20.0)
Result: PASS (score=0.70)

k. Ranking:
1. Meridian: $40.15
2. Fixed Width 0.1: $0.18
3. Fixed Width 0.05: $-34.06
Meridian bankrupt: False (cash balance: 60.15, starting capital: 20.0)
Result: PASS (score=1.00)

l. Ranking:
1. Meridian: $-3.92
2. Fixed Width 0.05: $-21.32
Meridian bankrupt: False (cash balance: 16.08, starting capital: 20.0)
Result: PASS (score=1.00)

m. Ranking:
1. Fixed Width 0.1: $18.93
2. Lattice: $11.16
3. Situational Unawareness: $3.39
4. Meridian: $-7.35
Meridian bankrupt: False (cash balance: 12.65, starting capital: 20.0)
Result: PASS (score=0.40)

n. Ranking:
1. Meridian: $18.16
2. Lattice: $11.63
3. Fixed Width 0.05: $-16.71
Meridian bankrupt: False (cash balance: 38.16, starting capital: 20.0)
Result: PASS (score=1.00)

o. Ranking:
1. Meridian: $23.8
2. Situational Unawareness: $5.16
3. Lattice: $2.37
Meridian bankrupt: False (cash balance: 43.8, starting capital: 20.0)
Result: PASS (score=1.00)

p. Ranking:
1. Meridian: $22.92
2. Fixed Width 0.05: $10.05
3. Lattice: $5.38
Meridian bankrupt: False (cash balance: 62.92, starting capital: 40.0)
Result: PASS (score=1.00)

q. Ranking:
1. Meridian: $22.51
2. Situational Unawareness: $7.58
3. Lattice: $4.68
4. Mongoose: $-31.06
Meridian bankrupt: False (cash balance: 62.51, starting capital: 40.0)
Result: PASS (score=1.00)

r. Ranking:
1. Fixed Width 0.05: $22.86
2. Lattice: $3.81
3. Mongoose: $-4.04
4. Meridian: $-13.39
Meridian bankrupt: False (cash balance: 26.61, starting capital: 40.0)
Result: PASS (score=0.40)

s. Ranking:
1. Situational Unawareness: $18.01
2. Mongoose: $-8.51
3. Meridian: $-17.98
4. Fixed Width 0.05: $-38.78
Meridian bankrupt: False (cash balance: 22.02, starting capital: 40.0)
Result: PASS (score=0.60)

t. Ranking:
1. Lattice: $-16.92
2. Meridian: $-23.55
3. Mongoose: $-33.23
4. Fixed Width 0.05: $-95.91
Meridian bankrupt: False (cash balance: 16.45, starting capital: 40.0)
Result: PASS (score=0.80)