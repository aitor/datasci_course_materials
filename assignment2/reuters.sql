## A - ok
select count(*) from Frequency where docid ='10398_txt_earn';

## B - ok
select count(term) from Frequency where docid ='10398_txt_earn' and count = 1;

## C - ok
select count(*) from(
	select term from Frequency where docid ='10398_txt_earn' and count = 1 
	UNION
	select term from Frequency where docid = '925_txt_trade' and count = 1
);

## D - ok
SELECT count(*) FROM (select docid from Frequency where term = 'legal' or term='law' group by docid) x;

## E - ok
select count(*) from(select docid from Frequency group by docid having count(term) > 300);

## F - ok
SELECT docid FROM Frequency where term='transactions' group by docid 
INTERSECT 
SELECT docid FROM Frequency where term='world' group by docid;

## G 
select * from a, b where a.row_num = 2 and b.col_num = 3;


## H 
## I 