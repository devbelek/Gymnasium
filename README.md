django-filter: 

    Фильтрация "Выпускники": /api/graduates/?year=2000 
    Фильтрация "Ученики по классам": /api/students/?school_grade=11, ?school_class__parallel=А
    Поиск по "Студенты": /api/students/?full_name=[ФИО(можно просто имя)]

`pip install poetry`
`poetry shell`
`poetry install`   


1) corsheaders сделать, когда фронтенд начнёт свою работу!
2) Объязательно при развёртывании установить Tesseract, Poppler!