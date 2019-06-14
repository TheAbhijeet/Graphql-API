import json
import graphene
# from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id
# from .mutations import CreatePost
from .models import Post, Comment, Page, Comment, User, Category, Tag, SeoModel, user_actions
## from mutations.py
from graphene import InputObjectType
from django.db.models import Q
from graphene_django.types import DjangoObjectType
import json

import graphql_jwt
# from graphql_jwt.decorators import login_required

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class PageType(DjangoObjectType):
    class Meta:
        model = Page

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class UserType(DjangoObjectType):
    class Meta:
        model = User

class TagType(DjangoObjectType):
    class Meta:
        model = Tag

class SeoModelType(DjangoObjectType):
    class Meta:
        model = SeoModel

class UactionType(DjangoObjectType):
    class Meta:
        model = user_actions
## Query

class Query(graphene.AbstractType):

    all_posts = graphene.List(PostType, search=graphene.String())
   

    def resolve_all_posts(self, info, search=None, **kwarg):
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
            return Post.objects.filter(filter)

        return Post.objects.all() 


    post = graphene.Field(PostType, id=graphene.Int())
    
    def resolve_post(self, info, **args):
        id = args.get('id')

        if id is not None :
            return Post.objects.get(pk=id)

    ## Comments

    all_comments = graphene.List(CommentType)
    comment = graphene.Field(CommentType, id=graphene.Int())
    def resolve_all_comments(self, info, **kwarg):
        return Comment.objects.all() 
    
    def resolve_comment(self, info, **args):
        id = args.get('id')

        if id is not None :
            return Comment.objects.get(pk=id)
    # comment = graphene.Field(CommentType, id=graphene.Int())
    ## Users
    all_users = graphene.List(UserType)

    user = graphene.Field(UserType, id=graphene.Int())
    def resolve_all_users(self, info, **kwarg):
        return User.objects.all() 
    
    def resolve_user(self, info, **args):
        id = args.get('id')

        if id is not None :
            return User.objects.get(pk=id)
    
    ## Categories

    all_categories = graphene.List(CategoryType)
    Category = graphene.Field(CategoryType, id = graphene.Int())
    def resolve_all_categories(self, info, **kwarg):
        return Category.objects.all() 
    
    def resolve_category(self, info, **args):
        id = args.get('id')

        if id is not None :
            return Category.objects.get(pk=id)

        ## Pages 

    all_Pages = graphene.List(PageType)
    page = graphene.Field(PageType, id = graphene.ID())

    def resolve_all_pages(self, info, **kwarg):
        return Page.objects.all() 
    
    def resolve_page(self, info, **args):
        id = args.get('id')

        if id is not None :
            return Page.objects.get(pk=id)

        ## Tag

    all_tags = graphene.List(TagType)

    def resolve_all_tags(self, info, **kwarg):
        return Tag.objects.all() 


    tag = graphene.Field(TagType, id=graphene.Int())
    
    def resolve_tag(self, info, **args):
        id = args.get('id')

        if id is not None :
            return Tag.objects.get(pk=id)


    ## Seo Model
    all_seomodel = graphene.List(SeoModelType)
    seomodel = graphene.Field(SeoModelType, id=graphene.Int())

    def resolve_all_seomodel(self, info, **kwargs):
        return SeoModel.objects.all()

    def resolve_seomodel(self, info, **args):
        id = args.get('id')

        if id is not None:
            return SeoModel.objects.get(pk=id)

    ## User action

    all_Uactions = graphene.List(UactionType)
    uactions = graphene.Field(UactionType, id=graphene.Int())

    def resolve_all_Uactions(self, info, **kwargs):
        return user_actions.objects.all()

    def resolve_uactions(self, info, **args):
        id = args.get('id')

        if id is not None:
            return user_actions.objects.get(pk=id)

# class Mutations(graphene.ObjectType):
#     create_post = CreatePost.Field()



# class PostInput(graphene.InputObjectType):
#     title = graphene.String()
#     content = graphene.String()
#     # category =  graphene.List(graphene.ID)
#     # category = graphene.String()
#     category_id = graphene.Field(CategoryType)



