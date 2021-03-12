# MHMelectric
MHMelectric is a system created for managing electric car charging. 

MHMelectric was created by [Markos Baratsas](https://github.com/markosbaratsas), [Maria Retsa](https://github.com/mariartc) and [Iliana Xigkou](https://github.com/IlianaXn), for the purposes of the [Software Engineering Course](https://courses.softlab.ntua.gr/softeng/2020b/) at [ECE NTUA](https://www.ece.ntua.gr/en).

The MHMelectric system consists of 3 components: backend, frontend and cli. Of course, there is some documentation for each of these components, as well as "higher-level" documentation, that presents the different Use Cases and different Stakeholders that could be involved in the MHMelectric system.


## Backend

[Django Framework](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/) were used for the development of the backend system. The MHMelectric Django project consists of 2 different Django apps, one for consumption of the CLI and REST API calls, and another for user management and backend-frontend communication.

## Frontend

[React JS](https://reactjs.org/) was used for the development of the frontend system.

## CLI

[Python Argparse](https://docs.python.org/3/library/argparse.html) module was used for the development of the CLI. The CLI consumes the REST API developed in the backend.
