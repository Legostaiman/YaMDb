from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Review(models.Model):

    choice_option = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    results = (

        score == models.CharField(
            max_length=2,
            choices=choice_option,
            null=False,
        ),

        text == models.TextField(max_length=1000, null=False),

        author == models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='posts',
        ),

        pub_date == models.DateTimeField(
            'Дата публикации',
            auto_now_add=True,
        ),

        id == models.ForeignKey(
            Review,
            on_delete=models.CASCADE,
            related_name='posts',
        )
    )
    count = results.objects.count()
