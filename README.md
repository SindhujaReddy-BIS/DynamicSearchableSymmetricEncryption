Dynamic Searchable Symmetric Encryption (DSSE) for Secure Healthcare Data



Project Overview



This project implements a "secure healthcare data management system" using "Dynamic Searchable Symmetric Encryption (DSSE)". It enables patients and doctors to securely store, search, and retrieve encrypted medical data from a cloud server while ensuring "data privacy and security".





\## Key Features



\*  Secure data storage using "AES Encryption"

\*  Search over encrypted data (DSSE technique)

\*  Role-based access (Patient, Doctor, Cloud Server, Trusted Authority)

\*  Upload and retrieve medical reports securely

\*  Key generation and management system

\*  Cloud-based data handling

\*  Dynamic updates (add/delete/search data securely)



\##  System Architecture



The system consists of the following modules:



\* Patient Module – Upload encrypted medical data and request access

\* Doctor Module – Request and view decrypted patient reports

\* Cloud Server– Stores encrypted data securely

\* Trusted Authority (TA)– Manages keys and authorization





\## Tech Stack



\* Backend: Python, Django

\* Frontend: HTML, CSS, Bootstrap

\* Database: SQLite

\* Security: AES Encryption, DSSE

\* Tools: Git, GitHub





\##  How to Run the Project



\# Clone the repository



```bash

git clone https://github.com/SindhujaReddy-BIS/DynamicSearchableSymmetricEncryption.git

cd DynamicSearchableSymmetricEncryption```





\#Activate environment (Conda)



```bash

conda activate env

```



\#Install dependencies



```bash

pip install django cryptography

```



\# Run migrations



```bash

python manage.py migrate

```



\# Start server



```bash

python manage.py runserver

```



\# Open in browser



```

http://127.0.0.1:8000

```



\---



\#Security Highlights



\* Ensures confidentiality of sensitive healthcare data

\* Supports secure search without decrypting entire dataset

\* Provides forward and backward security

\* Prevents unauthorized access using role-based authentication



\---



\##  Use Cases



\* Secure hospital data management systems

\* Cloud-based healthcare applications

\* Privacy-preserving data sharing systems



\---



\##  Future Enhancements



\* Integration with Quantum Key Distribution (QKD)

\* Deployment on cloud platforms (AWS/Azure)

\* Advanced search optimization for large datasets

\* Real-time analytics dashboard



\---



\# Author



Sindhuja Reddy



GitHub: https://github.com/SindhujaReddy-BIS



