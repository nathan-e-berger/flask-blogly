import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()



        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        test_post = Post(
            title="test2_title",
            content="test2_content",
            user_id=self.user_id
        )

        db.session.add(test_post)
        db.session.commit()

        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_single_user(self):
        """Tests the displaying of a single user's page"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Delete This User", html)

    def test_new_user_form(self):
        """Tests displaying new user form"""
        with self.client as c:
            resp = c.get('/users/new')
            html = resp.get_data(as_text=True)
            self.assertIn("Add This User", html)
            self.assertEqual(resp.status_code, 200)

    def test_edit_form(self):
        """Tests displaying edit user form"""
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Save", html)

    def test_register_user(self):
        """Tests registering user"""
        with self.client as c:
            resp = c.post("/users/new", data={ "first_name":"Jason", "last_name":"Molina", "image_source": DEFAULT_IMAGE_URL}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Jason", html)

    def test_register_redirect(self):
        """Test redirect after user registered"""
        with self.client as c:
            resp = c.post("/users/new", data={ "first_name":"Jason", "last_name":"Molina", "image_source": DEFAULT_IMAGE_URL}, follow_redirects=False)
            self.assertEqual(resp.status_code, 302)

    def test_show_new_post_form(self):
        """Test the function showing the form for a new post"""
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Add Post for", html)

    def test_show_post(self):
        """Test the showing of an individual post."""
        with self.client as c:
            resp = c.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("test2_content", html)