class CreatePost(graphene.Mutation):
    title = graphene.String()
    content = graphene.String()
    # slug = graphene.String()
    tags = graphene.Field(TagType)
    category = graphene.Field(CategoryType)

    #2
    class Arguments:
        title = graphene.String()
        content = graphene.String()
        tag_id =graphene.Int()
        category_id = graphene.Int()
        status = graphene.Int()
    # @staticmethod
    # @login_required
    def mutate(self, info, title, content, category_id, tag_id, status):
        user = info.context.user
        if not user.is_authenticated:
            return CreatePost(errors=json.dumps('Please Login to create a Post'))
        
        category = Category.objects.get(id=category_id)
        if not category:
            raise Exception('Invalid Category!')
        post =Post.objects.create(
        title= title, 
        content= content,
       category = category,
        author = info.context.user,
        status = status 
        )

        return CreatePost(
            title = title,
            content= content,
            
            )      
     
## Comment create mutation

class commentInput(InputObjectType):
    post_id = graphene.Int()
    parent_id = graphene.Int(required=False, default_value = None)
    description = graphene.String()


class CreateComment(graphene.Mutation):
    post = graphene.Field(PostType)
    description = graphene.String()
    parent_id = graphene.Field(CommentType)

    class Arguments:
        input = commentInput()
       

    def mutate(self, info, input):
        user = info.context.user
        if not user.is_authenticated:
            return CreateComment(errors=json.dumps('Please Login to create a Post'))
        
        if input.parent_id is None:
            post = Post.objects.get(id=input.post_id)
        
            comment = Comment.objects.create(
            post = post,
            author = info.context.user,
            description = input.description,
            )

            return CreateComment(
            description =input.description
            )
        
        else:
            parent_comment = Comment.objects.get(id=input.parent_id)
            post = Post.objects.get(id=input.post_id)

            comment = Comment.objects.create(
                post = post,
                author = info.context.user,
                description = input.description,
                parent = parent_comment
            )


            return CreateComment(
                description = input.description
            )

## Likes
# class CreateUaction(graphene.Mutation):
#     user = graphene.Field(UserType)
#     liked_post = graphene.Field(UactionType)

#     class Arguments:
#         post_id = graphene.Int()

#     def mutate(self, info, post_id):
#         user = info.context.user
#         if user.is_anonymous:
#             raise Exception('You must be logged to vote!')

#         liked_post = Post.objects.get(id=post_id)
#         if not Post:
#             raise Exception('Invalid Link!')

#         user_actions.objects.create(
#             user=user,
#             liked_post=liked_post,
#         )

#         return CreateUaction(user=user, liked_post=liked_post)

class UactionInput(InputObjectType):
    liked_post_id = graphene.Int()
    fav_post_id = graphene.Int()
    comment_id = graphene.Int()
    target_id = graphene.Int()
    follower_id = graphene.Int()
    
class CreateUaction(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input =  UactionInput()
       

    def mutate(self, info, input):
        user = info.context.user
        if not user.is_authenticated:
            return CreateUaction(errors=json.dumps('Please Login '))
        
        
        if input.liked_post_id:

            post = Post.objects.get(id=input.liked_post_id)
            user_action = user_actions.objects.create(
                liked_post = post,
                user = user 
            )

            return CreateUaction( user = user )

        if input.liked_comment_id:

            comment = Comment.objects.get(id=input.liked_comment_id)
            user_action = user_actions.objects.create(
                liked_comment = comment,
                user = user 
            )

            return CreateUaction(user = user )

        if input.fav_post_id:

            post = Post.objects.get(id=input.fav_post_id)
            user_action = user_actions.objects.create(
                fav = post,
                user = user 
            )

            return CreateUaction(user = user )

        if input.target_id:

            user = User.objects.get(id=input.target_id)
            user_action = user_actions.objects.create(
                target = user,
                user = user 
            )

            return CreateUaction(user = user )

        if input.follower_id:

            user = User.objects.get(id=input.follower_id)
            user_action = user_actions.objects.create(
                follower= user,
                user = user 
            )

            return CreateUaction(user = user )

class Mutation(graphene.ObjectType):
    create_post= CreatePost.Field()
    create_comment = CreateComment.Field()
    create_uaction = CreateUaction.Field()