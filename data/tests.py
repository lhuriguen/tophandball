from django.test import TestCase
from django.contrib.auth.models import User
from .models import Club


class ClubViewsTestCase(TestCase):
    def setUp(self):
        # Create some users
        self.user_1 = User.objects.create_user('User1', 'no@mail.com', 'tst1')
        self.user_2 = User.objects.create_user('User2', 'no@mail.com', 'tst2')
        self.user_3 = User.objects.create_user('User3', 'no@mail.com', 'tst3')
        self.club_1 = Club.objects.create(
            name='Test Club', country='ESP', ehf_id=0)

    def tearDown(self):
        self.user_1.delete()
        self.user_2.delete()
        self.user_3.delete()

    def test_index(self):
        resp = self.client.get('/data/clubs/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('club_list' in resp.context)
        self.assertEqual([club.pk for club in resp.context['club_list']], [1])

    def test_detail(self):
        resp = self.client.get('/data/clubs/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('fan' in resp.context)
        self.assertTrue('fan_count' in resp.context)
        self.assertTrue('comp_list' in resp.context)
        self.assertEqual(resp.context['club'].pk, 1)
        self.assertEqual(resp.context['club'].name, 'Test Club')
        self.assertEqual(resp.context['club'].country, 'ESP')
        self.assertEqual(resp.context['club'].ehf_id, 0)

        # Ensure that non-existent clubs throw a 404.
        resp = self.client.get('/data/clubs/2/')
        self.assertEqual(resp.status_code, 404)

    def test_matches(self):
        resp = self.client.get('/data/clubs/1/matches/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('match_list' in resp.context)
        self.assertTrue('club' in resp.context)
        self.assertTrue('fan' in resp.context)
        self.assertTrue('fan_count' in resp.context)

        # Ensure that non-existent clubs throw a 404.
        resp = self.client.get('/data/clubs/2/matches/')
        self.assertEqual(resp.status_code, 404)

    def test_update(self):
        # Unauthenticated users get redirected to login.
        resp = self.client.get('/data/clubs/1/edit/')
        self.assertEqual(resp.status_code, 302)

        # Ensure authenticated users can access the view.
        self.client.login(username='User1', password='tst1')
        resp = self.client.get('/data/clubs/1/edit/')
        self.assertEqual(resp.status_code, 200)
