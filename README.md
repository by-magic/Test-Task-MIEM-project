# Test-Task-MIEM-project
Test task to the data collection project
# The Metropolitan Museum of Art 
## Задача
Данная работа нацелена на создание консольного приложения, которое поможет пользователю найти арт объект, хранящийся в коллекции музея, по ввёденному слову и вывести выбранную заранее информацию на экран: 
- покажет название произведения;
- покажет ФИО автора;
- покажет изображение;
- покажет дату создания;
- открывает в браузере страницу арт объекта на сайте музея.
## Ограничения и работа с API
Доступ к информации Метропόлитен-музея осуществляется по средствам REST API.
От пользователя не требуется предварительная регистрация на сайте музея или получения API key.

Ограничение составляет **не более 80 запросов** в секунду.
## Структура программы
Взаимодействие с API осуществляется в функции `btn_click` файла `main.py`:
```python
def btn_click():
    object_name = object_nameField.get()
    response = requests.get(
        'https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&isOnView=true&q={object_name}')
    res_to_json = response.json()
    length = len(res_to_json['objectIDs'])
    try:
        id = randint(0, length - 1)
        ob_id = res_to_json['objectIDs'][id]
        response1 = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(ob_id))
        res1_to_json = response1.json()
        ...
 ```
 Значение `object_name` вводится пользователем с клавиатуры и является термином, по которому производится поиск объектов с помощью запроса **search**.
 
 Далее из полученного словаря `res_to_json` выбирается случайным образом ID объекта и записывается в переменную `ob_id`. 
 
 Следующим шагом по переменной `ob_id` производится поиск всей информации об этом объекте с помощью запроса **object**.
## Структура API
В данной программе используется два вида запросов:
- **object** - возвращает запись, содержащую все данные, доступные для этого объекта;
- **search** - возвращает запись, содержащую ID объектов, данные которых удовлетворяют заданным параметрам поиска: заголовок, автор произведения, слово,содержащиеся в описании объекта, наличие изображения и т.д.
### API endpoint - object
Данный запрос выдаёт информацию об объекте по его ID: изображение, автор, год приобретения, год создания, название, ссылка на страницу объекта на сайте музея, размеры объекта и т.д.

С помощью Get запроса принимаем данные в переменную `response1`. Далее для удобства работы с данными, создадим JSON файл с этими данными.
```python
response1 = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/45734' )
res1_to_json = response1.json()
```
В качестве ответа, содержащегося в переменной `res1_to_json`, получаем **словарь** такого вида:

```python
{
    "objectID": 45734,
    "isHighlight": false,
    "accessionNumber": "36.100.45",
    "accessionYear": "1936",
    "isPublicDomain": true,
    "primaryImage": "https://images.metmuseum.org/CRDImages/as/original/DP251139.jpg",
    "primaryImageSmall": "https://images.metmuseum.org/CRDImages/as/web-large/DP251139.jpg",
    "additionalImages": [
        "https://images.metmuseum.org/CRDImages/as/original/DP251138.jpg",
        "https://images.metmuseum.org/CRDImages/as/original/DP251120.jpg"
    ],
    "constituents": [
        {
            "constituentID": 11986,
            "role": "Artist",
            "name": "Kiyohara Yukinobu",
            "constituentULAN_URL": "http://vocab.getty.edu/page/ulan/500034433",
            "constituentWikidata_URL": "https://www.wikidata.org/wiki/Q11560527",
            "gender": "Female"
        }
    ],
    "department": "Asian Art",
    "objectName": "Hanging scroll",
    "title": "Quail and Millet",
    "culture": "Japan",
    "period": "Edo period (1615–1868)",
    "dynasty": "",
    "reign": "",
    "portfolio": "",
    "artistRole": "Artist",
    "artistPrefix": "",
    "artistDisplayName": "Kiyohara Yukinobu",
    "artistDisplayBio": "Japanese, 1643–1682",
    "artistSuffix": "",
    "artistAlphaSort": "Kiyohara Yukinobu",
    "artistNationality": "Japanese",
    "artistBeginDate": "1643",
    "artistEndDate": "1682",
    "artistGender": "Female",
    "artistWikidata_URL": "https://www.wikidata.org/wiki/Q11560527",
    "artistULAN_URL": "http://vocab.getty.edu/page/ulan/500034433",
    "objectDate": "late 17th century",
    "objectBeginDate": 1667,
    "objectEndDate": 1682,
    "medium": "Hanging scroll; ink and color on silk",
    "dimensions": "46 5/8 x 18 3/4 in. (118.4 x 47.6 cm)",
    "measurements": [
        {
            "elementName": "Overall",
            "elementDescription": null,
            "elementMeasurements": {
                "Height": 118.4,
                "Width": 47.6
            }
        }
    ],
    "creditLine": "The Howard Mansfield Collection, Purchase, Rogers Fund, 1936",
    "geographyType": "",
    "city": "",
    "state": "",
    "county": "",
    "country": "",
    "region": "",
    "subregion": "",
    "locale": "",
    "locus": "",
    "excavation": "",
    "river": "",
    "classification": "Paintings",
    "rightsAndReproduction": "",
    "linkResource": "",
    "metadataDate": "2020-09-14T12:26:37.48Z",
    "repository": "Metropolitan Museum of Art, New York, NY",
    "objectURL": "https://www.metmuseum.org/art/collection/search/45734",
    "tags": [
        {
            "term": "Birds",
            "AAT_URL": "http://vocab.getty.edu/page/aat/300266506",
            "Wikidata_URL": "https://www.wikidata.org/wiki/Q5113"
        }
    ],
    "objectWikidata_URL": "https://www.wikidata.org/wiki/Q29910832",
    "isTimelineWork": false,
    "GalleryNumber": ""
}
```
### API endpoint - search
Данный запрос возвращает информацию об объекте, удовлетворяющему заданному параметру.

