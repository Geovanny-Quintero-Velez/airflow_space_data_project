# Airflow Space Project
Project for practice knowledge obtained with the course: Foundations of Apache Airflow from Platzi.

It this project is explored the creation of DAGs, making them communicate through the use of FileSensors and ExternalTaskSensors, extracting data from the SpaceX API and simulate the issuing of permission from NASA to extract data and then generate the data. Finally the airflow pipeline send notifications through email to the analytics team. 

# Project results

## DAG orchestation

![DAG orchestation](doc_images\Airflow_DAG_orchestation.jpg)

## Tasks orchestation

### NASA permission issuer:

#### Tasks
- Inform the logical date of the dag
- Create the permission in a txt file
- Succes notification: Notify about operation success if the permission creator works correctly
- Error notification: Notify about operation failure if the permission creator does not work correctly

![Issuer](doc_images\NASA_issuer_graph.png)

### NASA permission checker:

#### Tasks
- Inform the logical date of the dag
- Check if the permission file is created
- Validate permission format and content
- Succes notification: Notify about operation success if the permission check works correctly
- Error notification: Notify about operation failure if the permission check does not work correctly

![NASA checker](doc_images\permission_checker.png)

### NASA data consumer:

#### Tasks
- Inform the logical date of the dag
- Watch if the permission checker validation task was executed
- Mock data consumption from NASA satellite (Generate data)
- Succes notification: Notify about operation success if the NASA data ingestion works correctly
- Error notification: Notify about operation failure if the NASA data ingestion does not work correctly

![NASA consumer](doc_images\NASA_data_consumer.png)

### SpaceX API consumer:

#### Tasks
- Inform the logical date of the dag
- Obtain data through SpaceX API about key milestones in SpaceX space travel and save it in csv
- Validate that data file is not empty
- Succes notification: Notify about operation success if the API consumption works correctly
- Error notification: Notify about operation failure if the permission creator does not work correctly

![SpaceX consumer](doc_images\SpaceX_API_consumer.png)

### data completeness checker:

#### Tasks
- Inform the logical date of the dag
- Check NASA data is present
- Check SpaceX data is present
- Notify that both data files are present

![Completness checker](doc_images\data_completeness_checker.png)

### Notification sender:

#### Tasks
- Inform the logical date of the dag
- Watch if the data completeness validation task was executed
- Use EmailOperator to send an email notification to analytics team
- Succes notification: Notify about operation success if the email notification sender works correctly
- Error notification: Notify about operation failure if the email notification sender does not work correctly

![Notification sender](doc_images\email_sender.png)

## Email notification sent

![Email sent](doc_images\email_notification.png)

# Running the project

Clone this github repository and execute this steps

Into the **config** folder change the file **airflow.cfg** with the credentials to send emails. It must have the following content:

``` ini

[smtp]

smtp_host = smtp.gmail.com
smtp_starttls = True
smtp_ssl = False
smtp_user = your_email@gmail.com
smtp_password = <Your gmail's app password>
smtp_port = 587
smtp_mail_from = your_email@gmail.com
smtp_timeout = 30
smtp_retry_limit = 5

```

To create an app password, follow the steps:

- Visit [https://myaccount.google.com/security](https://myaccount.google.com/security)
- Go to two-step verification
- Go to app passwords
- Give a name to your password
- Copy and paste the password in the field **smtp_password**

As next, create a 'secrets' folder containing a txt file. The file should have the following name **email_receiver.txt** and as content the email address of the receiver account:

``` txt

<receiver_address>@gmail.com

```

Now you are ready to execute the project!

Execute the following command in the project's root folder:

``` bash

docker-compose up

```

Visit [http://localhost:8080/home](http://localhost:8080/home). Insert the credentials:
- Username: airflow
- Password: airflow

Go to **Admin** on the navbar and select **connections**. Set a connection **fs_default** with type **File (path)** and press save:

![Issuer](doc_images\connection.png)

Now you are ready!
