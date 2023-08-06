.. role:: raw-html-m2r(raw)
   :format: html



.. image:: https://github.com/vinyguedess/alcherializer/actions/workflows/main.yml/badge.svg
   :target: https://github.com/vinyguedess/alcherializer/actions/workflows/main.yml
   :alt: Github Actions


.. image:: https://api.codeclimate.com/v1/badges/332cfdc498df9f6dc272/maintainability
   :target: https://codeclimate.com/github/vinyguedess/alcherializer/maintainability
   :alt: Maintainability


.. image:: https://api.codeclimate.com/v1/badges/332cfdc498df9f6dc272/test_coverage
   :target: https://codeclimate.com/github/vinyguedess/alcherializer/test_coverage
   :alt: Test Coverage


Alcherializer
=============

A "Django like" model serializer.

Declaring Serializer
--------------------

It's very simples to declare a serializer. Just like Django, the only
thing you need is to create a class with a Meta class inside and
a model attribute.

This instantly maps all fields declared in model.

.. code-block:: python

   from datetime import datetime
   from alcherializer import Serializer
   import sqlalchemy


   class User:
       name = sqlalchemy.Column(sqlalchemy.String(100))
       age = sqlalchemy.Column(sqlalchemy.Integer)
       is_active = sqlalchemy.Column(sqlalchemy.Boolean)
       created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)


   class UserSerializer(Serializer):
       class Meta:
           model = User

PS: For further exemplifications we will always use **User** and **UserSerializer**.

Data
----

Gets a dictionary of a single model.

.. code-block:: python

   model = User(
       name="Clark Kent",
       age=31,
       is_active=True)

   serializer = UserSerializer(model)
   serializer.data  # { "name": "Clark Kent", ... }

Or, a list of models

.. code-block:: python

   model = User(
       name="Clark Kent",
       age=31,
       is_active=True)

   serializer = UserSerializer([model], many=True)
   serializer.data  # [{ "name": "Clark Kent", ... }]

Validation
----------

To validate a payload, it's possible to send it through data argument while
instantiating the serializer and call **.is_valid** method.

.. code-block:: python

   serializer = UserSerializer(data={
       "name": "Clark Kent",
       "age": 31,
       "is_active": True
   })
   serializer.is_valid()  # True

Fetching validation errors
^^^^^^^^^^^^^^^^^^^^^^^^^^

If any error happens you can fetch the information through error attribute.

.. code-block:: python

   serializer = UserSerializer(data={
       "name": "", # If ommitted or None should present error too
       "age": 31,
       "is_active": True
   })
   serializer.is_valid()  # False
   serializer.errors # {"name": ["Can't be blank"]}

Fields
------

This shows off how fields are mapped from SQLAlchemy models.

.. list-table::
   :header-rows: 1

   * - Model attribute
     - Alcherializer field
     - Validations
   * - Boolean
     - BooleanField
     - :raw-html-m2r:`<ul><li>[x] Required</li><li>[x] Valid boolean</li></ul>`
   * - BigInteger, Integer, SmallInteger
     - IntegerField
     - :raw-html-m2r:`<ul><li>[x] Required</li></ul>`
   * - String, Text Unicode
     - StringField
     - :raw-html-m2r:`<ul><li>[x] Required</li><li>[x] Max length</li></ul>`

