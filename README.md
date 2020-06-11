# Consensus

Consensus is a real-time webapp made for keeping students and teachers on the same page during
class.

As a student, it's easy to miss something in class, but it's hard to know exactly what you missed --
sometimes the only thing I know is "I'm confused." It can be hard to figure out exactly what
question to ask to get yourself back on track, and it can be scary to make the class wait for you to
catch up.

As a teacher, it's hard to know exactly how students are feeling -- a student may look checked out
even though they're actually paying attention or have just seen the material before. Pausing for
questions doesn't always do the trick, and graded microquizzes or clicker questions can be
stressful.

Consensus provides students an "I'm confused" button and teachers a live-updating display for the
number of confused students. Consensus was born out of a [Design for
America](http://designforamerica.com/) project in 2018 with my team: @jynnie, @kelvin-lu, @mlarash,
and Hoang Nguyen.

# Contributing

Contributions are welcome. This project is build in Django with Django Channels. To get set up
locally, install `docker` and `docker-compose`.

`sudo docker-compose up` should spin the website up at `localhost:8000` (though I haven't really
tested this).

You might need to do some `docker-compose exec web python manage.py migrate`'s to get the database
up to speed.
