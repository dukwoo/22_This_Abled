import json

from django.test import TestCase, Client

from .models import User

#유닛

class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="doboblock@google.com",
            name="bodoblock",
            password="0694",
        )

    def tearDown(self):
        User.objects.all().delete()
        
    def test_signup_success(self):
        client = Client()
        user = {
            "email": "bodoblock2@google.com",
            "name": "보도블록",
            "password": "0694",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})

    def test_duplication_user(self):
        client = Client()
        user = {
            "email": "loveim0112@gmail.com",
            "name": "임예진",
            "password": "yejin0694",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "ALREADY_EXISTED_EMAIL"})

    def test_email_format_error(self):
        client = Client()
        user = {
            "email": "sumin@gmail.com",
            "name": "이수민",
            "password": "sumin12",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "EMAIL_ERROR"})
    
    def test_password_format_error(self):
        client = Client()
        user = {
            "email": "jeongyoon@gmail.com",
            "name": "신정윤",
            "password": "jy0776",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "PASSWORD_ERROR"})
    
    def test_key_error(self):
        client = Client()
        user = {
            "email": "sooin@gmail.com",
            "name": "조수인",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "KEY_ERROR"})
        
        
        
        


# 통합
class TestView(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_james = User.objects.create_user(username='yejin', password='somepassword')
        self.user_james.is_staff = True
        self.user_james.save()
        self.user_trump = User.objects.create_user(username='sumin', password='somepassword')

        self.post_001 = Comunity.objects.create(
            title='일자리 검사 결과 음식 제조 분야 나오신 분?',
            content='음식 제조 분야 나오신 분 계신가요?',
            author=self.user_james,
            category=self.category_programming
        )
        self.post_001.tags.add(self.tag_hello)
        self.post_002 = Comunity.objects.create(
            title='취미 결과 운동 나오신 분 계신가요?',
            content='거리 가까우면 함께 운동해요~',
            author=self.user_trump,
            category=self.category_culture
        )
        self.post_003 Comunity.objects.create(
            title='뮤지컬 같이 보러가요.',
            content='표가 남아서 그런데, 뮤지컬 취미이신 분 함께 보러가요~',
            author=self.user_trump,
        )
        self.post_003.tags.add(self.tag_python)
        self.post_003.tags.add(self.tag_python_kor)

        self.comment_001 = Comment.objects.create(
            post = self.post_001,
            author = self.user_trump,
            content = '첫번째 댓글입니다.'
        )

    def test_search(self):
        post_004 = Comunity.objects.create(
            title="일자리에 대한 포스트입니다.",
            content="일자리 결과",
            author=self.user_trump
        )

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertNotIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertIn(self.post_003.title, main_area.text)
        self.assertIn(post_004.title, main_area.text)

    def test_comment_form(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(), 1)

        # 로그인 하지 않은 상태
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        comment_area = soup.find('div', id='comment-area')
        self.assertIn('Log in and leave a comment', comment_area.text)
        self.assertFalse(comment_area('form', id='comment-form'))

        # 로그인 한 상태
        self.client.login(username='Trump', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        comment_area = soup.find('div', id='comment-area')
        self.assertNotIn('Log in and leave a comment', comment_area.text)

        comment_form = comment_area.find('form', id='comment-form')
        self.assertTrue(comment_form.find('textarea', id='id_content'))

        response = self.client.post(
            self.post_001.get_absolute_url() + 'new_comment/',
            {
                'content' : "두번째 댓글입니다."
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)

        new_comment = Comment.objects.last()
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(new_comment.post.title, soup.title.text)
        comment_area = soup.find('div', id='comment-area')
        new_comment_div = comment_area.find('div', id=f'comment-{new_comment.pk}')
        self.assertIn('Trump', new_comment_div.text)
        self.assertIn('두번째 댓글입니다.', new_comment_div.text)

    def navbar_test(self, soup):
        # 네비게이션바가 있다 - soup.nav로 soup에 담긴 내용 중 nav요소만 가져와 navbar에 저장한다.
        navbar = soup.nav
        # 네비게이션바에 This_Abled, 마이페이지 라는 문구가 있다 - navbar의 텍스트 중
        self.assertIn('This_Abled', navbar.text)
        self.assertIn('마이페이지', navbar.text)

        logo = navbar.find('a',text='This_Abled')
        self.assertEqual(logo.attrs['href'], '/')
        home = navbar.find('a', text='마이페이지')
        self.assertEqual(home.attrs['href'], '/mypage/')
        blog = navbar.find('a', text='일자리테스트')
        self.assertEqual(blog.attrs['href'], '/job_test/')
        about = navbar.find('a', text='취미테스트')
        self.assertEqual(about.attrs['href'], '/hoby_test/')
        about = navbar.find('a', text='커뮤니티')
        self.assertEqual(about.attrs['href'], '/community/')

    def test_category_page(self):
        # 카테고리 페이지 url로 불러오기
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        # beautifulsoup4로 html을 parser하기
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_test(soup)
        # 카테고리 name을 포함하고 있는지
        self.assertIn(self.category_programming.name, soup.h1.text)
        # 카테고리에 포함된 post만 포함하고 있는지
        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_tag_page(self):
        # 카테고리 페이지 url로 불러오기
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        # beautifulsoup4로 html을 parser하기
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_test(soup)
        # 카테고리 name을 포함하고 있는지
        self.assertIn(self.tag_hello.name, soup.h1.text)
        # 카테고리에 포함된 post만 포함하고 있는지
        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_create_post(self):
        # 포스트 목록 페이지를 가져온다
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)
        self.client.login(username='Trump', password='somepassword')
        response = self.client.get('/blog/create_post/')
        # 정상적으로 페이지가 로드 - 404는 오류 200이 정상
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='James', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        # 페이지 타이틀이 'Blog'
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Create Post - Blog')
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)


    def test_update_post(self):
        update_url = f'/blog/update_post/{self.post_003.pk}/'
        # 로그인하지 않은 경우
        response = self.client.get(update_url)
        self.assertNotEqual(response.status_code, 200)

        # 로그인했지만 작성자가 아닌경우
        self.assertNotEqual(self.post_003.author, self.user_james)
        self.client.login(username='James', password='somepassword')
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 403) # 403은 forbidden(접근권한금지)

        # 로그인했지만 작성자인 경우
        self.client.login(username='Trump', password='somepassword')
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)

        # 수정 페이지
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Edit Post - Blog')
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        self.assertIn('파이썬 공부; python', tag_str_input.attrs['value'])


        # 포스트(게시물)의 타이틀이 3개 존재하는가 - 포스트가 생성되었으니 문구가 메인 영역에 더이상 없어야함 그래서 assertNotIn~
        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)

        self.assertIn(self.user_james.username.upper(), main_area.text)
        self.assertIn(self.user_trump.username.upper(), main_area.text)

        # 포스트(게시물)이 하나도 없는 경우
        Test.objects.all().delete()
        self.assertEqual(Test.objects.count(), 0)
        # 포스트 목록 페이지를 가져온다
        response = self.client.get('/')
        # 정상적으로 페이지가 로드
        self.assertEqual(response.status_code, 200)
        # 페이지 타이틀이 'Test'
        soup = BeautifulSoup(response.content, 'html.parser')
        # 적절한 안내 문구가 포함되어 있는지 - id가 main-area인 div요소를 찾아 main_area에 저장한다. 그리고 Post레코드가 하나도 없으니 문구가 나타나느지 점검
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)