CREATE PROCEDURE `csp_get_items_features` (itemsids VARCHAR(200))
BEGIN

if lenght(itemsids) > 0 then
	Set @filter = CONCAT('where a.restaurant_id in (',itemsids,')');
else
	Set @filter = '';
end if;    
Set @query  = CONCAT('select a.restaurant_id,GROUP_CONCAT(concat( a.feature_id,''|'',a.tf_idf)),count(1)
from (select restaurant_id,feature_id,tf_idf
from feature_to_sentences_rest_db inner join sentences_rest_db
on feature_to_sentences_rest_db.sentences_id = sentences_rest_db.id
',@filter,'
group by sentences_rest_db.restaurant_id,feature_to_sentences_rest_db.feature_id
order by feature_id) as a
group by restaurant_id
order by restaurant_id desc,GROUP_CONCAT(a.feature_id)');

PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
END
