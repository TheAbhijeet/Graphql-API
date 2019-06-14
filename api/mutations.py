
# import graphene
# from .models import Post
# from graphene_django.types import DjangoObjectType
# # from .models import Category 
# import json
# # from api.schema import CategoryType

# # class CategoryType(DjangoObjectType):
# #     class Meta:
# #         model = Category

# class PostInput(graphene.InputObjectType):
#     title = graphene.String()
#     content = graphene.String()
#     category =  graphene.List(graphene.ID)
#     # category = graphene.String()


# class CreatePost(graphene.Mutation):
#     # slug = graphene.String()
#     title = graphene.String()
#     content = graphene.String()
#     # category =  graphene.String()
#     # tags = graphene.String()

#     #2
#     class Arguments:
#         # title = graphene.String()
#         # content = graphene.String()
#         # category =  graphene.String()
#         # tags = graphene.String()
#         # errors = graphene.String()

#         input = PostInput(description="These fields are required", required=True)

#     #3
#     @staticmethod
#     def mutate(root, info, input):

#         user = info.context.user
#         if not user.is_authenticated:
#             return CreatePost(errors=json.dumps('Please Login to list your company'))
        
#         # catgory = graphene.List(CategoryType)

#         post = Post.objects.create(
#         title=input.title, 
#         content=input.content,
#        category = input.category,
#         author = info.context.user,
#         )

#         Post.save()

#         return CreatePost(
#             title = Post.title,
#             content= Post.content,
#             category = Post.category ,
#             author = Post.author
#             )      

#         # return CreatePost(Post=post)
# #4



# # class CreatePost(graphene.Mutation):
# #     class Arguments:
# #         input = PostInput(
# #             required=True, description='Fields required to create a page.')
#     # class Meta:
#     #     description = 'Creates a new page.'
#     #     model = Post

#     # ok = graphene.Boolean()
#     # post = graphene.Field(lambda: Post)

#     # @staticmethod
#     # def mutate(self, info, title):
#     #     post = Post(title=title)
#     #     ok = True
#     #     return CreatePost(post=post, ok=ok)