Список настраиваемых параметров:
| Параметр              | Тип                                                                        | Запись                                                                                                                                                                                                                                                    |   |   |
|-----------------------|----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---|---|
| q                     | поиск по термину(слову)                                                    | Возвращает список ID всех объектов, которые удовлетворяют данному условию                                                                                                                                                                                 |   |   |
| isHighlight           | Boolean, true or false. С учетом регистра.                                    | Возвращает объекты, соответствующие запросу и обозначенные как основные моменты. Это избранные произведения искусства из постоянной коллекции Музея Метрополитен, представляющие различные культуры и периоды времени.                       |   |   |
| title                 | Boolean, true or false. С учетом регистра.                                    | Возвращает объекты, у которых поле заголовка соответствует запросу.                                                                                                                                                        |   |   |
| tags                  | Boolean, true or false. С учетом регистра.                                    | Возвращает объекты, поля тегов которого (ключевые слова) соответствуют запросу.                                                                                                                                          |   |   |
| departmentId          | Integer                                                                    | Возвращает объекты, которые являются частью определенного отдела.                                        |   |   |
| isOnView              | Boolean, true or false. С учетом регистра.                                    | Возвращает объекты, которые соответствуют запросу и находятся в настоящее время в экспозиции музея.                                                                                                                                                                             |   |   |
| artistOrCulture       | Boolean, true or false. С учетом регистра.                                    | Возвращает объекты, соответствующие запросу, в частности, для поиска объектов по имени исполнителя или полю культуры.                                                                                                                                       |   |   |
| medium                | String, возможно несколько значений записанных через  \| оператор. С учетом регистра. | Возвращает объекты, соответствующие запросу и относящиеся к указанному материалу или типу объекта. Например: "Керамика", "Мебель", "Картины", "Скульптура", "Текстиль" и т.д.                                                                              |   |   |
| hasImages             | Boolean, true or false. С учетом регистра.                                    | Возвращает объекты, соответствующие запросу и имеющие изображения.                                                                                                                                                                              |   |   |
| geoLocation           | String, возможно несколько значений записанных через  \| оператор. С учетом регистра. | Возвращает объекты, соответствующие запросу и указанному географическому местоположению. Например: "Европа", "Франция", "Париж", "Китай", "Нью-Йорк" и т.д.                                                                                             |   |   |
| dateBegin and dateEnd | Integer. Вы должны использовать как dateBegin, так и dateEnd                          | Возвращает объекты, соответствующие запросу и находящиеся между параметрами dateBegin и dateEnd. Например: dateBegin=1700 и dateEnd =1800 для объектов с 1700 по 1800 год н.э. |   |   |
#### Примеры
isHighlight запрос:
```
https://collectionapi.metmuseum.org/public/collection/v1/search?isHighlight=true&q=sunflowers
```
```python
{
	"total": 3,
	"objectIDs": [
		437329,
		436121,
		436535
	]
}
```
Is On View запрос:
```
https://collectionapi.metmuseum.org/public/collection/v1/search?isOnView=true&q=sunflower
```
```python
{
	"total": 19,
	"objectIDs": [
		436524,
		11922,
		2032,
		// more results ...
	]
}
```
Medium запрос:
```
https://collectionapi.metmuseum.org/public/collection/v1/search?medium=Quilts|Silk|Bedcovers&q=quilt
```
```python
{
	"total": 15,
	"objectIDs": [
		229155,
		227076,
		229930,
		// more results ...
	]
}
```
Date Range запрос:
```
https://collectionapi.metmuseum.org/public/collection/v1/search?dateBegin=1700&dateEnd=1800&q=African
```

```python
{
	"total": 56,
	"objectIDs": [
		320993,
		188180,
		394199,
		// more results ...
	]
}
```
#### 

С помощью Get запроса принимаем данные в переменную `response`. Далее для удобства работы с данными, создадим JSON файл с этими данными.
```python
response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&isOnView=true&q=sunflower')
res_to_json = response.json()
```
В качестве ответа, содержащегося в переменной `res_to_json`, получаем **словарь** такого вида:
```python
{
	'total': 25, 
	'objectIDs': [
  	437112, 
    436524, 
    210191, 
    11922, 
    2032, 
    816522, 
    20141, 
    2019, 
    207869, 
    437115, 
    208218, 
    437984, 
    202228, 
    436534, 
    436252, 
    436580, 
    207753, 
    437526, 
    203893, 
    436121, 
    436529, 
    436144, 
    436530, 
    436535, 
    437980
  ]  
}
```
