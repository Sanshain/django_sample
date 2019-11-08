# -*- coding: utf-8 -*-

import random
import datetime
from django.conf import settings

from django.core.files.storage import FileSystemStorage                         # используется в settings.DEFAULT_FILE_STORAGE для полей моделей











class STORAGE:
    MESSAGES = 'media_messages/'
    NOTES = 'notes_media/'



class FileStorage:

##    unique_pair = (0, [])                                                       # мс, все занятые айди - на случай, если делать его глобальным

    def __init__(self, user_id ='', sub_path = 'media_messages/', diap=1000000):
        self.__uniques = []
        self.__sphere = diap
        self.__deep_rec = 10
        self.sender = user_id

        self.PATH = settings.MEDIA_ROOT + sub_path                                  # path

    def _get_unique(self, deep=0):

        rand = random.randint(0, self.__sphere)
        if rand in self.__uniques:
            if deep < self.__deep_rec:
                deep+=1
                return self._get_unique(deep)
            else:
                raise OverflowError('Overflow for recursion in Keeper')
        else:
            self.__uniques.append(rand)
            return str(rand)


    def image_save(self, image_file, deep=0):

        # проверяем расширение файла
        file_extension = image_file.name.split('.')[-1]
        if file_extension not in ('jpg','jpeg','png','gif'):
            print 'not allowed exception'
            print '**************************************'
            return False

        # генерируем уникальное имя
        a = datetime.datetime.now()
        b = datetime.datetime(2000, 1, 1, 1, 1, 1)
        d = ((a-b).total_seconds()*1000).__repr__()[:-2]

        name = '{}_{}_{}.{}'.format(
            str(self.sender),
            d,
            self._get_unique(),
            file_extension)

        # сохраняем объект
        try:
            destination = open(self.PATH + name, 'wb+')
            print name

            for chunk in image_file.chunks():
                destination.write(chunk)
            destination.close()

        except FileExistsError:
            raise Warning('inside image_save: its impossible! I dont believe it')        # даже рекурсивные попытки делать не надо

            if deep < self.__deep_rec:

                import time
                time.sleep(1)

                deep+=5
                self.image_save(image_file, deep)

            return False

        return name



