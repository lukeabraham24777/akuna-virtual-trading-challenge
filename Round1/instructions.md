Fill in the MarketMaker class in trader.py.
The rest of the trader.py file contains the objects this class operates on;
you may need them, construct them, and add helpers, but any changes you make to them will not be reflected by the autograder.

Your market maker trades binary options (a.k.a. "event contracts") on three ficticious daily-evolving underlying:
1. The fed funds rate ("FED"),
2. The valuatino of AjarAI ("AJR"), a private frontier AI research lab, and 
3. The valuation of Theriodic ("THR"), a different private frontier AI research lab. 

These options are represented by the BinaryOption class. 
Each option pays out 1.0 at expiry if the event it represents occurs, and 0.0 otherwise.
Some example events include:
1. Fed rate greater than or equal to 3.0 in 3 days
2. Theriodic valuation greater than or equal to $1 trillion in 5 days
3. AjarAI valuation greater than or equal to Theriodic valuation in 2 days

Note that although the BinaryOption class can represent options with any amount of legs, in practice you will only encounter single-legged options, or "spreads" on whether AjarAI or Theriodic has a higher valuation like the third example above. 

Orders will come in via two distinct pipelines. For RFQ (request-for-quote) orders, the exchange will request quotes from all the participating market makers, and route the order to the highest bid or lowest offer it receives, splitting up the order if necessary. Therefore, your quote method should return the most competitive prices and quantities you are able to trade on. Note that you will not know ahead of time whether the RFQ is a buy or sell order. FOK (fill-or-kill) orders give you all the information up front, and it is up to you whether you want to trade them, via your return value from respond_to_fok. If multiple market makers denote that they want to trade an FOK order, it will be broken up between them. 

The evolution of the underlying prices is controlled by a join distribution paramterized by MarketParameters. The first test, THEO, will score whether you correctly price binary options given the true MarketParameters via the method price_option_from_parameters; the other tests will all provide a warm-up MarketHistory object from which you should estimate the MarketParameters. 

The first three tests after the THEO test are denoted VERBOSE -- these are short tests which output helpful logs to assist with debugging your MarketMaker. You will recieve full points for these tests so long as your code does not error and your MarketMaker does not go bankrupt. 

The remaning 16 tests are SCORED, and your score will vary based on your performance. You will receive full credit for being the top market maker in the session by PnL, zero credit for going bankrupt (or code errors), and pratial credit for avoiding bankruptcy. These tests will also vary in difficulty, including via different counterparties and different competing market makes. 

A note on bankruptcy: the autograder will keep track of cash balance, separate of the balance you may store on your MarketMaker. Every time you do a trade, your balance will decrease by the maximum loss of your trade. So if you buy 5 contracts for $0.20 each, your cash balance will go down by a dollar; if you sell 5 contracts at $0.20 apiece, your cash balance will go down by $4. Cash solvency is checked at the end of each day. First, any payoffs associated with expired options will be credited -- not that this process can only increase your balance. At this point if your cash balance is below zero, you will be marked as bankrupt, and the session will end early. 