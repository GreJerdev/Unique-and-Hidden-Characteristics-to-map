CREATE DEFINER=`root`@`localhost` PROCEDURE `csp_get_item_reviews_id_by_item_id`(in_item_id int(6))
BEGIN
	select review_id
	from feature_to_sentences_rest_db inner join sentences_rest_db
	on feature_to_sentences_rest_db.sentences_id = sentences_rest_db.id
	where sentences_rest_db.item_id = in_item_id 
	group by review_id;
END