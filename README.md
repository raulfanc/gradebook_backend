a Django REST Framework (DRF) application that handles a gradebook system for a school, work with ReactJS to build a frontend

- viewsets.py: This file includes a ViewSet for each model in your Django app. ViewSets are a type of class-based View,
that provide CRUD operations without having to explicitly define methods for each operation. Each ViewSet defines the
queryset of objects it handles, the serializer to use for formatting responses, and the permissions necessary to
interact with the endpoint.

- models.py: This file describes the data models for the application. Django uses these models to create the corresponding
database tables. Here, you have models representing semesters, courses, lecturers, students, classes, and enrolments.

- permissions.py: This file defines custom permission classes for the application. These classes define who can perform
what actions. For example, there are permissions for students and lecturers, where lecturers can update grades and
students can view grades.

- serializers.py: Serializers in DRF are similar to Django forms and allow complex data types, like querysets and model
instances, to be converted to Python datatypes that can then be easily rendered into JSON, XML, or other content types.

- views.py: This file contains the definition of additional endpoints for entering student marks and viewing student
marks. These endpoints use the @api_view decorator, which is a function-based view for handling API endpoints.

- urls.py: There are two urls.py files. The one in the app directory registers the ViewSets with a router, which
automatically generates a set of URLs for the defined ViewSets. It also defines URL patterns for the additional views
defined in views.py. The other urls.py in the project directory includes the app's urls and a URL for obtaining an
authentication token.