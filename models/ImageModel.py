__author__ = 'hyeonsj'
from controllers import DbController
dc = DbController.DbController()


class ImageModel():

    class Image():
        def __init__(self):
            self.id = 0
            self.image_url = ""
            self.title = ""
            self.year = 0
            self.artist_id = 0
            self.description = ""

        def set(self, instance, column, value):
            setattr(instance, column, value)

        def to_dict(self, instance, filed_list):
            return_dict = dict()
            for filed in filed_list:
                return_dict[filed] = getattr(instance, filed)
            return return_dict

    def get(self, filed=None, artist_id=None, image_id=None):

        filed_list = []

        #특정 필드가 아니면 artist테이블의 모든 칼럼 이름을 가져와서 filed_list에 넣음
        if filed is None or filed is '':
            filed = "*"
            sql = " SHOW COLUMNS FROM images; "
            cur = dc.find(sql)

            for item in cur:
                filed_list.append(item[0])
        else:
            for item in filed.split(","):
                filed_list.append(item)

        sql = ""
        #todo 쿼리 정리하기
        if artist_id is not None and artist_id > 0 and image_id is None:
            sql = "SELECT "+filed+"  FROM images where artist_id = "+str(artist_id)

        if image_id is not None and image_id > 0 and artist_id is None:
            sql = "SELECT "+filed+"  FROM images where id = "+str(image_id)

        if artist_id > 0 and image_id > 0:
            sql = "SELECT "+filed+"  FROM images as i, artists as a where a.id = i.artist_id and i.id = "+str(image_id)+\
                  " and a.id = "+str(artist_id)

        cur = dc.find(sql)
        #에러일 경우 tuple 리턴
        if type(cur) is tuple:
            return cur

        return_instance_list = []
        for item in cur:
            #객체 생성 후 변수 삽입
            instance_artist = self.Image()

            for idx, column in enumerate(filed_list):
                instance_artist.set(instance_artist, column, item[idx])

            return_instance_list.append(instance_artist)

        return return_instance_list, filed_list

    def delete(self, artist_id, image_id=None):

        delete_and = ""

        if image_id is not None:
            delete_and = " and id = "+str(image_id)+" "

        sql = "delete from images where artist_id = " + str(artist_id) + delete_and
        cur = dc.delete(sql)

        if type(cur) is tuple:
            return cur

        else:
            return True

    def insert(self, instance_artist):

        image_dict = instance_artist.__dict__

        insert_columns = []
        insert_values = []
        columns = image_dict.keys()
        for artist_columns in columns:
            if artist_columns is not "id":
                if image_dict[artist_columns] is not None and image_dict[artist_columns] != "":
                    insert_columns.append(artist_columns)
                    if type(image_dict[artist_columns]) is str:
                        insert_values.append("'"+image_dict[artist_columns]+"'")
                    else:
                        insert_values.append(str(image_dict[artist_columns]))

        insert_columns = ",".join(insert_columns)
        insert_values = ",".join(insert_values)

        sql = "insert into images("+insert_columns+") value("+insert_values+")"
        dc.insert(sql)

        sql = "SELECT LAST_INSERT_ID();"
        cur = dc.find(sql)

        return cur

    def update(self, instance_artist, artist_id):

        artist_dict = instance_artist.__dict__
        update_set_list = []
        columns = artist_dict.keys()
        for artist_columns in columns:
            if artist_columns is not "id":
                if type(artist_dict[artist_columns]) is str:
                    update_set_list.append(artist_columns+"='"+artist_dict[artist_columns]+"'")
                else:
                    update_set_list.append(artist_columns+"="+str(artist_dict[artist_columns]))

        update_set_list = ",".join(update_set_list)

        sql = "update artists set "+update_set_list+" where id ="+str(artist_id)
        cur = dc.update(sql)

        return cur