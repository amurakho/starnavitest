### Requests to api: 
####         'register': 'http://127.0.0.1:8000/api/accounts/register/',
####         'get_jwt': 'http://127.0.0.1:8000/api/token/',
####         'posts': 'http://127.0.0.1:8000/api/posts/',

##### i use base login template for rest framework and use rest_registration

####  i use rest_framework_simplejwt because its recommended in the documentation

## API:
### Models:
#### i made 3 models: Post, Like, UserActivity (the names speak for themselves)

### Serializers
#### PostSerializer, LikeSerializer, AnalyticsByDaySerializer, MyTokenObtainPairSerializer (the names speak for themselves)

### Views
#### PostViewSet - also has two methods - like(to manage like) and get_likes(get likes by post). get_likes_by_period-view (the name speak for themselves) 

### Also:
#### lastrequestmiddleware - make an endpoint of request.
#### signals - endpoint of login


## BOT:
#### my bot(automated_bot) use a config_for_bot.ini file for configurate. It parse parameters and create object of StarnaviBot class. This bot take each parameter and work with it. 
#### 1 action - user creating. I create a random user name for each user and static password for all. When i create the user, i save it into csv file for a future.
#### 2 action - post creation. For each user i get a random(to max) value of posts. 
#### 3 action - post likes. FOR EACH USER: at first i get a list of all posts in base and take their id's. Next i take a random id and like/unlike it.

#### NOTE: i didt make test and didn use logging. I just use print for loggin because i think the better solution for logging its to make it with decorators. So i did think that the task need this
#### NOTE: if you create superuser from manage.py it didnt create UserActivity model because this model are created in signals. So to solve it i should create custom manager for my model. And i didt create it because i have no task to work with admin