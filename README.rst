Orange Button Checklist Registry
================================


Deployment
==========

Build image

.. code:: bash

   docker build -t django-ecs .

Test image

.. code:: bash

   docker run --rm -p 8000:8000 --name django-test django-ecs --bind 0.0.0.0:8000

Log into AWS (use sudo docker if you used this elsewhere)

.. code:: bash

   aws ecr get-login-password --region us-west-1 | sudo docker login --username AWS --password-stdin <account_number>.dkr.ecr.us-west-1.amazonaws.com


Tag image


.. code:: bash

   docker tag django-ecs:latest <account_number>.dkr.ecr.us-west-1.amazonaws.com/django-app-repo:latest


Push image to AWS

.. code:: bash

   docker push <account_number>.dkr.ecr.us-west-1.amazonaws.com/django-app-repo:latest
