
A django blogpost app based on maximilian udemy course, since the course doesn't have signup/signin, i thought it would be a good idea to add it.
I made all routes protected except for the index (home page) route
you can fork the code.
<br />
<br />
<br />
<b>Usage</b> (assuming that you have python installed):<br />
python -m venv ENVIRONMENTNAME<br />
source venv/Scripts/activate<br />
pip install<br />
python manage.py makemigrations <br />
python manage.py migrate <br />
python manage.py runserver<br />
<br />
<br />
<br />

<b>Also you can creat a super user and navigate to /admin to mange the cotnent of the blog:</b>
<br />
python manage.py createsuperuser

<br />
<br />

<b>Note: the code is not prepared for deployment</b>

