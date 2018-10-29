# File Online Media

### Course Details

 University Name: http://www.sjsu.edu/ \
 Course: Cloud Technologies \
 Professor: [Sanjay Garje](https://www.linkedin.com/in/sanjaygarje/) \
 ISA: [Anushri Srinath Aithal](https://www.linkedin.com/in/anushri-aithal/)

### Demo
- Put the Video here

### File Online Media Introduction

File Online Media, is a web application hosted on AWS cloud which intends to provide users to maintain their files on cloud. 
It is 3 Tier Web Application which uses AWS building blocks to achieve highly available, scalable solution.
File Online Media application leverages AWS auto scaling functionality to provide seamless experience during peak load times. 
The application also monitors the health of the EC2 associated with auto scale group using Cloud Watch and SNS. 
Users can perform the following activities on the portal using AWS VPC and S3 Transfer Acceleration.

- Upload file 
- Download Files 
- Delete Files on S3

There is admin user login who has the previllage following previllage
 - View all user files
 - Delete any user file
 - Delete any user 
 
 ### Basic 3 Tier Architechture
 <img width="1648" alt="screen shot 2018-10-29 at 4 20 16 am" src="https://user-images.githubusercontent.com/42690026/47646727-0f84a880-db32-11e8-9597-7d49e365065e.png">

 
 ### AWS Architecture
 <img width="1679" alt="screen shot 2018-10-29 at 4 20 26 am" src="https://user-images.githubusercontent.com/42690026/47646731-13b0c600-db32-11e8-9b49-4b7c8f4b16db.png">
 
 ### Feature List
 
##### Users can perform the following activities on the portal 
•	Register users \
•	Upload file into S3 \
•	Download Files from S3 via Cloud Front \
•	Delete Files from S3 \
•	Edit the already uploaded files to rename and change description.
##### Admins Users can perform the following activities on the portal 
•	Upload file to S3 as regular users \
•	Download Files from S3 via Cloud Front of any user \
•	Delete Files on S3 of any user files \
•	Edit the already uploaded files to rename and change description. \
•	Delete any other users 
 ### AWS components Leveraged 
•	Used route-53 to forward the domain to the elastic beanstalk \
•	Load Balancers are provisioned with 2min-4Max EC2 instances \
•	Auto-scaling group provisioned to scale up on peak demand \
•	EC2 instances with AMI are used for hosting the web-services APP. \
•	S3 bucket has been used with web scale multi-site architecture \
•	S3 Transfer Acceleration: S3 bucket is enabled with Transfer Acceleration to enable faster and secure transfer of files to S3. \
•	S3 life cycle policy with 75 days policy to move to S3-1A  \
•	Amazon Glacier used after 365 days archive \
•	Cloud front delivery with S3 bucket has been provisioned with low TTL \
•	Aurora RDS with multi-site disaster recovery and read replication \
•	AWS Lambda function to monitor the file upload/download activity \
•	Cloud watch to collect the lambda generated logs and monitor the EC2 instance health \
•	SNS configured to send email to admin when the EC2 instance goes down below threshold.
 
 ### Deployment Instructions 
 
a.	Prerequisite Software: Python 3.6 development environment using Flask and Boto3 \
b.	Download the application code from the github using git pull command \
c.	Pip3 Install all the dependency given in the requirements.txt \
d.	Provision your AWS environment using awscli and make sure following file has been created to have the right access \
cat ~/.aws/config \
[default] \
output = json \
region = us-west-1 \
rds_host    = <your rdb_host url> \
username    = <your rds admin user name > \
password    = <your rds admin password > \
db_name     = <RD DB name where user table is created> \
s3_bucket   = "S3 bucket" \
e.	Run “python application.py” \
f.	Open the web browser and access the webpage “http://127.0.0.1:5000/” to test the functionality \
g.	Once everything is working we can use the following code pipeline to deploy/test and move to production automatically
 
 ### Sample Screenshots
 #### Login
 <img width="1216" alt="screen shot 2018-10-29 at 4 02 06 am" src="https://user-images.githubusercontent.com/42690026/47646278-a6506580-db30-11e8-89c8-56b05e33acbf.png"> 
 
 #### New User
<img width="1035" alt="screen shot 2018-10-29 at 4 02 20 am" src="https://user-images.githubusercontent.com/42690026/47646459-3abac800-db31-11e8-93e6-c601d8464185.png"> 
#### File Listing
<img width="1290" alt="screen shot 2018-10-29 at 4 02 42 am" src="https://user-images.githubusercontent.com/42690026/47646472-40b0a900-db31-11e8-8bd0-71851d60f3f2.png">
 #### User Listing
<img width="1259" alt="screen shot 2018-10-29 at 4 03 20 am" src="https://user-images.githubusercontent.com/42690026/47646481-44dcc680-db31-11e8-85e6-93f1e439dd93.png">
 #### File Editing
<img width="1112" alt="screen shot 2018-10-29 at 4 03 44 am" src="https://user-images.githubusercontent.com/42690026/47646484-46a68a00-db31-11e8-9a8c-ebcb6c02eacb.png">
