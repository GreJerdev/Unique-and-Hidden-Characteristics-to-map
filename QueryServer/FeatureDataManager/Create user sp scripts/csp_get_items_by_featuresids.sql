CREATE DEFINER=`root`@`localhost` PROCEDURE `csp_get_items_by_featuresids`(featureids VARCHAR(500))
BEGIN
Set @query  = CONCAT('
select a.restaurant_id,GROUP_CONCAT(a.feature_id) as features_in_item,count(1) as count
from (select restaurant_id,feature_id
from feature_to_sentences_rest_db inner join sentences_rest_db
on feature_to_sentences_rest_db.sentences_id = sentences_rest_db.id
where feature_to_sentences_rest_db.feature_id in (',featureids,')
group by sentences_rest_db.restaurant_id,feature_to_sentences_rest_db.feature_id
order by feature_id) as a
group by restaurant_id
order by Count(1) desc,GROUP_CONCAT(a.feature_id);
');


PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;



END