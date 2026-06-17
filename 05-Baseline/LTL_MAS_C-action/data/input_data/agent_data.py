#agent_data:[(sequence number, place symbol,{service: True/False})]
agent_type={'UAV':{'serve':['goto','leader','follower','surrounder','searcher','evacuater','coverage_UAV'],'velocity':2.0},
            'UGV':{'serve':['goto','coverage_UGV','searcher','evacuater'],'velocity':1.0}}
# new structure:
# agent_date=[{'num':0,'init_place':'b','type':'UAV'}]
agent_data=[(0,'b','UAV'),
            (1,'d','UAV'),
            (2,'g','UAV'),
            (3,'g','UGV'),
            (4,'g','UGV'),
            (5,'a','UGV'),
            (6,'f','UGV'),
            (7,'b','UAV'),
            (8,'c','UGV'),
            (9,'b','UGV')]
            #(7,'b','UGV'),
            #(8,'b','UGV'),
            #(9,'b','UGV')]
    #,(10,'b'),(11,'b'),(12,'b'),(13,'d'),        (14,'f'),(15,'a'),(16,'d'),(17,'e'),(18,'f'),(19,'e')]
