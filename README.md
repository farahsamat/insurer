# SIMPLE INSURER APP FOR INSURANCE POLICY UPDATE AND PAYMENTS

The project background, instructions and requirements are specified [here](https://bitbucket.org/paysure/hiring-test-project/src/master/README.md).


## Solution
##### Policy
The combination of `external_user_id`, `benefit` and `currency` is the unique identification for each policy and there should not be duplicates.

Example:

*din_djarin might have multiple policies for different benefits (dentist, psychiatrist, physician) and possibly different currencies (GBP, USD, MYR, etc.).*

*Policy 1: din_djarin, physician, GBP*

*Policy 2: din_djarin, psychiatrist, USD*

*Policy 3: din_djarin, dentist, USD*

##### Making a payment
With user inputs `external_user_id`, `benefit` and `currency`, the app will query the database based on the given inputs. 

This could be visualised as:
```
select * from POLICY 
where external_user_id == 'din_djarin' and benefit == 'dentist' and currency == 'GBP'
```

The next constraint that has to be met is the `amount` specified by the user in this transaction plus all other `amount`'s that have been authorized for payment must not exceed the `total_max_amount`.
```
amount(now) + amount(previous1) + amount(previous2) + amount(previous4) +... <= total_max_amount
```

Payment will only be authorized when these two conditions are met.

Notice `amount(previous4)` instead of `amount(previous3)` in the above inequality. This is to demonstrate that only authorized previous payments are considered in this inequality. 


##### Adding a new policy
Since `external_user_id` + `benefit` + `currency` is the unique policy identification, the app will prompt for these inputs from the user. 

Once again the app will query the database and if there is no matching record, his new policy will be added into the database.

```
Policy 1
Policy 2
Policy 3
...
...
New Policy <-- just added!

```

##### Django framework
The project has been pre-initiated in Django framework. In Django, there are `models`, `views` and `templates`.
Here are some descriptions that we like for an easy high level understanding:

* **Model**

*"defines your data model by extrapolating your single lines of code into full database tables and adding a pre-built (totally optional) administration section to manage content." - Pamela Statz*

*"handles your data representation, it serves as an interface to the data stored in the database itself, and also allows you to interact with your data without having to get perturbed with all the complexities of the underlying database." - Ada Nduka Oyom*


* **View**

*"views are where you grab the data you’re presenting to the visitor" - Pamela Statz*

*"Django Views are custom Python code that get executed when a certain URL is accessed. Views can be as simple as returning a string of text to the user. They can also be made complex, querying databases, processing forms, processing credit cards, etc." - ultimatedjango.com*

*"serves as the bridge between the model and the template" - Ada Nduka Oyom*


* **Template**

*"this is a HTML web page, showing a combination of text and images." - ultimatedjango.com*

*"controls what should be displayed and how it should be displayed to the user" - Ada Nduka Oyom*

In summary:
```
"Here’s what happens when a visitor lands on your Django page:

1. First, Django consults the various URL patterns you’ve created and uses the information to retrieve a view.

2. The view then processes the request, querying your database if necessary.

3. The view passes the requested information on to your template.

4. The template then renders the data in a layout you’ve created and displays the page."
- Pamela Statz
```

We will now briefly describe how this project is implemented in Django.

Since the project has been pre-initiated in Django, we only need to create `insurer` app by running `python manage.py startapp insurer` in the root directory.

We know what data that we want to store and use in our database, therefore we create our models in `models.py`, specifying the data types. For this work, we have `Policy` and `Payment` model which represent two database tables.

We create views in `view.py`. All actions/data processing in [here](#making-a-payment) and [here](#adding-a-new-policy) are written in `views.py`. We create four views for the data - `policy_list` and `payment_list` to view the database records in json format, `add_policy` for new policy updates, and `make_payment` for payment processing/authorization. We then create basic html pages for the views.


## Using this app
Clone this repository: `git clone https://github.com/farahsamat/insurer.git`

In the working directory `src` directory, run `python manage.py runserver` and go to these links:
 * [to add new policies](http://127.0.0.1:8000/policy)
 
 * [for payments](http://127.0.0.1:8000/payment)
 
## Future work
Reformat codes to comply with the supplied [behavior test](https://github.com/farahsamat/insurer/tree/master/src/features).

Current error:

`policy_query = simplify(user_id+benefit+currency)`

 `TypeError: unsupported operand type(s) for +: 'NoneType' and 'NoneType'`


## Reference
[Getting Started With Django - Pamela Statz](https://www.wired.com/2010/02/get_started_with_django/)

[Understanding the MVC Pattern in Django - Ada Nduka Oyom](https://medium.com/shecodeafrica/understanding-the-mvc-pattern-in-django-edda05b9f43f)

[Learn Django - ultimatedjango.com](https://ultimatedjango.com/learn-django/lessons/how-django-works/)
