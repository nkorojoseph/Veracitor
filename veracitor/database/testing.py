import unittest
from mongoengine import *
import globalNetwork
import tag
import producer
import user
import information
import group
import extractor
import datetime
from dbExceptions import *
connect('mydb')

graph = None

class GeneralSetup(unittest.TestCase):
    
    def setUp(self):

        self.tearDown()

        graph = globalNetwork.build_network_from_db()

        self.tag1 = tag.Tag(name="Gardening", 
                            description="Hurrr HURRRRRR")
        self.tag1.save()
        
        self.tag2 = tag.Tag(name="Cooking",
                            description="Hurrdidurr")
        self.tag2.parent.append(self.tag1)
        self.tag2.save()
        
        self.user1 = user.User(name="Lasse", password="123")
        self.user1.save()

        self.group1 = group.Group(name="KTH",
                                  owner=self.user1,
                                  tags=[self.tag1, self.tag2],
                                  time_created=datetime.\
                                      datetime.now())
        self.info1 = information.Information(title="dnledare",
                                             url="dn.se/ledare",
                                             time_published=datetime.datetime.now(),
                                             tags=[self.tag1])
        self.info2 = information.Information(title="SvDledare",
                                             url="svd.se/ledare",
                                             references=[self.info1],
                                             time_published=datetime.datetime.now(),
                                             tags=[self.tag1, self.tag2])
        self.info3 = information.Information(title="AftonbladetEntertainment",
                                             references=[],
                                             time_published=datetime.datetime.now(),
                                             tags=[self.tag2])
        self.prod1 = producer.Producer(name="DN",
                                       type_of="newspaper")
        self.prod2 = producer.Producer(name="SvD",
                                       type_of="newspaper")
        self.prod3 = producer.Producer(name="Aftonbladet",
                                       type_of="newspaper")
        self.info_rating1 = producer.InformationRating(rating=4, 
                                                       information=self.info1)
        self.info_rating2 = producer.InformationRating(rating=2,
                                                       information=self.info1)
        self.info_rating3 = producer.InformationRating(rating=1,
                                                       information=self.info2)
        self.info_rating4 = producer.InformationRating(rating=5,
                                                       information=self.info2)
        
        self.prod1.info_ratings.append(self.info_rating1)
        self.prod2.info_ratings.append(self.info_rating2)
        self.prod2.info_ratings.append(self.info_rating3)
        self.prod3.info_ratings.append(self.info_rating4)
        self.group1.save()
        self.info1.save()
        self.info2.save()
        self.prod1.save()
        self.prod2.save()
                                                       
                                                       
    def tearDown(self):
        for t in tag.Tag.objects:
            t.delete()
        for p in producer.Producer.objects:
            p.delete()
        for u in user.User.objects:
            u.delete()
        for g in group.Group.objects:
            g.delete()
        for i in information.Information.objects:
            i.delete()

class TestTagThings(GeneralSetup):

    def test_tag_model(self):
        assert self.tag2.parent[0].name == "Gardening"
        assert tag.Tag.objects(name="Cooking")[0].parent[0].\
            name == "Gardening"

    def test_tag_extractor(self):
        assert self.tag1 == extractor.get_tag("Gardening")
        assert self.tag1 in extractor.get_all_tags() and\
            self.tag2 in extractor.get_all_tags()
        assert extractor.contains_tag(self.tag1.name) == True
        assert extractor.contains_tag("Not a tag!") == False

    def test_tag_group(self):
        assert self.tag1 in self.group1.tags

class TestInformationThings(GeneralSetup):
    def test_info_extractor(self): 
        date1 = datetime.datetime(year=1970, month=12, day=24)
        date2 = datetime.datetime(year=2017, month=12, day=24)
        
        assert self.info1 in extractor.search_informations("d", [self.tag1],
                                                           date1, date2)
        assert extractor.contains_information(self.info1.title) == True
        assert extractor.contains_information("DEUS EX!!!") == False
        self.assertRaises(Exception, extractor.get_information, "Woo")
                                         
class TestProducerThings(GeneralSetup):
    
    def test_producer_extractor(self):
        assert self.prod1 in extractor.search_producers('dn', 'newspaper')
        assert self.prod2 in extractor.search_producers('d', 'newspaper')
        assert self.prod1 in extractor.search_producers('d', 'newspaper')
        assert self.prod1 not in extractor.search_producers('vd', 'newspaper')
        assert extractor.contains_producer(self.prod1.name) == True
        assert extractor.contains_producer("Should not exist!") == False

class TestGroupThings(GeneralSetup):
    
    def test_group_extractor(self):
        assert extractor.contains_group(self.group1.name) == True
        assert extractor.contains_group("Not a group!!") == False


class TestGlobalNetworkThings(GeneralSetup):
    
    def test_global_info_ratings(self):
        assert globalNetwork.get_common_info_ratings(self.prod1, self.prod2,[self.tag1])\
            == [(self.info_rating1, self.info_rating2,)]
        assert globalNetwork.get_common_info_ratings(self.prod1, self.prod2,[self.tag2])\
            == []
        assert globalNetwork.get_common_info_ratings(self.prod1, self.prod3,[self.tag1, self.tag2])\
            == []
        assert globalNetwork.get_common_info_ratings(self.prod2, self.prod3,[self.tag2])\
            == [(self.info_rating3, self.info_rating4,)]


if __name__ == "__main__":
    unittest.main()


