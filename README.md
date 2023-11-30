# Calendar
<h2 style="text-align: center"> Idea of the project was to create a calendaer API which can calculate many performance metrics and give usefull insigths into how time is spend on activities..</h2>

 <h2>Main Tasks Metrics:</h2>
  <ul>
    <li>Efficiency in relation to priority level for each task</li>
    <li>Efficiency without considering priority level for each task</li>
    <li>Number of tasks completed on time with a given priority</li>
    <li>Number of tasks completed within the slide time with a given priority</li>
    <li>Total number of tasks completed on time before the deadline</li>
    <li>Total number of tasks completed within the slide time</li>
    <li>Number of tasks completed up to the expected completion</li>
    <li>Check what percentage of tasks in a given category is completed within different timeframes (until now / overall) (deadline, slide, expected completion)</li>
    <li>Average delay for tasks in a specific category concerning different timeframes (deadline, slide, expected completion)</li>
    <li>Average delay for tasks at a specific priority level concerning different timeframes (deadline, slide, expected completion)</li>
    <li>Amount of time tasks from a specific category take</li>
    <li>Amount of time tasks at a specific priority level take</li>
    <li>Total time taken by events from a specific category</li>
    <li>Percentage of events in a specific location</li>
    <li>Percentage of events with a particular priority level</li>
  </ul>

  <h2>Subtasks Metrics:</h2>
  <ul>
    <li>Total time spent on a task + its subtasks</li>
    <li>Percentage of task completion, including its subtasks (100 * number of completed subtasks / total number of subtasks)</li>
    <li>Task + its subtasks - how many were completed within the expected time, how many within the expected time plus a delay, how many before the deadline, how many after the deadline</li>
    <li>Average time between completing subtasks and their expected completion date</li>
    <li>Average time between completing subtasks and their expected completion date + delay (if completed after the expected date)</li>
    <li>Average time between completing subtasks and their deadline (if not completed by the expected date + delay)</li>
    <li>Average time between the deadline and completing subtasks (if completed after the deadline)</li>
  </ul>

In order to run with dummy data and html view:
<ul>
    <li><code>python manage.py collectstatic</code></li>
    <li><code>python manage.py makemigrations calendar_events</code></li>
    <li><code>python manage.py migrate</code></li>
    <li><code>python manage.py runserver</code></li>
</ul>



Database schema:
![image](https://user-images.githubusercontent.com/110239601/236347084-b45c7a45-ff7b-481c-b56d-538c4923d299.png)


Database view with dummy data
![image](https://user-images.githubusercontent.com/110239601/236087425-659dd0aa-bab8-446b-9351-8288fdba3e86.png)
![image](https://user-images.githubusercontent.com/110239601/236261574-24a2dff7-79ee-4c8d-ae91-3a7d8f3dabd4.png)
![image](https://user-images.githubusercontent.com/110239601/236087466-1c3b7bda-8bca-4093-a5d9-8baa9c0d38cb.png)
