from django.test import TestCase

class PostAndProfileTest(TestCase):
    def setUp(self):
        self.test_text="I am going to school"
        self.test_text_edit = "I am going to shop"
        self.client = Client()
        self.new_user = User.objects.create_user(
            username="sarah", 
            email="connor.s@skynet.com", 
            password="12345"
            )
        self.new_group = Group.objects.create(
            title="Skynet", 
            slug="skynet", 
            description="JugmentDay"
            )
        self.client.force_login(self.new_user)
        self.new_post = Post.objects.create(
            text=self.test_text, 
            author=self.new_user, 
            group=self.new_group
            )
        self.urls = (
            reverse("profile", 
                kwargs={"username": self.new_user.username}
                ), 
            reverse("index"), 
            reverse("post", 
                kwargs={"username": self.new_user.username, 
                    "post_id": self.new_post.id}
                )
            )
                    response = self.client.get(reverse(
            "profile", 
            kwargs={"username": self.new_user.username})
            )

response = client.post(reverse("token_obtain_pair", kwargs={"email": "2112311231312@yandex.ru", "confirmation_key": "vHVxZVecHQZi"}))