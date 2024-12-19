# Bookstore Management System

**Authors:** Yiheng Liu (yl5354)      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Yiming Zhao (yz4579)

## 1. Application Overview
![alt text](images/image.png)
This application ([http://3.136.117.103:8111/](URL)) serves as a comprehensive platform for managing the trading activities and products of the University bookstore. It empowers administrators with tools to monitor, update, and streamline store operations while maintaining a user-friendly interface. Key features include:

1. **User Authentication:**
   - Users are registered with a `user_name` and password, stored securely in the `User` dataset.
   - On first login, users receive an `Admin-id` and `Admin-name`, defining their roles and responsibilities in the management hierarchy.

2. **Product and Customer Management:**
   - Administrators have the ability to add, update, and monitor products, including fields such as `id`, `title`, and `price`.
   - Customer information, including phone numbers and addresses, is updated semi-annually to align with the start of the fall and spring semesters.
   - Deletion of entities in datasets like `User`, `Admin`, `Customer`, and `Product` is restricted to predefined maintenance periods during winter and summer breaks.

3. **Application Constraints:**
   - The schema is designed to prevent unauthorized deletions outside maintenance windows, ensuring data integrity.

## 2. Major Software Components

### **System Architecture**
1. **Frontend:**
   - Provides login and management interfaces using responsive design principles.
   - Interacts with backend APIs for data operations.
2. **Backend:**
   - Implements user authentication, CRUD operations, and API endpoints using Flask.
   - Manages database operations via SQLAlchemy ORM.
3. **Database:**
   - PostgreSQL database hosted on AWS RDS.
   - Contains structured tables for `Users`, `Products`, `Orders`, and `Admin` data.
4. **Cloud Deployment:**
   - AWS EC2 instance serves as the primary hosting environment.
   - Nginx acts as a reverse proxy, and Gunicorn serves the Flask application.

## 3. Technologies Used

### **Frontend:**
- HTML, CSS, and JavaScript for web interfaces.

### **Backend:**
- **Flask Framework:** Python-based microframework.
- **SQLAlchemy:** Object Relational Mapper (ORM) for database operations.
- **Gunicorn:** Python WSGI HTTP server.

### **Database:**
- **PostgreSQL:** Relational database management system hosted on AWS RDS.

### **Cloud Services:**
- **AWS EC2:** Virtual server for hosting the application.
- **AWS RDS:** Managed database service for PostgreSQL.
- **AWS Elastic IP:** Ensures consistent public IP for the EC2 instance.
- **Nginx:** High-performance HTTP server for reverse proxying.


## 4. Cloud Infrastructure

### Database Setup
1. **Database Construction:**
![alt text](image-4.png)
   - Access the AWS RDS Console to configure a new PostgreSQL database:
     - **Instance Class:** `db.t2.micro` (Free tier eligible).
     - **Storage:** Minimal allocation to optimize cost.
     - **Credentials:** Specify a robust master username and password.
   - Ensure the database is publicly accessible for development, with security groups restricting IP-based access.

2. **Table and Relationship Creation:**
![alt text](image-3.png)
   - Use SQL Pro Studio or equivalent tools to connect to the RDS database with appropriate credentials.
   - Define tables and relationships with PostgreSQL commands, incorporating constraints and references to maintain data consistency.

## 5. Backend Development (Flask)
![alt text](image-5.png)

1. **Project Initialization:**
   - Establish a Python virtual environment and install required dependencies:
     ```bash
     pip install flask flask_sqlalchemy flask_bcrypt flask_jwt_extended
     ```
   - Develop API endpoints for user registration, login, and CRUD operations for data management.

2. **Database Integration:**
   - Set up the database URI using the RDS endpoint:
     ```python
     DATABASEURI = "postgresql://ELENDB:Ipromise12345@database-2.c9yesue8cf71.us-east-2.rds.amazonaws.com:5432/ELEN"
     ```
   - Implement SQLAlchemy for seamless database interactions.

3. **API Testing:**
   - Validate API functionality using tools like Postman or curl to simulate client requests.

---

## 6. Frontend Development
The front-end interface is crafted using HTML templates and styled with CSS to ensure accessibility and usability for administrative users. Responsive design principles are applied to enhance user experience across devices.
![alt text](image-6.png)

---

## 7. Deployment on AWS EC2

### EC2 Instance Setup
![alt text](image-7.png)
1. **Instance Initialization:**
   - Launch an Ubuntu-based EC2 instance under the free tier and connect via SSH:
     ```bash
     ssh -i "<key_pair>.pem" ubuntu@<ec2_public_ip>
     ```

2. **Environment Preparation:**
   - Update the system and install essential packages:
     ```bash
     sudo apt update
     sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
     ```

3. **Application Deployment:**
   - Clone the GitHub repository containing the project code:
     ```bash
     git clone https://github.com/IAN0201/6770-Project-Bookstore-Management.git
     ```
   - Install application dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Run the application locally to confirm functionality before deployment.

### Production Configuration
1. **Gunicorn Setup:**
   - Define a systemd service file for Gunicorn:
     ```bash
     sudo nano /etc/systemd/system/gunicorn.service
     ```
     Add the following configuration:
     ```ini
     [Unit]
     Description=Gunicorn instance to serve Flask app
     After=network.target

     [Service]
     User=ubuntu
     Group=www-data
     WorkingDirectory=/home/ubuntu/apiv1
     Environment="PATH=/home/ubuntu/apiv1/env/bin"
     ExecStart=/home/ubuntu/apiv1/env/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8111 server:asgi_app

     [Install]
     WantedBy=multi-user.target
     ```
   - Enable and start the service to ensure persistent availability:
     ```bash
     sudo systemctl start gunicorn
     sudo systemctl enable gunicorn
     ```
2. **Nginx Configuration:**
   - Configure Nginx to act as a reverse proxy for Gunicorn:
     ```bash
     sudo nano /etc/nginx/sites-available/api
     ```
     Insert the following block:
     ```nginx
     server {
         listen 80;
         server_name <server_ip>;

         location / {
             proxy_pass http://127.0.0.1:8111;
         }
     }
     ```
   - Test the configuration and restart the Nginx service:
     ```bash
     sudo nginx -t
     sudo systemctl restart nginx
     ```
2. **Elastic IP Allocation:**
   - Allocate an Elastic IP to ensure a consistent public-facing address for the application.

### Accessing the Application
Access the fully deployed application using the public IP: [http://3.136.117.103:8111/](URL)
![alt text](image-1.png)
