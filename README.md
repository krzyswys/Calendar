# Calendar
<h2 style="text-align: center"> Idea of the project was to create a calendaer API which can calculate many performance metrics and give usefull insigths into how time is spend on activities. Whole list of metrics can be found in statistics list.txt.</h2>
In order to run with dummy data and html view:
- python manage.py collectstatic
- python manage.py makemigrations calendar_events
- python manage.py migrate 
- python manage.py runserver


Database schema:
![image](https://user-images.githubusercontent.com/110239601/236347084-b45c7a45-ff7b-481c-b56d-538c4923d299.png)


Database view with dummy data
![image](https://user-images.githubusercontent.com/110239601/236087425-659dd0aa-bab8-446b-9351-8288fdba3e86.png)
![image](https://user-images.githubusercontent.com/110239601/236261574-24a2dff7-79ee-4c8d-ae91-3a7d8f3dabd4.png)
![image](https://user-images.githubusercontent.com/110239601/236087466-1c3b7bda-8bca-4093-a5d9-8baa9c0d38cb.png)
